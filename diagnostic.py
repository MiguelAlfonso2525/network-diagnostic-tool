import subprocess
import datetime

def obtener_info_red():
    """
    Ejecuta ipconfig y extrae la información
    importante de la red.
    Como cuando abres CMD y escribes ipconfig
    pero automáticamente.
    """
    resultado = subprocess.run(
        ["ipconfig"],
        capture_output=True,
        text=True
    )
    return resultado.stdout

def hacer_ping(destino, intentos=2):
    """
    Hace ping a una IP o dominio.
    Retorna True si responde, False si no.
    
    destino: la IP o dominio a verificar
    intentos: cuántas veces intenta
    """
    resultado = subprocess.run(
        ["ping", destino, "-n", str(intentos)],
        capture_output=True,
        text=True
    )
    # Si "Respuesta desde" aparece → hay conexión
    return "Respuesta desde" in resultado.stdout

def verificar_dns(dominio="google.com"):
    """
    Verifica si el DNS funciona intentando
    resolver un dominio conocido.
    Es como preguntar: ¿el traductor funciona?
    """
    resultado = subprocess.run(
        ["ping", dominio, "-n", "1"],
        capture_output=True,
        text=True
    )
    return "Respuesta desde" in resultado.stdout

def mostrar_reporte(ip_local, gateway, 
                    internet, dns):
    """
    Muestra el resultado del diagnóstico
    de forma clara y ordenada.
    """
    ahora = datetime.datetime.now()
    
    print("\n" + "="*40)
    print("  DIAGNÓSTICO DE RED")
    print(f"  {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*40)
    
    print(f"\n  IP local:  {ip_local}")
    print(f"  Gateway:   {gateway}")
    
    if internet:
        print(f"  Internet:  ✅ Conectado")
    else:
        print(f"  Internet:  ❌ Sin conexión")
    
    if dns:
        print(f"  DNS:       ✅ Funcionando")
    else:
        print(f"  DNS:       ❌ Fallando")
    
    print("\n" + "-"*40)
    
    # Diagnóstico inteligente
    if not internet:
        print("  ⚠ PROBLEMA: Sin internet")
        print("  💡 Solución: Verifica el cable")
        print("     o reinicia el router")
    elif not dns:
        print("  ⚠ PROBLEMA: DNS fallando")
        print("  💡 Solución: Cambia el DNS a")
        print("     8.8.8.8 en tu configuración")
    else:
        print("  ✅ Todo funciona correctamente")
    
    print("="*40 + "\n")

# Programa principal
if __name__ == "__main__":
    print("\nDiagnosticando tu red...")
    
    # Paso 1: obtener info de red
    info = obtener_info_red()
    
    # Extraer IP y gateway del resultado
    ip_local = "No detectada"
    gateway = "No detectada"
    
    for linea in info.split("\n"):
        if "IPv4" in linea:
            ip_local = linea.split(":")[-1].strip()
        if "Puerta de enlace" in linea and \
           "." in linea:
            gateway = linea.split(":")[-1].strip()
    
    # Paso 2: verificar internet
    internet = hacer_ping("8.8.8.8")
    
    # Paso 3: verificar DNS
    dns = verificar_dns("google.com")
    
    # Paso 4: mostrar reporte
    mostrar_reporte(ip_local, gateway,
                    internet, dns)