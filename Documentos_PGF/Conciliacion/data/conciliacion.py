"""
conciliacion.py
Script para conciliar transacciones: Argos (Egreper.csv) vs Intranet (Excel).
Genera un Excel con reportes y una gráfica PNG con montos faltantes en Argos por mes.

Requisitos:
 pip install pandas openpyxl matplotlib

Uso:
 Coloca 'Egreper.csv', 'Ejecxcuentas.csv' y el Excel de intranet
 'Organizacion_intranet.xlsx' en la misma carpeta
 y ejecuta:
 python conciliacion.py
"""
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import re
import os

# ---------- UTILIDADES ----------
def parse_amount_chilean(x):
    """Parsea montos tipo $11.130 o 1.234.567 o -44,500 etc. Retorna float o NaN."""
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    s = s.replace('$','').replace('CLP','').replace(' ','').replace('�','')
    # Caso: "1.234.567,89" -> remove '.' thousands, ',' decimal -> -> 1234567.89
    if '.' in s and ',' in s:
        s = s.replace('.','').replace(',','.')
    else:
        # caso "1.234.567" o "1,234,567" -> remove separators
        s = s.replace('.','').replace(',','')
    # keep digits, minus and dot
    s = re.sub(r'[^\d\-.]', '', s)
    if s in ('','-'):
        return np.nan
    try:
        return float(s)
    except:
        return np.nan

def try_parse_date(x):
    """Intento robusto de parseo (día/mes/año preferente)."""
    try:
        return pd.to_datetime(x, dayfirst=True, errors='coerce')
    except:
        return pd.to_datetime(x, errors='coerce')

# ---------- CARGA ----------
eg_path = 'Egreper.csv'
ejec_path = 'Ejecxcuentas.csv'
intranet_path = 'Organizacion_intranet.xlsx'

eg = pd.read_csv(eg_path, engine='python', sep=None)
ejec = pd.read_csv(ejec_path, engine='python', sep=None)
in_raw = pd.read_excel(intranet_path, engine='openpyxl', header=None)

# ---------- LIMPIEZA INTRANET ----------
# Detectar la fila de encabezado (busca 'Sub' y 'Mov' en las primeras filas)
header_row = 1
preview = in_raw.head(8)
for i in range(0,6):
    values = preview.iloc[i].astype(str).str.upper().tolist()
    if any('SUB' in v for v in values) and any('MOV' in v for v in values):
        header_row = i
        break

in_df = in_raw.copy()
in_df.columns = in_df.iloc[header_row].fillna(method='ffill')
in_df = in_df.iloc[header_row+1:].reset_index(drop=True)

# Normalizar nombres de columnas (buscar keywords)
def find_col(df, *keywords):
    for c in df.columns:
        uc = str(c).upper()
        if all(k.upper() in uc for k in keywords):
            return c
    # fallback: primera que contenga alguno
    for c in df.columns:
        uc = str(c).upper()
        if any(k.upper() in uc for k in keywords):
            return c
    return None

col_sub = find_col(in_df, 'SUB')
col_mov = find_col(in_df, 'MOV')
col_ingelo = find_col(in_df, 'ELO')
col_ingesif = find_col(in_df, 'SIF')
col_doc = find_col(in_df, 'DOCUMENTO')
col_ndoc = find_col(in_df, 'N','DOCUMENT')
col_cuenta_desc = find_col(in_df, 'CUENTA')
col_abono = find_col(in_df, 'ABONO')
col_cargo = find_col(in_df, 'CARGO')

in_work = pd.DataFrame({
    'SubOrganizacion': in_df[col_sub] if col_sub is not None else None,
    'N_Movimiento': in_df[col_mov] if col_mov is not None else None,
    'IngresoELO': in_df[col_ingelo] if col_ingelo is not None else None,
    'IngresoSIF': in_df[col_ingesif] if col_ingesif is not None else None,
    'Documento': in_df[col_doc] if col_doc is not None else None,
    'N_Documento': in_df[col_ndoc] if col_ndoc is not None else None,
    'CuentaDescripcion': in_df[col_cuenta_desc] if col_cuenta_desc is not None else None,
    'Abono_raw': in_df[col_abono] if col_abono is not None else None,
    'Cargo_raw': in_df[col_cargo] if col_cargo is not None else None
})

