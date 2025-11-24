import pandas as pd
import os

# ================================
#  CONFIGURACIÓN DE RUTAS
# ================================
BASE = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE"
PATH_DATA = f"{BASE}/data"
PATH_OUT  = f"{BASE}/output"

# Crear carpeta output si no existe
os.makedirs(PATH_OUT, exist_ok=True)

print("📂 Leyendo archivos...")

# ================================
# 1) LECTURA DE ARCHIVOS
# ================================
ejec = pd.read_csv(f"{PATH_DATA}/Ejecxcuentas_LEIDO.csv", dtype=str)
egre = pd.read_csv(f"{PATH_DATA}/Egreper_LEIDO.csv", dtype=str)
intra = pd.read_csv(f"{PATH_DATA}/Organizacion_intranet_limpio.csv", dtype=str)

print("   ✔️ Archivos cargados correctamente.")

# ================================
# 2) CONVERSIÓN A NÚMEROS SIN DECIMALES
# ================================
def to_int(x):
    if pd.isna(x):
        return 0
    return int(str(x).replace(".", "").replace(",", "").strip())

ejec["monto"] = ejec["monto"].apply(to_int)
egre["monto"] = egre["monto"].apply(to_int)
intra["monto"] = intra["monto"].apply(to_int)

# ================================
# 3) TABLA 1 — RELACIÓN EJEC vs EGRE (ARGOS)
# ================================
print("🔍 Generando conciliación entre Ejecxcuentas y Egreper...")

t1 = pd.merge(
    ejec,
    egre,
    on=["codigo"],
    how="outer",
    suffixes=("_ejec", "_egre")
)

# Agregar diferencia y estado
t1["monto_ejec"] = t1["monto_ejec"].fillna(0).astype(int)
t1["monto_egre"] = t1["monto_egre"].fillna(0).astype(int)

t1["diferencia"] = t1["monto_ejec"] - t1["monto_egre"]

def estado_row(row):
    if row["monto_ejec"] == row["monto_egre"]:
        return "COINCIDE"
    if row["monto_ejec"] != 0 and row["monto_egre"] != 0:
        return "DIFERENCIA"
    if row["monto_ejec"] != 0 and row["monto_egre"] == 0:
        return "SOLO EN EJEC"
    if row["monto_egre"] != 0 and row["monto_ejec"] == 0:
        return "SOLO EN EGRE"
    return "SIN INFORMACIÓN"

t1["estado"] = t1.apply(estado_row, axis=1)

# Guardar archivo
out1 = f"{PATH_OUT}/conciliacion_argos.csv"
t1.to_csv(out1, index=False, encoding="utf-8-sig")

print(f"   ✔️ conciliacion_argos.csv generado ({len(t1)} filas)")

# ================================
# 4) CONSOLIDADO ARGOS
# ================================
# Para comparar con Intranet, sumamos Ejec + Egre por codigo
consolidado_argos = (
    pd.concat([ejec[["codigo","monto"]], egre[["codigo","monto"]]])
    .groupby("codigo", as_index=False)
    .sum()
)

# ================================
# 5) TABLA 2 — ARGOS vs INTRANET
# ================================
print("🔍 Generando conciliación Argos consolidado vs Intranet...")

t2 = pd.merge(
    consolidado_argos,
    intra,
    on="codigo",
    how="outer",
    suffixes=("_argos", "_intra")
)

# Rellenar vacíos
t2["monto_argos"] = t2["monto_argos"].fillna(0).astype(int)
t2["monto_intra"] = t2["monto_intra"].fillna(0).astype(int)
t2["diferencia"] = t2["monto_argos"] - t2["monto_intra"]

def estado2(row):
    if row["monto_argos"] == row["monto_intra"]:
        return "COINCIDE"
    if row["monto_argos"] != 0 and row["monto_intra"] != 0:
        return "DIFERENCIA"
    if row["monto_argos"] != 0 and row["monto_intra"] == 0:
        return "SOLO ARGOS"
    if row["monto_intra"] != 0 and row["monto_argos"] == 0:
        return "SOLO INTRANET"
    return "SIN INFORMACIÓN"

t2["estado"] = t2.apply(estado2, axis=1)

# Guardar archivo
out2 = f"{PATH_OUT}/conciliacion_intranet.csv"
t2.to_csv(out2, index=False, encoding="utf-8-sig")

print(f"   ✔️ conciliacion_intranet.csv generado ({len(t2)} filas)")

print("\n🏁 PROCESO COMPLETO.\n")
