@echo off
echo Configurando Firewall para el Sistema SIC...
powershell -Command "New-NetFirewallRule -DisplayName 'Sistema SIC Acceso Movil' -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow"
if %errorlevel% equ 0 (
    echo [OK] El puerto 5000 ha sido abierto exitosamente.
) else (
    echo [ERROR] No se pudo abrir el puerto. Asegurate de ejecutar este archivo como ADMINISTRADOR.
)
pause
