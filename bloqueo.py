import os
import winreg
import time

# Nombre del archivo .exe que quieres bloquear
nombre_archivo = "notepad.exe"

# Buscar el archivo en el sistema
for raiz, directorios, archivos in os.walk("C:\\"):
    if nombre_archivo in archivos:
        ruta_archivo = os.path.join(raiz, nombre_archivo)
        break

# Verificar si se encontró el archivo
if not ruta_archivo:
    print(f"No se encontró el archivo {nombre_archivo}")
    exit()

# Crear la entrada en el registro de Windows para restringir el acceso al archivo
llave_registro = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer")
winreg.SetValueEx(llave_registro, "DisallowRun", 0, winreg.REG_DWORD, 1)

# Agregar la ruta del archivo a la lista de programas bloqueados
llave_registro = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun")
winreg.SetValueEx(llave_registro, "1", 0, winreg.REG_SZ, ruta_archivo)

print(f"Se ha bloqueado el acceso al archivo {ruta_archivo}")

# Esperar 10 segundos
time.sleep(10)

# Eliminar la entrada del registro creada anteriormente
winreg.DeleteValue(llave_registro, "1")
winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun")

print(f"Se ha eliminado el bloqueo al archivo {ruta_archivo}")
