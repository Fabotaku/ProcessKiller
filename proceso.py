import psutil
import os
import time
import winreg

# Nombre del proceso que queremos monitorear
process_name = input("Ingrese el nombre del proceso a limitar: ")
process_name += ".exe"

# Tiempo máximo que permitimos que el proceso se ejecute (en segundos)
max_process_time = 36000

# Tiempo de espera para no permitir que se abra el proceso nuevamente (en segundos)
lockout_time = 60 * 60 * 24 * 7

# Clave del registro de Windows donde se almacenará el tiempo de bloqueo del proceso
registry_key = "SOFTWARE\\DetalleApp"

# Obtenemos la lista de todos los procesos activos en el sistema
process_list = psutil.process_iter()

# Buscamos el proceso que nos interesa
process = None
for p in process_list:
    try:
        if p.name() == process_name:
            process = p
            break
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

# Si no encontramos el proceso, mostramos un mensaje y salimos
if not process:
    print(f"No se encontró el proceso {process_name} en ejecución.")
    exit()

# Obtenemos la hora actual
start_time = time.time()

# Monitoreamos el tiempo de ejecución del proceso
while process.is_running():
    if time.time() - start_time > max_process_time:
        print(f"Se ha superado el tiempo máximo de ejecución ({max_process_time} segundos). Cerrando el proceso...")
        process.terminate()
        break
    time.sleep(1)

# Bloqueamos el proceso en el registro de Windows
lock_time = int(time.time())
try:
    reg = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
    winreg.SetValueEx(reg, process_name, 0, winreg.REG_DWORD, lock_time)
    winreg.CloseKey(reg)
    print(f"El proceso {process_name} ha sido bloqueado por {lockout_time} segundos.")
except Exception as e:
    print(f"No se pudo bloquear el proceso {process_name}. {e}")

# Esperamos un tiempo para que no se pueda abrir el proceso nuevamente
time.sleep(lockout_time)

# Desbloqueamos el proceso si ha transcurrido suficiente tiempo desde su bloqueo
try:
    reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
    lock_time, _ = winreg.QueryValueEx(reg, process_name)
    winreg.CloseKey(reg)
    if time.time() - lock_time >= lockout_time:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
        print(f"El proceso {process_name} ha sido desbloqueado.")
except Exception as e:
    print(f"No se pudo desbloquear el proceso {process_name}. {e}")

