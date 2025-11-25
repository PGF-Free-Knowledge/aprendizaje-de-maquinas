import pandas as pd
import os

DATA = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE/data"
OUTPUT = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE/output"

print("📂 Leyendo archivos...")

ejec = pd.read_csv(f"{DATA}/Ejecxcuentas_LEIDO.csv")
egre = pd.read_csv(f"{DATA}/Egreper_LEIDO.csv")
intra = pd.read_csv(f"{DATA}/Organizacion_intranet_limpio.csv")
cuentas = pd.read_csv(f"{DATA}/Cuentas_Codigos.csv")

print("✔️ Archivos cargados correctamente.\n")

# ============================================================
# 🔧 Función única y robusta para limpiar montos chilenos
# ============================================================

def limpiar_monto(x):
    if pd.isna(x):
        return 0
    x = str(x).strip()
    x = x.replace(".", "")   # miles
    x = x.replace(",", "")   # por si acaso
    if x == "" or x == "-" or x == "--":
        return 0
    return int(x)

# ============================================================
# 🔧 Limpieza EJEC (Presupuesto / Devengado / Pagado / Gastos)
# ============================================================

columnas_montos_ejec = ["Presupuesto", "Devengado", "Pagado", "Gastos"]

for col in columnas_montos_ejec:
    if col in ejec.columns:
        try:
            ejec[col] = ejec[col].apply(limpiar_monto)
        except Exception as e:
            print(f"⚠️ Error limpiando columna {col}: {e}")
            print(ejec[col].head())
            raise

# Normalizar cuenta
ejec = ejec.rename(columns={"Cuenta": "codigo_cuenta"})
ejec["codigo_cuenta"] = ejec["codigo_cuenta"].astype(str)

# ============================================================
# 🔧 Limpieza EGREPER (monto)
# ============================================================

egre = egre.rename(columns={"Cod Cuenta": "codigo_cuenta", "Monto": "monto"})
egre["codigo_cuenta"] = egre["codigo_cuenta"].astype(str)

if "monto" in egre.columns:
    try:
        egre["monto"] = egre["monto"].apply(limpiar_monto)
    except Exception as e:
        print(f"⚠️ Error limpiando columna monto en EGRE: {e}")
        print(egre["monto"].head())
        raise

# ============================================================
# 1. UNIFICACIÓN ARGOS
# ============================================================

print("🔧 Unificando datos de ARGOS...")

argos = pd.concat([
    ejec[["codigo_cuenta", "Presupuesto", "Gastos"]],
    egre[["codigo_cuenta", "monto"]]
], ignore_index=True)

# ============================================================
# 2. Normalizar INTRANET
# ============================================================

print("🔧 Normalizando INTRANET...")

intra = intra.rename(columns={"Cuenta": "codigo_cuenta"})
intra["codigo_cuenta"] = intra["codigo_cuenta"].astype(str)

intra["Abono"] = intra["Abono"].apply(limpiar_monto)
intra["Cargo"] = intra["Cargo"].apply(limpiar_monto)

intra["neto"] = intra["Abono"] - intra["Cargo"]

# ============================================================
# 3. Agrupar ARGOS por cuenta
# ============================================================

argos_group = argos.groupby("codigo_cuenta").sum(numeric_only=True).reset_index()

argos_group["monto_argos"] = (
    argos_group.get("Presupuesto", 0)
    + argos_group.get("Gastos", 0)
    + argos_group.get("monto", 0)
)

argos_group = argos_group[["codigo_cuenta", "monto_argos"]]

# ============================================================
# 4. Agrupar INTRANET por cuenta
# ============================================================

intra_group = intra.groupby("codigo_cuenta")["neto"].sum().reset_index()
intra_group = intra_group.rename(columns={"neto": "monto_intranet"})

# ============================================================
# 5. Cruces para conciliación
# ============================================================

print("🔍 Comparando ARGOS vs INTRANET...")

solo_argos = argos_group[~argos_group["codigo_cuenta"].isin(intra_group["codigo_cuenta"])]
solo_intra = intra_group[~intra_group["codigo_cuenta"].isin(argos_group["codigo_cuenta"])]

comparado = argos_group.merge(intra_group, on="codigo_cuenta", how="inner")
diferencias = comparado[comparado["monto_argos"] != comparado["monto_intranet"]]

# ============================================================
# 6. Exportar resultados
# ============================================================

solo_argos.to_csv(f"{OUTPUT}/solo_en_argos.csv", index=False)
solo_intra.to_csv(f"{OUTPUT}/solo_en_intranet.csv", index=False)
diferencias.to_csv(f"{OUTPUT}/diferencias_montos.csv", index=False)

print("\n🏁 Conciliación completada.")
print(f"📤 Generado: solo_en_argos.csv")
print(f"📤 Generado: solo_en_intranet.csv")
print(f"📤 Generado: diferencias_montos.csv\n")

# ============================================================
# 7. Generar archivo conciliado final
# ============================================================

print("📝 Generando archivo conciliado final...")

resultado = argos_group.merge(intra_group, on="codigo_cuenta", how="outer")

# Indicador de presencia
resultado["en_argos"] = resultado["monto_argos"].notna().astype(int)
resultado["en_intranet"] = resultado["monto_intranet"].notna().astype(int)

# Llenar NaN con 0 para cálculo
resultado["monto_argos"] = resultado["monto_argos"].fillna(0)
resultado["monto_intranet"] = resultado["monto_intranet"].fillna(0)

# Diferencia
resultado["diferencia"] = resultado["monto_argos"] - resultado["monto_intranet"]

# Ordenar por código
resultado = resultado.sort_values("codigo_cuenta")

# Exportar
resultado.to_csv(f"{OUTPUT}/resultado_conciliado.csv", index=False)

