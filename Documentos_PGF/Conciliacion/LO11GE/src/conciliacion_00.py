import os
import pandas as pd

# ================================
# SECCIÓN 1: LECTURA DE ARCHIVOS
# ================================

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data")

FILE_INTRANET = os.path.join(DATA_PATH, "Organizacion_intranet_limpio.csv")
FILE_EGREP = os.path.join(DATA_PATH, "Egreper.csv")
FILE_EJECU = os.path.join(DATA_PATH, "Ejecxcuentas.csv")

print("📂 Leyendo archivos CSV...")

df_intranet = pd.read_csv(FILE_INTRANET, dtype=str)
df_egreper = pd.read_csv(FILE_EGREP, dtype=str)
df_ejecxcuentas = pd.read_csv(FILE_EJECU, dtype=str)

print("✔ Archivos cargados correctamente:")
print(f"  - Organizacion_intranet_limpio: {df_intranet.shape[0]} filas")
print(f"  - Egreper: {df_egreper.shape[0]} filas")
print(f"  - Ejecxcuentas: {df_ejecxcuentas.shape[0]} filas")


# =======================================
# SECCIÓN 2: NORMALIZACIÓN DE COLUMNAS
# =======================================

print("\n🔧 Normalizando columnas...")

df_intranet.columns = [c.strip().lower().replace(" ", "_") for c in df_intranet.columns]
df_egreper.columns = [c.strip().lower().replace(" ", "_") for c in df_egreper.columns]
df_ejecxcuentas.columns = [c.strip().lower().replace(" ", "_") for c in df_ejecxcuentas.columns]

print("✔ Nombres de columnas estandarizados.")


def limpiar_montos(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


columnas_montos = ["abono", "cargo", "monto", "valor"]

df_intranet = limpiar_montos(df_intranet, columnas_montos)
df_egreper = limpiar_montos(df_egreper, columnas_montos)
df_ejecxcuentas = limpiar_montos(df_ejecxcuentas, columnas_montos)

print("✔ Montos convertidos a formato numérico.")

for df in [df_intranet, df_egreper, df_ejecxcuentas]:
    if "n°_documento" in df.columns:
        df["n°_documento"] = df["n°_documento"].astype(str).str.strip()

print("✔ Columnas clave normalizadas.")
print("\n🎯 SECCIÓN 2 completada con éxito.")


# ============================================================
# SECCIÓN 3 — CONCILIACIÓN REAL (INTRANET vs EGREPER)
# ============================================================

print("\n🔗 Iniciando conciliación REAL entre bases...")

# Crear clave robusta de documento
df_intranet["documento_id"] = (
    df_intranet["documento"].astype(str).str.upper().str.strip()
)
df_egreper["documento_id"] = (
    df_egreper["documento"].astype(str).str.upper().str.strip()
)

# Merge para buscar coincidencias y detectar faltantes
df_conc = df_intranet.merge(
    df_egreper,
    on="documento_id",
    how="outer",
    suffixes=("_intranet", "_egreper"),
    indicator=True
)

# Clasificación del estado
df_conc["_estado"] = df_conc["_merge"].map({
    "both": "COINCIDE",
    "left_only": "FALTA_EN_EGREPER",
    "right_only": "FALTA_EN_INTRANET"
})

print("✔ Comparación Intranet ↔ Egreper completada.")


# ============================================================
# SECCIÓN 4 — INTEGRACIÓN CON EJECXCUENTAS (MAPEO DE CUENTAS)
# ============================================================

print("🔗 Añadiendo información de Ejecxcuentas...")

df_conc = df_conc.merge(
    df_ejecxcuentas,
    left_on="cuenta_intranet",
    right_on="cuenta",
    how="left"
)

print("✔ Mapeo de cuentas completado.")


# ============================================================
# SECCIÓN 5 — EXPORTACIÓN FINAL
# ============================================================

OUTPUT_PATH = "../output/resultado_conciliado.csv"
df_conc.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"\n✅ Archivo final generado: {OUTPUT_PATH}")
print(f"📌 Total de filas procesadas: {len(df_conc)}")
print("📌 Columnas en salida:", df_conc.columns.tolist())

