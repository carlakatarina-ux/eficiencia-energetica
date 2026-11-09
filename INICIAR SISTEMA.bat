@echo off
title O&G - Gestao Energetica

cd /d "%~dp0"

echo.
echo ==========================================
echo       O&G - GESTAO ENERGETICA
echo ==========================================
echo.
echo Iniciando o sistema...
echo.

python -m streamlit run app.py

pause