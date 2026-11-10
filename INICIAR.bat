@echo off
REM Usa a pasta deste arquivo como diretorio do aplicativo.
cd /d "%~dp0"
REM A preparacao precisa ter criado o interpretador no ambiente virtual.
if not exist ".venv\Scripts\python.exe" (
  echo Execute PREPARAR_AMBIENTE.bat primeiro.
  pause
  exit /b 1
)
REM Executa o ponto de entrada com o Python e as bibliotecas do ambiente local.
".venv\Scripts\python.exe" main.py
if errorlevel 1 pause
