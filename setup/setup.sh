#!/bin/bash

VENV_DIR="venv"

# Determine the directory where the script is stored (setup/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CURRENT_DIR="$(pwd)"

# --- Check Execution Location ---
# Get project root absolute path (parent of setup/)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if current directory ($CURRENT_DIR) matches PROJECT_ROOT
if [ "$CURRENT_DIR" != "$PROJECT_ROOT" ]; then
    echo "[FATAL ERROR] ----------------------------------------"
    echo "This setup file must be executed from the Project Root Directory."
    echo "Current Location: $CURRENT_DIR"
    echo "Correct Execution Path: $PROJECT_ROOT"
    echo "Example Command: ./setup/setup.sh"
    echo "----------------------------------------"
    exit 1
fi

# --- Move to setup directory for requirements.txt ---
cd "$SCRIPT_DIR"

echo "----------------------------------------"
echo "1. Starting setup for Unix/Linux/macOS..."
echo "----------------------------------------"

# Find suitable Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python command not found. Please ensure Python is installed."
    # 元のディレクトリに戻る際も引用符を使用
    cd "$CURRENT_DIR"
    exit 1
fi

# Create venv in the root directory (PROJECT_ROOTは絶対パスで安全)
"$PYTHON_CMD" -m venv "$PROJECT_ROOT/$VENV_DIR"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment."
    cd "$CURRENT_DIR"
    exit 1
fi

echo "----------------------------------------"
echo "2. Activating venv and installing packages..."
echo "----------------------------------------"
# Activate venv
source "$PROJECT_ROOT/$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment."
    cd "$CURRENT_DIR"
    exit 1
fi

# Install packages from requirements.txt (in the current dir: setup/)
pip install -r "requirements.txt"
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install packages. Check requirements.txt."
    deactivate
    cd "$CURRENT_DIR"
    exit 1
fi

echo "----------------------------------------"
echo "Setup successful. Creating run.sh in the root directory."
echo "----------------------------------------"

# Create run.sh in the root directory
cat << EOF > "$PROJECT_ROOT/run.sh"
#!/bin/bash
# Execute main.py within the created virtual environment

source $VENV_DIR/bin/activate
# $PROJECT_ROOT/src/main.py に変更しても良いですが、元のパスを維持
python src/main.py "\$@" 
deactivate
EOF

# Ensure run.sh is executable
chmod +x "$PROJECT_ROOT/run.sh"

deactivate
# Return to the original directory (Project Root)
cd "$CURRENT_DIR"
echo "Setup is complete. You can run your program using ./run.sh from the root directory."