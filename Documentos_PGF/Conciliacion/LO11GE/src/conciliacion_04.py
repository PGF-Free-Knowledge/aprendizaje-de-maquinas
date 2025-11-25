import pandas as pd
import os

# -----------------------------
# Rutas estándar del proyecto
# -----------------------------
BASE = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE"
DATA = f"{BASE}/data"
OUTPUT = f"{BASE}/output"

os.makedirs(OUTPUT, exist_ok=True)

# -----------------------------
# 1. Cargar archivos
# -----------------------------
print("📂 Cargando archivos...")

ejec = pd.read_csv(f"{DATA}/Ejecxcuentas_LEIDO.csv")
egre = pd.read_csv(f"{DATA}/Egreper_LEIDO.csv")
intra = pd.read_csv(f"{DATA}/Organizacion_intranet_limpio.csv")
cuentas = pd.read_csv(f"{DATA}/Cuentas_Codigos.csv")

print("   ✔️ Archivos cargados correctamente.")

# Normalizar columnas del maestro de cuentas
cuentas.rename(columns={
    "CUENTA": "codigo_cuenta",
    "NOMBRE_CUENTA": "nombre_cuenta"
}, inplace=True)

# -----------------------------
# 2. Normalizar nombres de columnas
# -----------------------------
ejec.rename(columns={
    "Cuenta": "codigo_cuenta",
    "Presupuesto": "presupuesto",
    "Gastos": "gastos"
}, inplace=True)

egre.rename(columns={
    "Cod Cuenta": "codigo_cuenta",
    "Monto": "monto"
}, inplace=True)

intra.rename(columns={
    "Cuenta": "codigo_cuenta",
    "Abono": "abono",
    "Cargo": "cargo"
}, inplace=True)

# -----------------------------
# 3. Convertir montos a números
# -----------------------------
def to_int(x):
    if pd.isna(x):
        return 0
    return int(str(x).replace(".", "").replace(",", "").replace("$", ""))

ejec["presupuesto"] = ejec["presupuesto"].apply(to_int)
ejec["gastos"] = ejec["gastos"].apply(to_int)

egre["monto"] = egre["monto"].apply(to_int)

intra["abono"] = intra["abono"].apply(to_int)
intra["cargo"] = intra["cargo"].apply(to_int)

# -----------------------------
# 4. Unificar ingresos/egresos
# -----------------------------
print("🔧 Unificando ARGOS...")

# Ejecxcuentas: ingresos y egresos separados
ejec_ingresos = ejec[["codigo_cuenta", "presupuesto"]].copy()
ejec_ingresos["monto"] = ejec_ingresos["presupuesto"]
ejec_ingresos["origen"] = "ejec_presupuesto"

ejec_egresos = ejec[["codigo_cuenta", "gastos"]].copy()
ejec_egresos["monto"] = ejec_egresos["gastos"] * -1
ejec_egresos["origen"] = "ejec_gastos"

# Egreper: monto ya tiene signo
egre2 = egre[["codigo_cuenta", "monto", "Glosa", "Fecha", "Documento"]].copy()
egre2["origen"] = "egreper"

# -----------------------------
# 5. Unión de todos
# -----------------------------
argos = pd.concat([ejec_ingresos[["codigo_cuenta", "monto", "origen"]],
                   ejec_egresos[["codigo_cuenta", "monto", "origen"]],
                   egre2],
                  ignore_index=True)

# -----------------------------
# 6. Validar contra la tabla de cuentas
# -----------------------------
argos = argos.merge(cuentas, on="codigo_cuenta", how="left")

# -----------------------------
# 7. Exportar
# -----------------------------
output_file = f"{OUTPUT}/argos_unificado.csv"
argos.to_csv(output_file, index=False)

print(f"🏁 Unificación completada.")
print(f"📄 Archivo generado: {output_file}")
