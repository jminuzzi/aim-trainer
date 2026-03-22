@echo off
setlocal

echo ========================================
echo   Gerando executavel do Treinador de Mira
echo ========================================

echo.
echo [1/3] Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install pygame pyinstaller

if errorlevel 1 (
    echo.
    echo Erro ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo [2/3] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist TreinadorDeMira.spec del /q TreinadorDeMira.spec

echo.
echo [3/3] Gerando executavel...
pyinstaller --onefile --windowed --name TreinadorDeMira treinador_mira.py

if errorlevel 1 (
    echo.
    echo Erro ao gerar o executavel.
    pause
    exit /b 1
)

echo.
echo Executavel criado com sucesso em:
echo dist\TreinadorDeMira.exe
pause
