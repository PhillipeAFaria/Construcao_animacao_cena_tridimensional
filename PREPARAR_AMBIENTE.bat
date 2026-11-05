@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0preparar.ps1"
if errorlevel 1 (
  echo Falha na preparacao. Confira a mensagem acima.
  pause
  exit /b 1
)
pause
