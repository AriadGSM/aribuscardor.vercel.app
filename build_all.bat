@echo off
setlocal enableextensions enabledelayedexpansion
chcp 65001 >nul
set "PYTHONUTF8=1"

title 🚀 BUILD AUTOMATICO DEL PROYECTO ARIAD GSM

:: 🎨 Colores
set "GREEN=[32m"
set "YELLOW=[33m"
set "CYAN=[36m"
set "RED=[31m"
set "RESET=[0m"

echo %CYAN%===========================================
echo 🚀 INICIANDO BUILD COMPLETO - ARIAD GSM
echo ===========================================%RESET%

:: Ir a la carpeta del script (evita rutas con ❤)
cd /d "%~dp0"

:: 1️⃣ Activar entorno virtual
echo %YELLOW%🐍 Activando entorno virtual...%RESET%
if not exist "venv\Scripts\activate.bat" (
    echo %RED%⚠️ No se encontró entorno virtual. Creando...%RESET%
    python -m venv "venv"
)
call "venv\Scripts\activate.bat" || (echo %RED%❌ No se pudo activar el entorno virtual.%RESET% & exit /b 1)

:: 2️⃣ Instalar dependencias Python
echo %YELLOW%📦 Instalando dependencias Python...%RESET%
if exist "requirements.txt" (
    pip install -r "requirements.txt" >nul
) else (
    echo Flask > "requirements.txt"
    echo mysql-connector-python >> "requirements.txt"
    echo Werkzeug >> "requirements.txt"
    pip install -r "requirements.txt" >nul
)
call :progress

:: 3️⃣ Instalar dependencias de Node y compilar TypeScript
if exist "package.json" (
    echo %YELLOW%🧩 Instalando dependencias Node...%RESET%
    npm install >nul
)
echo %YELLOW%🔧 Compilando TypeScript...%RESET%
where tsc >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%❌ TypeScript no está instalado globalmente. Ejecuta: npm install -g typescript%RESET%
) else (
    tsc >nul
)
call :progress

:: 4️⃣ Ejecutar pruebas
echo %YELLOW%🧪 Ejecutando pruebas (si existen)...%RESET%
pytest >nul 2>nul
call :progress

:: 5️⃣ Crear paquete ZIP seguro
echo %YELLOW%📦 Creando paquete ZIP del proyecto...%RESET%

if exist "app_build.zip" del "app_build.zip"

powershell -NoProfile -Command ^
"try {
    Compress-Archive -Path (Get-ChildItem -Path . -Exclude 'venv','__pycache__','node_modules','app_build.zip') -DestinationPath 'app_build.zip' -Force;
    Write-Host '✅ Archivo app_build.zip creado correctamente.' -ForegroundColor Green;
} catch {
    Write-Host '❌ Error al crear el ZIP.' -ForegroundColor Red;
    exit 1
}"

if not exist "app_build.zip" (
    echo %RED%❌ No se generó app_build.zip. Revisa los errores anteriores.%RESET%
    exit /b 1
)
call :progress

:: 6️⃣ Subir automáticamente al servidor cPanel (FTP)
echo %YELLOW%🌍 Subiendo automáticamente al servidor cPanel...%RESET%

:: 🔧 CONFIGURACIÓN FTP — CAMBIA ESTOS DATOS 🔧
set "FTP_SERVER=ftp.tudominio.com"
set "FTP_USER=tu_usuario_ftp"
set "FTP_PASS=tu_contraseña_ftp"
set "REMOTE_DIR=public_html"

powershell -NoProfile -Command ^
"try {
    Write-Host 'Conectando a %FTP_SERVER%...' -ForegroundColor Cyan;
    $ftp = 'ftp://%FTP_SERVER%/%REMOTE_DIR%/app_build.zip';
    $webclient = New-Object System.Net.WebClient;
    $webclient.Credentials = New-Object System.Net.NetworkCredential('%FTP_USER%', '%FTP_PASS%');
    $webclient.UploadFile($ftp, 'STOR', 'app_build.zip');
    Write-Host '✅ Archivo app_build.zip subido correctamente al servidor.' -ForegroundColor Green;
} catch {
    Write-Host '❌ Error al subir el archivo al servidor FTP.' -ForegroundColor Red;
}"

call :progress

:: 7️⃣ Finalización
echo %GREEN%===========================================
echo ✅ BUILD COMPLETO EXITOSO
echo 📁 Archivo generado: app_build.zip
echo 🌐 Subido a tu servidor: /%REMOTE_DIR%/
echo 🕒 Fecha: %date% %time%
echo ===========================================%RESET%

pause
exit /b

:: Función de barra de progreso
:progress
setlocal
set "BAR="
for /L %%G in (1,1,20) do (
    set "BAR=#%BAR%"
    <nul set /p "=" %CYAN%[%BAR%>%RESET%
    timeout /nobreak /t 1 >nul
)
echo.
endlocal
exit /b