print("📤 Generado: resultado_conciliado.csv")

# ============================================================
# 8. RESUMEN EJECUTIVO DE TOTALES
# ============================================================

print("📊 Generando resumen de totales...")

# === Totales generales ===
total_argos = resultado["monto_argos"].sum()
total_intra = resultado["monto_intranet"].sum()
total_diferencia = resultado["diferencia"].sum()

resumen_totales = pd.DataFrame({
    "descripcion": ["Total ARGOS", "Total INTRANET", "Diferencia Total"],
    "monto": [total_argos, total_intra, total_diferencia]
})

resumen_totales.to_csv(f"{OUTPUT}/resumen_totales.csv", index=False)
print("📤 Generado: resumen_totales.csv")

# === Resumen por grupo de cuenta (ej: 11, 21, 33) ===
resultado["grupo"] = resultado["codigo_cuenta"].str[:2]

resumen_por_grupo = resultado.groupby("grupo")[["monto_argos", "monto_intranet", "diferencia"]].sum().reset_index()
resumen_por_grupo.to_csv(f"{OUTPUT}/resumen_por_grupo.csv", index=False)
print("📤 Generado: resumen_por_grupo.csv")

# === Estado de conciliación ===
total_cuentas = len(resultado)
coinciden = len(resultado[resultado["diferencia"] == 0])
no_coinciden = len(resultado[resultado["diferencia"] != 0])
solo_argos_cnt = len(solo_argos)
solo_intra_cnt = len(solo_intra)

resumen_estado = pd.DataFrame({
    "item": ["Cuentas Totales", "Cuentas Iguales", "Cuentas con Diferencias",
             "Solo en ARGOS", "Solo en INTRANET"],
    "cantidad": [total_cuentas, coinciden, no_coinciden,
                 solo_argos_cnt, solo_intra_cnt]
})

resumen_estado.to_csv(f"{OUTPUT}/resumen_estado.csv", index=False)
print("📤 Generado: resumen_estado.csv")

print("\n✅ Fase 3 completada: resúmenes generados.\n")

# ============================================================
# 9. EXPORTAR ARCHIVO EXCEL FINAL CONSOLIDADO
# ============================================================

print("📘 Generando archivo Excel final...")

ruta_excel = f"{OUTPUT}/conciliacion_final.xlsx"

with pd.ExcelWriter(ruta_excel, engine="xlsxwriter") as writer:
    resultado.to_excel(writer, sheet_name="Conciliacion", index=False)
    solo_argos.to_excel(writer, sheet_name="Solo_ARGOS", index=False)
    solo_intra.to_excel(writer, sheet_name="Solo_INTRANET", index=False)
    diferencias.to_excel(writer, sheet_name="Diferencias", index=False)
    resumen_totales.to_excel(writer, sheet_name="Resumen_Totales", index=False)
    resumen_por_grupo.to_excel(writer, sheet_name="Resumen_Grupo", index=False)
    resumen_estado.to_excel(writer, sheet_name="Estado", index=False)

print(f"📤 Archivo Excel generado: conciliacion_final.xlsx")
print("\n🎉 FASE 4 COMPLETADA: Informe final listo.\n")

# --------------------------------------------------------------
# FASE 4: VALIDACIONES FINALES Y GENERACIÓN DE REPORTES
# --------------------------------------------------------------

import pandas as pd
import numpy as np
from datetime import datetime
import os

print("\n=== FASE 4: Validaciones finales y reportes automáticos ===")

# --------------------------------------------------------------
# ⚠️ IMPORTANTE: AJUSTA ESTA LÍNEA
# Reemplaza 'df_conciliado' por EL NOMBRE REAL de tu DataFrame final.
# --------------------------------------------------------------

df = resultado   # ✔️ Este SÍ existe en tu código

# ==============================================================
# VALIDACIONES
# ==============================================================

# 1. VALIDACIÓN DE DUPLICADOS
duplicados = df[df.duplicated()]
num_duplicados = len(duplicados)

print(f"→ Registros duplicados detectados: {num_duplicados}")

# 2. VALIDACIÓN DE CAMPOS CRÍTICOS VACÍOS
columnas_criticas = ["codigo", "descripcion", "categoria"]
columnas_presentes = [c for c in columnas_criticas if c in df.columns]

faltantes = df[df[columnas_presentes].isnull().any(axis=1)]
num_faltantes = len(faltantes)

print(f"→ Registros con datos críticos faltantes: {num_faltantes}")

# 3. EXPORTACIÓN AUTOMÁTICA
os.makedirs("salidas", exist_ok=True)

df.to_excel("salidas/datos_limpios_final.xlsx", index=False)
print("✔ Archivo final exportado: datos_limpios_final.xlsx")

if num_duplicados > 0:
    duplicados.to_excel("salidas/registros_duplicados.xlsx", index=False)
    print("✔ Se exportó archivo con duplicados")

if num_faltantes > 0:
    faltantes.to_excel("salidas/registros_con_campos_faltantes.xlsx", index=False)
    print("✔ Se exportó archivo con registros incompletos")

# 4. REPORTE TXT DE EJECUCIÓN
reporte = f"""
REPORTE DE PROCESAMIENTO – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total de registros finales: {len(df)}

Registros duplicados: {num_duplicados}
Registros con campos faltantes críticos: {num_faltantes}

Archivos generados:
- datos_limpios_final.xlsx
- registros_duplicados.xlsx (si aplica)
- registros_con_campos_faltantes.xlsx (si aplica)

Ejecución completada correctamente.
"""

with open("salidas/reporte_proceso.txt", "w", encoding="utf-8") as f:
    f.write(reporte)

print("✔ Reporte TXT generado")
print("\n=== FASE 4 FINALIZADA ===")