# fechas
in_work['Fecha'] = in_work['IngresoELO'].combine_first(in_work['IngresoSIF']).apply(try_parse_date)

# montos
in_work['Cargo'] = in_work['Cargo_raw'].apply(parse_amount_chilean)
in_work['Abono'] = in_work['Abono_raw'].apply(parse_amount_chilean)
# definimos monto firmado: Cargo = gasto -> negativo; Abono = ingreso -> positivo
in_work['Monto'] = in_work['Abono'].fillna(0) - in_work['Cargo'].fillna(0)
in_work['Monto_abs'] = in_work['Monto'].abs()
in_work['Origen'] = 'Intranet'

# ---------- LIMPIEZA ARGOS ----------
# detectar columna monto y fecha
monto_col = None
for c in eg.columns:
    if 'MON' in str(c).upper() or 'IMP' in str(c).upper():
        monto_col = c
        break
if monto_col is None:
    raise SystemExit("No pude detectar columna monto en Egreper.csv")

eg['Monto_parsed'] = eg[monto_col].apply(parse_amount_chilean)
# fecha
date_col = None
for c in eg.columns:
    if 'FECHA' in str(c).upper():
        date_col = c
        break
eg['Fecha'] = eg[date_col] if date_col is not None else None
eg['Fecha'] = eg['Fecha'].apply(try_parse_date)
# cod cuenta detection
cod_cuenta = None
for c in eg.columns:
    if 'COD' in str(c).upper() and 'CUEN' in str(c).upper():
        cod_cuenta = c
        break
if cod_cuenta is None:
    # fallback try exact names
    if 'Cod Cuenta' in eg.columns:
        cod_cuenta = 'Cod Cuenta'
eg['CodCuenta'] = eg[cod_cuenta] if cod_cuenta is not None else np.nan

eg['Monto_abs'] = eg['Monto_parsed'].abs()
eg['Origen'] = 'Argos'

# keep
arg_df = eg[['Fecha','Documento','Folio','Glosa','Monto_parsed','RUT','Nombre','CodCuenta','Monto_abs','Origen']].rename(columns={'Monto_parsed':'Monto'})

# ---------- MATCHING (algoritmo greedy) ----------
intr = in_work.reset_index().rename(columns={'index':'idx'})
arg = arg_df.reset_index().rename(columns={'index':'idx'})

intr['matched'] = False
arg['matched'] = False

matches = []
for i,row in intr.iterrows():
    if pd.isna(row['Monto']) or row['Monto_abs']==0:
        continue
    # candidates same abs
    cand = arg[(~arg['matched']) & (arg['Monto_abs']==row['Monto_abs'])]
    # small tolerance if none found
    if cand.empty:
        tol = 1.0
        cand = arg[(~arg['matched']) & (arg['Monto_abs'].between(row['Monto_abs']-tol, row['Monto_abs']+tol))]
    if cand.empty:
        continue
    # prefer date proximity
    if not pd.isna(row['Fecha']):
        cand = cand.copy()
        cand['date_diff'] = cand['Fecha'].apply(lambda d: abs((d - row['Fecha']).days) if pd.notna(d) else 9999)
        cand = cand.sort_values('date_diff')
        chosen_idx = cand.index[0]
    else:
        chosen_idx = cand.index[0]
    matches.append({
        'intr_idx': int(row['idx']),
        'intr_fecha': row['Fecha'],
        'intr_cuenta': row['CuentaDescripcion'],
        'intr_monto': row['Monto'],
        'arg_idx': int(arg.loc[chosen_idx,'idx']),
        'arg_fecha': arg.loc[chosen_idx,'Fecha'],
        'arg_codcuenta': arg.loc[chosen_idx,'CodCuenta'],
        'arg_monto': arg.loc[chosen_idx,'Monto']
    })
    intr.at[i,'matched'] = True
    arg.at[chosen_idx,'matched'] = True

