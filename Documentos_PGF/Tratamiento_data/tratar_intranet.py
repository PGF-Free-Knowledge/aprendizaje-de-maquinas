import pandas as pd
import os

# Ruta base del repositorio
BASE_PATH = "Documentos_PGF/Tratamiento_data"

# Archivo original descargado desde Intranet
input_path = os.path.join(BASE_PATH, "Organizacion_intranet.xlsx")

# Archivo limpio de salida
output_path = os.path.join(BASE_PATH, "Organizacion_intranet_limpio.csv")

print("🔍 Leyendo archivo XLSX...")
df = pd.read_excel(input_path, header=None)

# Eliminar filas 0 y 1 (basura del archivo real)
df = df.drop(index=[0, 1])

# La fila 2 contiene la cabecera verdadera
df.columns = df.iloc[2]
df = df.drop(index=[2]).reset_index(drop=True)

# Detectar columnas de dinero (las que tienen un $ en alguna fila)
money_cols = [col for col in df.columns if df[col].astype(str).str.contains(r"\$").any()]

print("💰 Columnas monetarias detectadas:", money_cols)

# Limpiar columnas de dinero
for col in money_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Exportar CSV final
df.to_csv(output_path, index=False, encoding="utf-8")

print("✅ Archivo procesado correctamente.")
print(f"📁 CSV generado: {output_path}")
