# 🧩 Proyecto: Análisis de Instrumentos ELO

Este documento presenta un resumen técnico y operativo del análisis realizado sobre los instrumentos del laboratorio ELO.  
El propósito es documentar **resultados, procesos y herramientas** utilizadas, en un formato legible y navegable dentro de GitHub.

---

## 📍 **1. Introducción**

El presente repositorio forma parte del trabajo de análisis de datos y optimización del inventario de instrumentos del **Departamento de Electrónica - UTFSM**.  
Se emplean herramientas de análisis basadas en **Python (Pandas, Matplotlib)** dentro de entornos **Jupyter Notebooks**.

> 📎 **Repositorio principal:** [PGF-Free-Knowledge/aprendizaje-de-maquinas](https://github.com/PGF-Free-Knowledge/aprendizaje-de-maquinas)

---

## ⚙️ **2. Archivos principales**

| Archivo | Descripción | Formato |
|----------|--------------|----------|
| `analisis_instrumentos.ipynb` | Notebook principal con análisis de datos, agrupaciones y gráficos | Jupyter Notebook |
| `Control_Instrumentos_ELO_06_combinado.csv` | Base de datos de instrumentos (inventario consolidado) | CSV |
| `grafico_estado_instrumentos.png` | Gráfico de distribución por estado operativo | Imagen PNG |
| `README.md` | Documento de documentación general (este archivo) | Markdown |

---

## 🔍 **3. Estructura de datos**

Los campos principales utilizados en el análisis son los siguientes:

- **Descripción del Activo Fijo** → Referencia base del instrumento  
- **Marca** → Fabricante o proveedor  
- **Modelo** → Versión o familia del equipo  
- **Instrumento (Especificación)** → Tipo o función del instrumento  
- **Estado del Activo Fijo** → Condición actual (Operativo, Inoperativo, Sin Uso)  
- **Ubicación del Activo Fijo** → Lugar físico o laboratorio donde se encuentra

---

## 📊 **4. Resultados visuales**

Los resultados incluyen:

1. Gráficos de barras con distribución por tipo de instrumento  
2. Gráficos de pastel según estado operativo  
3. Tablas dinámicas que agrupan por descripción, marca y modelo  
4. Totales generales y subtotales resaltados con formato legible  

> 💡 Ejemplo de gráfico generado:
## 🔹 Gráficos de Resultados

### 1. Distribución por Estado
![Distribución por Estado](Instrumentos_ELO/graficos/estados_Tarjeta_de_desarrollo.png)

### 2. Distribución por Marca
![Distribución por Marca](Instrumentos_ELO/graficos/marcas_Tarjeta_de_desarrollo.png)

### 3. Distribución por Modelo
![Distribución por Modelo](Instrumentos_ELO/graficos/modelos_Tarjeta_de_desarrollo.png)

![Distribución por Estado](Documentos_PGF/Instrumentos_ELO/graficos/estados_Tarjeta_de_desarrollo.png)


---

> 
---

## 🧠 **5. Código base**

Los notebooks están desarrollados en **Python 3.12**, utilizando librerías estándar:
```python
import pandas as pd
import matplotlib.pyplot as plt