matches_df = pd.DataFrame(matches)
intr_missing = intr[~intr['matched']].copy()
arg_missing = arg[~arg['matched']].copy()

# detectar compensaciones en Argos (monto opuesto, misma abs, misma codcuenta opcional)
comp_pairs = []
arg_un = arg.copy().reset_index(drop=True)
used = set()
for i,row in arg_un.iterrows():
    if i in used:
        continue
    cand = arg_un[(arg_un['Monto_abs']==row['Monto_abs']) & (arg_un['Monto']== -row['Monto']) & (~arg_un.index.isin(used))]
    if not cand.empty:
        # intentar por CodCuenta
        if 'CodCuenta' in arg_un.columns and pd.notna(row.get('CodCuenta',np.nan)):
            cand2 = cand[cand['CodCuenta']==row['CodCuenta']]
            if not cand2.empty:
                cand = cand2
        # elegir por cercanía de fecha
        cand = cand.copy()
        cand['date_diff'] = cand['Fecha'].apply(lambda d: abs((d - row['Fecha']).days) if pd.notna(d) else 9999)
        chosen = cand.sort_values('date_diff').iloc[0]
        comp_pairs.append({
            'idx1': int(row['idx']),
            'fecha1': row['Fecha'],
            'monto1': row['Monto'],
            'idx2': int(chosen['idx']),
            'fecha2': chosen['Fecha'],
            'monto2': chosen['Monto'],
            'CodCuenta': row.get('CodCuenta', np.nan)
        })
        used.add(i)
        used.add(int(chosen['idx']))

comp_df = pd.DataFrame(comp_pairs)

# ---------- RESUMEN Y SALIDA ----------
summary = {
    'total_intr_amount': in_work['Monto'].sum(),
    'total_arg_amount': arg_df['Monto'].sum(),
    'total_missing_in_arg': intr_missing['Monto'].sum(),
    'total_missing_in_intranet': arg_missing['Monto'].sum(),
    'n_intr_records': len(intr),
    'n_arg_records': len(arg),
    'n_matches': len(matches_df),
    'n_intr_missing': len(intr_missing),
    'n_arg_missing': len(arg_missing),
    'n_comp_pairs': len(comp_df)
}

out_xlsx = 'conciliacion_result.xlsx'
with pd.ExcelWriter(out_xlsx, engine='openpyxl') as writer:
    in_work.to_excel(writer, sheet_name='Intranet_Clean', index=False)
    arg_df.to_excel(writer, sheet_name='Argos_Clean', index=False)
    matches_df.to_excel(writer, sheet_name='Matches', index=False)
    intr_missing.to_excel(writer, sheet_name='Intranet_only', index=False)
    arg_missing.to_excel(writer, sheet_name='Argos_only', index=False)
    comp_df.to_excel(writer, sheet_name='Argos_compensations', index=False)
    pd.DataFrame([summary]).to_excel(writer, sheet_name='Summary', index=False)

# gráfica: montos faltantes en Argos (intranet_only) por mes
png_out = 'missing_in_argos_by_month.png'
if not intr_missing.empty:
    intr_missing['Fecha'] = pd.to_datetime(intr_missing['Fecha'], errors='coerce')
    intr_missing['Mes'] = intr_missing['Fecha'].dt.to_period('M').astype(str)
    monthly = intr_missing.groupby('Mes')['Monto'].sum().sort_index()
    plt.figure(figsize=(8,4))
    monthly.plot(kind='bar')
    plt.title('Montos faltantes en Argos según Intranet (por mes)')
    plt.ylabel('Monto (CLP)')
    plt.tight_layout()
    plt.savefig(png_out)
    plt.close()
else:
    # gráfico simple indicando 0
    plt.figure(figsize=(6,3))
    plt.text(0.5,0.5,'No missing records found (según criterio actual)', ha='center')
    plt.axis('off')
    plt.savefig(png_out)
    plt.close()

print("Terminado. Archivos generados:")
print(" -", out_xlsx)
print(" -", png_out)
print("Resumen:", summary)
