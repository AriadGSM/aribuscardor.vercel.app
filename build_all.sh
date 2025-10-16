#!/bin/bash
echo "==============================="
echo "🚀 INICIANDO BUILD COMPLETO..."
echo "==============================="

# 1️⃣ Activar entorno virtual
echo "🐍 Activando entorno virtual..."
source venv/bin/activate

# 2️⃣ Instalar dependencias de Python
echo "📦 Instalando dependencias Python..."
pip install -r requirements.txt

# 3️⃣ Compilar TypeScript (si existe)
if [ -d "Environment" ]; then
  echo "⚙️ Compilando TypeScript..."
  cd Environment
  tsc
  cd ..
fi

# 4️⃣ Ejecutar pruebas (opcional)
echo "🧪 Ejecutando pruebas..."
python3 -m unittest discover

# 5️⃣ Crear versión lista para producción
echo "📦 Creando paquete ZIP..."
rm -rf build
mkdir build
rsync -av --exclude 'venv' --exclude '__pycache__' . build
zip -r app_build.zip build

echo "==============================="
echo "✅ BUILD COMPLETO EXITOSO"
echo "Archivo generado: app_build.zip"
echo "==============================="
