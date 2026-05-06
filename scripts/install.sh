#!/bin/bash
# install.sh
set -e
INSTALL_DIR="$HOME/.local/lib/lung"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR" "$BIN_DIR"
cp -r . "$INSTALL_DIR/"

cat > "$BIN_DIR/lung" << 'EOF'
#!/bin/bash
cd "$HOME/.local/lib/lung"
exec uv run tkinter-app "$@"
EOF

chmod +x "$BIN_DIR/lung"
echo "Installed. Run: lung"
