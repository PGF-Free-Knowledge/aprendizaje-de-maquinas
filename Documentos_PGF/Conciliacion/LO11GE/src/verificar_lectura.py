import pandas as pd
import os

print("📂 Leyendo archivos exactamente como vienen, sin modificar nada...\n")

# Ruta base del proyecto
BASE_DIR = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE"

# Rutas completas a los archivos de entrada
path_ejec = os.path.join(BASE_DIR, "data", "Ejecxcuentas.csv")
path_egreper = os.path.join(BASE_DIR, "data", "Egreper.csv")

# Ruta carpeta de output
output_dir = os.path.join(BASE_DIR, "output")

# Crear carpeta output si no existe
os.makedirs(output_dir, exist_ok=True)

# Verificación de existencia
print("🔍 Verificando existencia de archivos:")
print(f" - {path_ejec} -> {'OK' if os.path.exists(path_ejec) else 'NO ENCONTRADO'}")
print(f" - {path_egreper} -> {'OK' if os.path.exists(path_egreper) else 'NO ENCONTRADO'}\n")

# Leer archivos sin modificar nada
try:
    df_ejec = pd.read_csv(path_ejec, dtype=str)
    print(f"✔️ Archivo Ejecxcuentas.csv leído correctamente. Filas: {len(df_ejec)}")

    # Guardar copia exacta en output
    salida_ejec = os.path.join(output_dir, "Ejecxcuentas_LEIDO.csv")
    df_ejec.to_csv(salida_ejec, index=False, encoding="utf-8-sig")
    print(f"📤 Copia generada en: {salida_ejec}")

except Exception as e:
    print(f"❌ Error leyendo Ejecxcuentas.csv:\n{e}")

print()

try:
    df_egre = pd.read_csv(path_egreper, dtype=str)
    print(f"✔️ Archivo Egreper.csv leído correctamente. Filas: {len(df_egre)}")

    # Guardar copia exacta en output
    salida_egre = os.path.join(output_dir, "Egreper_LEIDO.csv")
    df_egre.to_csv(salida_egre, index=False, encoding="utf-8-sig")
    print(f"📤 Copia generada en: {salida_egre}")

except Exception as e:
    print(f"❌ Error leyendo Egreper.csv:\n{e}")

print("\n🏁 Proceso finalizado.")
