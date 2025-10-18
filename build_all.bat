@echo off
setlocal enableextensions enabledelayedexpansion
chcp 65001 >nul
set "PYTHONUTF8=1"

title 🚀 BUILD AUTOMATICO DEL PROYECTO ARIAD GSM

:: Colores ANSI
for /f "delims=" %%A in ('echo prompt $E^| cmd') do set "ESC=%%A"
set "GREEN=%ESC%[32m"
set "YELLOW=%ESC%[33m"
set "CYAN=%ESC%[36m"
set "RED=%ESC%[31m"
set "RESET=%ESC%[0m"

echo %CYAN%===========================================
echo 🚀 INICIANDO BUILD COMPLETO - ARIAD GSM
echo ===========================================%RESET%

cd /d "%~dp0"

:: 1) venv
echo %YELLOW%🐍 Activando entorno virtual...%RESET%
if not exist "venv\Scripts\activate.bat" (
  echo %YELLOW%Creando venv...%RESET%
  py -m venv "venv" || python -m venv "venv"
)
call "venv\Scripts\activate.bat" || (echo %RED%❌ No se pudo activar el entorno virtual.%RESET% & exit /b 1)

:: 2) Python deps
echo %YELLOW%📦 Instalando dependencias Python...%RESET%
python -m pip install -U pip >nul
if exist "requirements.txt" (
  python -m pip install -r "requirements.txt"
) else (
  >"requirements.txt" (
    echo Flask
    echo mysql-connector-python
    echo Werkzeug
  )
  python -m pip install -r "requirements.txt"
)
call :progress

:: 3) Node + TypeScript
if exist "package.json" (
  echo %YELLOW%🧩 Instalando dependencias Node...%RESET%
  call npm ci || call npm install
  echo %YELLOW%🔧 Compilando TypeScript...%RESET%
  call npx tsc || (call npm i -D typescript && call npx tsc)
)
call :progress

:: 4) Pruebas (si hay pytest)
echo %YELLOW%🧪 Ejecutando pruebas (si existen)...%RESET%
where pytest >nul 2>nul && python -m pytest
call :progress

:: 5) ZIP
echo %YELLOW%📦 Creando paquete ZIP del proyecto...%RESET%
if exist "app_build.zip" del /f /q "app_build.zip"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path (Get-ChildItem -Path . -Force -Exclude 'venv','__pycache__','node_modules','app_build.zip','build.log') -DestinationPath 'app_build.zip' -Force"
if not exist "app_build.zip" (
  echo %RED%❌ No se generó app_build.zip. Revisa los errores anteriores.%RESET%
  exit /b 1
) else (
  echo %GREEN%✅ Archivo app_build.zip creado correctamente.%RESET%
)
call :progress

echo %GREEN%===========================================
echo ✅ BUILD COMPLETO EXITOSO
echo 📁 Archivo generado: app_build.zip
echo 🕒 Fecha: %date% %time%
echo ===========================================%RESET%
exit /b 0

:progress
setlocal
set "BAR="
for /L %%G in (1,1,20) do (
  set "BAR=#%BAR%"
  <nul set /p "=%CYAN%[%BAR%^>%RESET%"
  timeout /nobreak /t 1 >nul
)
echo.
endlocal
exit /b
