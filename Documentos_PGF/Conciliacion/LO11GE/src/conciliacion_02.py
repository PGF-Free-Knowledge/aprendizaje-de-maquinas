#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
conciliacion.py
-----------------------------------------
Lee los datos limpios:
 - Ejecxcuentas_LEIDO.csv
 - Egreper_LEIDO.csv
 - Organizacion_intranet_limpio.csv

Y prepara la estructura para realizar la conciliación completa.

Autor: Paul Richard Gálvez Fernández
"""

import os
import pandas as pd

# -----------------------------
# RUTAS
# -----------------------------
BASE_DIR = "/workspaces/aprendizaje-de-maquinas/Documentos_PGF/Conciliacion/LO11GE"

DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

ARCHIVO_EJEC = os.path.join(DATA_DIR, "Ejecxcuentas_LEIDO.csv")
ARCHIVO_EGRE = os.path.join(DATA_DIR, "Egreper_LEIDO.csv")
ARCHIVO_INTR = os.path.join(DATA_DIR, "Organizacion_intranet_limpio.csv")

# Crear carpeta output si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# FUNCIONES
# -----------------------------
def leer_archivo(path, nombre):
    """Lee un CSV y reporta errores si existen."""
    print(f"📂 Leyendo {nombre} ...")
    try:
        df = pd.read_csv(path, dtype=str)
        print(f"   ✔️ OK ({len(df)} filas)")
        return df
    except Exception as e:
        print(f"   ❌ ERROR leyendo {nombre}: {e}")
        return None


def guardar(df, nombre):
    """Guarda un dataframe en output."""
    salida = os.path.join(OUTPUT_DIR, nombre)
    df.to_csv(salida, index=False, encoding="utf-8")
    print(f"📤 Archivo generado → {salida}")


# -----------------------------
# LECTURA DE LOS TRES ARCHIVOS
# -----------------------------
df_ejec = leer_archivo(ARCHIVO_EJEC, "Ejecxcuentas_LEIDO.csv")
df_egre = leer_archivo(ARCHIVO_EGRE, "Egreper_LEIDO.csv")
df_intr = leer_archivo(ARCHIVO_INTR, "Organizacion_intranet_limpio.csv")

if df_ejec is None or df_egre is None or df_intr is None:
    print("❌ No se pueden continuar los análisis por errores de lectura.")
    exit(1)

# -----------------------------
# NORMALIZACIÓN BÁSICA
# -----------------------------
print("\n🔧 Normalizando columnas clave...")

# Convertir a mayúsculas columnas importantes si existen
for df in [df_ejec, df_egre, df_intr]:
    for columna in ["codigo", "cuenta", "glosa", "descripcion"]:
        if columna in df.columns:
            df[columna] = df[columna].astype(str).str.upper().str.strip()

print("   ✔️ Normalización básica completada.")

# -----------------------------
# ESTRUCTURA DE CRUCES
# -----------------------------
print("\n🔍 Preparando cruces iniciales...")

# Cruce 1: Ejecxcuentas vs Egreper (Argos vs Argos)
cruce_argos = None
if "codigo" in df_ejec.columns and "codigo" in df_egre.columns:
    cruce_argos = df_ejec.merge(
        df_egre,
        on="codigo",
        how="outer",
        suffixes=("_ejec", "_egre"),
        indicator=True
    )
    guardar(cruce_argos, "cruce_argos.csv")

# Cruce 2: Argos unificado vs Intranet
if "codigo" in df_intr.columns and "codigo" in df_ejec.columns:
    df_argos = pd.concat([df_ejec, df_egre], ignore_index=True)
    cruce_intranet = df_argos.merge(
        df_intr,
        on="codigo",
        how="outer",
        suffixes=("_argos", "_intr"),
        indicator=True
    )
    guardar(cruce_intranet, "cruce_intranet.csv")

print("\n🏁 Proceso inicial de conciliación completado.")
print("Ahora podemos continuar con reglas más finas según tu necesidad.")
###### 
