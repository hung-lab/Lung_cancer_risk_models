#!/bin/bash
# install.sh
set -e
INSTALL_DIR="$HOME/.local/lib/PulmoRisk"
BIN_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR" "$BIN_DIR"
cp -r . "$INSTALL_DIR/"

cat > "$BIN_DIR/PulmoRisk" << 'EOF'
#!/bin/bash
cd "$HOME/.local/lib/PulmoRisk"
exec uv run pulmorisk "$@"
EOF

chmod +x "$BIN_DIR/PulmoRisk"
echo "Installed. Run: PulmoRisk"
