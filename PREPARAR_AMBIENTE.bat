@echo off
REM Define o diretorio do projeto mesmo quando o arquivo e aberto por duplo clique.
cd /d "%~dp0"
REM Delega a busca do Python e a instalacao ao script PowerShell.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0preparar.ps1"
if errorlevel 1 (
  echo Falha na preparacao. Confira a mensagem acima.
  pause
  exit /b 1
)
pause
