@echo off

IF "%~1"=="-help" GOTO helper

IF NOT EXIST .env (
    python -m venv .env
    cd .env\Scripts
    call activate.bat
    cd ../..
    pip install -r requirements.txt
) ELSE (
    cd .env\Scripts
    call activate.bat
    cd ../..
)
python.exe main.py
exit /b 0

:helper
echo NOM 
echo    envPython : create and start a virtual env for Python project. 
echo.
echo SYNTAXE
echo    envPython [-OPTION]
echo.
echo OPTION
echo    -h : the helper.