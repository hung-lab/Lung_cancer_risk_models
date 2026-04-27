#!/bin/bash
# Build script for Disconnectome macOS application
# Usage: ./build_macos.sh [clean|build|both]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${GREEN}[*]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only"
    exit 1
fi

# Configuration
BUILD_TYPE="${1:-both}"
PROJECT_ROOT="$(pwd)"
SPEC_FILE="Disconnectome.spec"

# Check for required files
check_requirements() {
    print_status "Checking requirements..."

    if [ ! -f "$SPEC_FILE" ]; then
        print_error "Spec file not found: $SPEC_FILE"
        exit 1
    fi

    if [ ! -f "app.py" ]; then
        print_error "app.py not found"
        exit 1
    fi

    if ! command -v pyinstaller &> /dev/null; then
        print_error "PyInstaller not found. Install with: pip install pyinstaller"
        exit 1
    fi

    print_status "Requirements check passed"
}

# Clean build artifacts
clean_build() {
    print_status "Cleaning build artifacts..."

    # Remove build directories
    rm -rf build/
    rm -rf dist/
    rm -rf __pycache__/
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true

    # Remove spec file generated files
    rm -f Disconnectome.spec.bak

    print_status "Clean complete"
}


# Create icon if it doesn't exist
create_icon() {
    if [ ! -f "icon.icns" ] && [ -f "app_icon.png" ]; then
        print_status "Creating .icns icon from app_icon.png..."

        # Create iconset directory
        mkdir -p icon.iconset

        # Generate required icon sizes
        sips -z 16 16     app_icon.png --out icon.iconset/icon_16x16.png
        sips -z 32 32     app_icon.png --out icon.iconset/icon_16x16@2x.png
        sips -z 32 32     app_icon.png --out icon.iconset/icon_32x32.png
        sips -z 64 64     app_icon.png --out icon.iconset/icon_32x32@2x.png
        sips -z 128 128   app_icon.png --out icon.iconset/icon_128x128.png
        sips -z 256 256   app_icon.png --out icon.iconset/icon_128x128@2x.png
        sips -z 256 256   app_icon.png --out icon.iconset/icon_256x256.png
        sips -z 512 512   app_icon.png --out icon.iconset/icon_256x256@2x.png
        sips -z 512 512   app_icon.png --out icon.iconset/icon_512x512.png
        sips -z 1024 1024 app_icon.png --out icon.iconset/icon_512x512@2x.png

        # Create icns file
        iconutil -c icns icon.iconset

        # Clean up
        rm -rf icon.iconset

        print_status "Icon created: icon.icns"
    fi
}

# Build the application
build_app() {
    print_status "Starting PyInstaller build..."

    # Set environment variables for build
    export PYTHONOPTIMIZE=1

    # Run PyInstaller
    pyinstaller \
        --clean \
        --noconfirm \
        "$SPEC_FILE" \
        2>&1 | tee build.log

    if [ $? -eq 0 ]; then
        print_status "Build completed successfully!"
        configure_ssl_cert_runtime

        if [ -d "dist/Disconnectome.app" ]; then
            APP_SIZE=$(du -sh dist/Disconnectome.app | cut -f1)
            print_status "Application size: $APP_SIZE"
            print_status "Application location: $PROJECT_ROOT/dist/Disconnectome.app"
        fi
    else
        print_error "Build failed. Check build.log for details"
        exit 1
    fi
}

# Configure bundled app to always use bundled certifi CA bundle
configure_ssl_cert_runtime() {
    local app_root="dist/Disconnectome.app/Contents"
    local cert_file="$app_root/Resources/certifi/cacert.pem"
    local macos_dir="$app_root/MacOS"

    if [ ! -f "$cert_file" ]; then
        print_warning "Bundled certifi CA file not found: $cert_file"
        print_warning "Skipping SSL_CERT_FILE runtime wrapper setup"
        return 0
    fi

    create_ssl_wrapper "$macos_dir/Disconnectome"
    create_ssl_wrapper "$macos_dir/disconnectome-cli"

    print_status "Configured SSL_CERT_FILE runtime wrappers"
}

