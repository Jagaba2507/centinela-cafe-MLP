# Proyecto Centinela del Café · Fase 1

Sistema de alerta temprana de roya (*Hemileia vastatrix*) en hojas de café robusta, desarrollado para el curso Profundización I: Redes Neuronales — Deep Learning (EA-N-F-004), Maestría en Ciencia de Datos, Universidad Santo Tomás.

## Cliente y problema

Técnicos de extensión rural que acompañan a pequeños productores de café robusta. El sistema indica si una hoja tiene roya (sí/no) para priorizar las visitas de campo y evitar aplicaciones innecesarias de fungicida.

## Fases

1. **Análisis visual (Fase 1):** perceptrón multicapa (MLP) sobre rasgos de color extraídos de las imágenes de hojas.
2. **Modelo integral (Fase 2):** red convolucional para la imagen y red recurrente para la serie climática, fusionadas para emitir alertas tempranas.

## Fuentes de datos

| Modalidad | Fuente | Licencia |
| --- | --- | --- |
| Imagen | RoCoLe v2, Mendeley Data, https://doi.org/10.17632/c5yvn32dzg.2 | CC BY 4.0 |
| Serie temporal | NASA POWER, https://power.larc.nasa.gov/ | Datos NASA de libre uso |

Los datos no se versionan en el repositorio: el cuaderno los descarga desde la fuente primaria.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `propuesta-de-datos-fase1.md` | Propuesta de Datos (v1), con la plantilla del curso y sus anexos A, B y C |
| `00_prueba_acoplamiento.ipynb` | Descarga de las fuentes, huellas SHA-256, huella de crudeza y prueba de acoplamiento de diez filas |
| `scripts/descargar_datos.py` | Descarga RoCoLe y NASA POWER desde su productor primario |
| `bitacora_ia/bitacora-ia-fase1.md` | Bitácora de IA y auditoría a la IA |
| `informe/` | Informe técnico-ético en PDF (máximo 4 páginas) |
| `requirements.txt` | Dependencias del proyecto |

## Cómo reproducir

1. Abrir `00_prueba_acoplamiento.ipynb` en Google Colab y ejecutar «Ejecutar todo», o correr `python scripts/descargar_datos.py`.
2. Los datos se guardan en `datos/`, carpeta excluida del repositorio.

## Reconocimiento

The data was obtained from the National Aeronautics and Space Administration (NASA) Langley Research Center (LaRC) Prediction of Worldwide Energy Resource (POWER) Project funded through the NASA Earth Science/Applied Science Program.

Imágenes: Parraga-Alava, J., Cusme, K., Loor, A. y Santander, E. (2019). RoCoLe: A robusta coffee leaf images dataset (Versión 2). Mendeley Data. Características tabulares derivadas de RoCoLe.
