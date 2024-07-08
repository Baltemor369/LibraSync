@echo off

IF NOT EXIST .env (
    echo environment creation..
    python -m venv .env
    cd .env\Scripts
    echo environment activation
    call activate.bat
    cd ../..
    echo requirements installation
    pip install -r requirements.txt
) ELSE (
    cd .env\Scripts
    echo environment activation
    call activate.bat
    echo environment activate
    cd ../..
)
echo launch app
python main.py