# Rename binary to *-bin and add a launcher that exports SSL_CERT_FILE
create_ssl_wrapper() {
    local executable_path="$1"
    local executable_name
    executable_name="$(basename "$executable_path")"
    local bin_path="${executable_path}-bin"

    if [ ! -f "$executable_path" ]; then
        print_warning "Executable not found, skipping wrapper: $executable_path"
        return 0
    fi

    mv "$executable_path" "$bin_path"

    cat > "$executable_path" <<EOF
#!/bin/bash
set -e
SCRIPT_DIR="\$(cd "\$(dirname "\$0")" && pwd)"
APP_ROOT="\$(cd "\$SCRIPT_DIR/.." && pwd)"
export SSL_CERT_FILE="\$APP_ROOT/Resources/certifi/cacert.pem"
exec "\$APP_ROOT/MacOS/${executable_name}-bin" "\$@"
EOF

    chmod +x "$executable_path"
}

# Test the built application
test_app() {
    print_status "Testing application..."

    if [ ! -d "dist/Disconnectome.app" ]; then
        print_error "Application not found"
        return 1
    fi

    # Try to launch the app
    print_status "Attempting to launch application..."
    open dist/Disconnectome.app

    print_status "Application launched. Check if it opens correctly."
    print_warning "Press Ctrl+C to stop if app doesn't open or crashes"
    sleep 5
}

# Create DMG (optional)
create_dmg() {
    if [ ! -d "dist/Disconnectome.app" ]; then
        print_error "Application not found. Build first."
        return 1
    fi

    print_status "Creating DMG installer..."

    DMG_NAME="Disconnectome-macOS.dmg"

    # Remove old DMG if exists
    [ -f "$DMG_NAME" ] && rm "$DMG_NAME"

    # Create DMG
    hdiutil create -volname "Disconnectome" \
        -srcfolder dist/Disconnectome.app \
        -ov -format UDZO \
        "$DMG_NAME"

    if [ $? -eq 0 ]; then
        DMG_SIZE=$(du -sh "$DMG_NAME" | cut -f1)
        print_status "DMG created: $DMG_NAME ($DMG_SIZE)"
    else
        print_error "Failed to create DMG"
        return 1
    fi
}

# Troubleshooting function
troubleshoot() {
    print_status "Running diagnostics..."

    echo ""
    echo "Python Version:"
    python --version

    echo ""
    echo "PyInstaller Version:"
    pyinstaller --version

    echo ""
    echo "Installed Packages (relevant):"
    pip list | grep -E "customtkinter|antspyx|scipy|numpy|nibabel|dipy"

    echo ""
    echo "Project Structure:"
    tree -L 2 -I '__pycache__|*.pyc|build|dist' || ls -R

    echo ""
    print_status "Check build.log for detailed error messages"
}

# Main execution
main() {
    echo ""
    echo "========================================"
    echo "  Disconnectome macOS Build Script"
    echo "========================================"
    echo ""

    check_requirements

    case "$BUILD_TYPE" in
        clean)
            clean_build
            ;;
        build)
            create_icon
            build_app
            ;;
        both)
            clean_build
            create_icon
            build_app
            ;;
        test)
            test_app
            ;;
        dmg)
            create_dmg
            ;;
        troubleshoot)
            troubleshoot
            ;;
        *)
            echo "Usage: $0 [clean|build|both|test|dmg|troubleshoot]"
            echo ""
            echo "Options:"
            echo "  clean         - Remove build artifacts"
            echo "  build         - Build the application"
            echo "  both          - Clean then build (default)"
            echo "  test          - Test the built application"
            echo "  dmg           - Create DMG installer"
            echo "  troubleshoot  - Run diagnostics"
            exit 1
            ;;
    esac

    echo ""
    print_status "Done!"
}

# Run main function
main
