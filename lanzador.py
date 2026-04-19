import os
import requests
import json
import subprocess
import time

# --- CONFIGURACIÓN (Ajusta estas URLs según tu servidor) ---
URL_VERSION = "http://tu-servidor.com/actualizaciones/version.json"
ARCHIVO_LOCAL_VERSION = "version_local.json"
EJECUTABLE_SISTEMA = "app_sistema.exe"

def check_for_updates():
    print("Buscando actualizaciones...")
    try:
        # 1. Obtener la versión más reciente del servidor
        response = requests.get(URL_VERSION, timeout=5)
        remote_data = response.json()
        remote_version = remote_data['version_actual']

        # 2. Leer la versión local
        local_version = "0.0.0"
        if os.path.exists(ARCHIVO_LOCAL_VERSION):
            with open(ARCHIVO_LOCAL_VERSION, 'r') as f:
                local_version = json.load(f).get('version_actual', "0.0.0")

        # 3. Comparar y descargar
        if remote_version > local_version:
            print(f"¡Nueva versión detectada! ({remote_version}). Descargando...")
            
            r = requests.get(remote_data['url_descarga'], stream=True)
            with open(EJECUTABLE_SISTEMA, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Guardar registro de la nueva versión local
            with open(ARCHIVO_LOCAL_VERSION, 'w') as f:
                json.dump(remote_data, f)
            
            print("Actualización completada con éxito.")
        else:
            print("El sistema ya está actualizado.")

    except Exception as e:
        print(f"Aviso: No se pudo verificar la actualización. {e}")
        print("Iniciando versión actual del sistema...")

def run_app():
    if os.path.exists(EJECUTABLE_SISTEMA):
        print(f"Iniciando {EJECUTABLE_SISTEMA}...")
        subprocess.Popen([EJECUTABLE_SISTEMA])
    else:
        print(f"Error fatal: No se encontró el archivo {EJECUTABLE_SISTEMA}")
        print("Por favor, asegúrate de haber compilado el sistema principal.")
        time.sleep(5)

if __name__ == "__main__":
    check_for_updates()
    run_app()
