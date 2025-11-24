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
            # Quitar símbolos, puntos y comas
            df[col] = (
                df[col].astype(str)
                .str.replace("$", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
            )

            # Convertir a entero (sin decimales)
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

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

# ============================================================
# SECCIÓN 4 — TABLA DE DIFERENCIAS POR DOCUMENTO
# ============================================================

print("\n📄 Generando diferencias por DOCUMENTO...")

# Documentos únicos en cada base
docs_intranet = set(df_intranet["documento"].dropna().unique())
docs_egreper = set(df_egreper["documento"].dropna().unique())

# A: Documentos en Intranet pero NO en Egreper
docs_solo_intranet = docs_intranet - docs_egreper

df_solo_intranet = df_intranet[df_intranet["documento"].isin(docs_solo_intranet)].copy()
df_solo_intranet["origen"] = "Solo en Intranet"

# B: Documentos en Egreper pero NO en Intranet
docs_solo_egreper = docs_egreper - docs_intranet

df_solo_egreper = df_egreper[df_egreper["documento"].isin(docs_solo_egreper)].copy()
df_solo_egreper["origen"] = "Solo en Egreper"

# Unimos ambas diferencias
df_diferencias_documentos = pd.concat([df_solo_intranet, df_solo_egreper], ignore_index=True)

# Exportar
output_diff_docs = "../output/diferencias_documentos.csv"
df_diferencias_documentos.to_csv(output_diff_docs, index=False, encoding="utf-8-sig")

print("✔ Tabla de diferencias por documento generada.")
print(f"📌 Archivo: {output_diff_docs}")
print(f"📌 Total diferencias detectadas: {len(df_diferencias_documentos)}")

# ============================================================
# SECCIÓN 5 — DIFERENCIAS POR CUENTA
# ============================================================

print("\n📊 Generando diferencias por CUENTA...")

# --- Calcular totales por cuenta en Intranet ---
df_intranet_tot = df_intranet.copy()
df_intranet_tot["monto_intranet"] = df_intranet_tot[["abono", "cargo"]].fillna(0).sum(axis=1)

tot_intranet = (
    df_intranet_tot.groupby("cuenta")["monto_intranet"]
    .sum()
    .reset_index()
)

# --- Calcular totales por cuenta en Egreper ---
tot_egreper = (
    df_egreper.groupby("cuenta")["monto"]
    .sum()
    .reset_index()
    .rename(columns={"monto": "monto_egreper"})
)

# --- Unir totales ---
df_cuentas = tot_intranet.merge(
    tot_egreper,
    on="cuenta",
    how="outer"
)

# Rellenar nulos
df_cuentas["monto_intranet"] = df_cuentas["monto_intranet"].fillna(0)
df_cuentas["monto_egreper"] = df_cuentas["monto_egreper"].fillna(0)

# --- Calcular diferencia ---
df_cuentas["diferencia"] = df_cuentas["monto_intranet"] - df_cuentas["monto_egreper"]

# --- Estado ---
df_cuentas["estado"] = df_cuentas["diferencia"].apply(
    lambda x: "OK" if abs(x) < 1 else "Descuadre"
)

# --- Ordenar por peor descuadre ---
df_cuentas = df_cuentas.sort_values("diferencia", ascending=False)

# --- Exportar ---
output_diff_cuentas = "../output/diferencias_cuentas.csv"
df_cuentas.to_csv(output_diff_cuentas, index=False, encoding="utf-8-sig")

print("✔ Tabla de diferencias por cuenta generada.")
print(f"📌 Archivo: {output_diff_cuentas}")
print(f"📌 Total cuentas analizadas: {len(df_cuentas)}")
print(f"📌 Cuentas con descuadre: {sum(df_cuentas['estado']=='Descuadre')}")
