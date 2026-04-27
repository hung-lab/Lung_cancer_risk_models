# ===================================================================
# FILE 4: convert_icon.py
# ===================================================================
# Script to convert PNG icon to Windows .ico and macOS .icns

import os
import subprocess

from PIL import Image

print("Converting icon to platform-specific icon formats...")

# Input icon
logo_path = "./app_icon.png"

if not os.path.exists(logo_path):
    print(f"ERROR: {logo_path} not found!")
    exit(1)

# Load image
img = Image.open(logo_path)

# === Windows .ico ===
print("Creating Windows .ico...")
ico_path = "icon.ico"
img.save(
    ico_path,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
)
print(f"✓ Created {ico_path}")

# === macOS .icns ===
print("Creating macOS .icns...")

# Check if on macOS (iconutil available)
if os.system("which iconutil > /dev/null 2>&1") == 0:
    # Create iconset directory
    iconset_dir = "icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)

    # Generate all required sizes
    sizes = [
        (16, "icon_16x16.png"),
        (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"),
        (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"),
        (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"),
        (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"),
        (1024, "icon_512x512@2x.png"),
    ]

    for size, filename in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(os.path.join(iconset_dir, filename))

    # Convert to .icns
    subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", "icon.icns"])

    # Clean up
    import shutil

    shutil.rmtree(iconset_dir)

    print("✓ Created icon.icns")
else:
    print("⚠ iconutil not available (macOS only), skipping .icns creation")
    print("  You can create .icns manually on macOS or use online converters")

print("\nIcon conversion complete!")
print("\nNext steps:")
print("pyinstaller Disconnectome.spec")
