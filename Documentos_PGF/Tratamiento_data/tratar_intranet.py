import pandas as pd
import os

# Ruta del archivo de entrada y salida
INPUT_FILE = "Organizacion_intranet.xlsx"
OUTPUT_FILE = "Organizacion_intranet_limpio.csv"

print("🔍 Leyendo archivo XLSX...")

# Verificar existencia del archivo
if not os.path.isfile(INPUT_FILE):
    raise FileNotFoundError(f"No encontré el archivo: {INPUT_FILE}")

# Leer archivo completo sin asumir encabezados
df_raw = pd.read_excel(INPUT_FILE, header=None, engine="openpyxl")

# -------------------------------------------------------
# 1) Eliminar filas basura arriba
# En tu archivo: fila 0 = vacía, fila 1 = título o basura
# La cabecera real está en fila 2
# -------------------------------------------------------
header_row = 2
df = df_raw.copy()
df.columns = df.iloc[header_row]
df = df.iloc[header_row + 1:].reset_index(drop=True)

# Limpia nombres de columnas
df.columns = [str(c).strip() for c in df.columns]

print("✔ Cabecera aplicada. Columnas detectadas:")
print(df.columns.tolist())

# -------------------------------------------------------
# 2) Detectar columnas monetarias
# -------------------------------------------------------
money_cols = [
    col for col in df.columns
    if df[col].astype(str).str.contains(r"\$", regex=True).any()
]

print("\n💰 Columnas monetarias detectadas:")
print(money_cols)

# -------------------------------------------------------
# 3) Convertir texto monetario a números **SIN DECIMALES**
# -------------------------------------------------------
for col in money_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    # Convertimos a número → luego a entero **sin decimales**
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df[col] = df[col].astype(float).astype(int)

print("\n✔ Conversión de montos finalizada (sin decimales).")

# -------------------------------------------------------
# 4) Guardar CSV limpio
# -------------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n✅ Archivo optimizado guardado en: {OUTPUT_FILE}")
print(f"Total filas procesadas: {len(df)}")
