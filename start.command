#!/bin/bash
cd "$(dirname "$0")"

echo "========================================"
echo "   Mac Launcher  "
echo "========================================"

if [ ! -d "venv" ]; then
    echo "[*] Setting up environment..."
    python3 -m venv venv
fi
source venv/bin/activate

python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[*] Installing dependencies..."
    pip install -r requirements.txt
fi

echo "[*] Launching PromptMill..."
open http://localhost:8501 2>/dev/null || xdg-open http://localhost:8501
python -m streamlit run app.py

chmod +x start.command