import pandas as pd
import os
import re

# Rutas
path_ejec = "../data/Ejecxcuentas.csv"
path_egre = "../data/Egreper.csv"
output_dir = "../output/"
os.makedirs(output_dir, exist_ok=True)

print("📂 Leyendo archivos...")

############################
# 1) EJECXCUENTAS - SIN CAMBIOS
############################
df_ejec = pd.read_csv(path_ejec, dtype=str)
df_ejec.to_csv(os.path.join(output_dir, "Ejecxcuentas_LEIDO.csv"),
               index=False, encoding="utf-8-sig")
print("✔️ Ejecxcuentas listo.")


############################
# 2) EGREPER - LIMPIAR Y FORMATEAR SOLO COLUMNA MONTO
############################
df_egre = pd.read_csv(path_egre, dtype=str)

# Identificar la columna de montos (case insensitive)
col_monto = None
for c in df_egre.columns:
    if "monto" in c.lower():
        col_monto = c
        break

if not col_monto:
    raise Exception("❌ No se encontró columna con 'monto' en Egreper.csv")

print(f"🔧 Columna detectada como monto: {col_monto}")

def limpiar_a_entero(valor):
    if pd.isna(valor):
        return 0
    # Quitar todo lo que no sea dígito o signo negativo
    limpio = re.sub(r"[^0-9\-]", "", valor)
    if limpio in ["", "-"]:
        return 0
    return int(limpio)

def formatear_chileno(n):
    return f"{n:,}".replace(",", ".")   # 1,600,000 → 1.600.000

# 1) Limpiar el valor
df_egre[col_monto] = df_egre[col_monto].apply(limpiar_a_entero)

# 2) Formatear como miles chilenos
df_egre[col_monto] = df_egre[col_monto].apply(formatear_chileno)

# Guardar archivo final
df_egre.to_csv(os.path.join(output_dir, "Egreper_LEIDO.csv"),
               index=False, encoding="utf-8-sig")

print("📤 Generado Egreper_LEIDO.csv con separador de miles correcto.")
print("🏁 Proceso finalizado.")

