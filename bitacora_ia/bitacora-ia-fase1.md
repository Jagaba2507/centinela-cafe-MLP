# Bitácora de IA · Proyecto Centinela del Café · Fase 1

Registro de cada interacción relevante con asistentes de IA: qué se pidió, qué devolvió la IA y qué se decidió (Aceptada, Modificada o Rechazada), con su justificación, su fecha y la sección del cuaderno o de la Propuesta que afecta.

A los asistentes de IA no se les entregan registros reales con datos personales: solo el esquema o filas sintéticas.

| N.º | Fecha (AAAA-MM-DD) | Herramienta | Qué se pidió | Qué devolvió la IA | Decisión | Justificación y cómo se verificó | Sección afectada | Integrante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-31 | Claude | Comparar Copernicus (Sentinel-1/2) frente a RoCoLe + NASA POWER como fuentes del proyecto. | Recomendó RoCoLe + NASA POWER: Copernicus no trae etiquetas del evento de riesgo y exige un preprocesamiento pesado. | _(Aceptada / Modificada / Rechazada)_ | _(…)_ | Propuesta, sección 3 | |
| 2 | 2026-10-31 | Claude | Verificar el sitio y las fechas de colecta de RoCoLe. | Según el artículo de datos, todas las imágenes vienen de un solo sitio (CIIDEA, Calceta, Ecuador) y no tienen fecha por imagen. | _(…)_ | _(contrastar con el artículo: Parraga-Alava et al., 2019)_ | Propuesta, sección 5 | |
| 3 | 2026-10-31 | Claude | Diligenciar la Propuesta de Datos con la plantilla del curso. | Borrador de las secciones 0 a 8 y de los anexos A, B y C. Propuso excluir el ácaro rojo y agrupar los cuatro niveles de roya como clase positiva. | _(…)_ | _(…)_ | Propuesta, secciones 1 y 6 | |
| 4 | 2026-10-31 | Claude | Escribir la celda de descarga de RoCoLe en `00_prueba_acoplamiento.ipynb`. | Usó una URL de descarga directa en Amazon S3 que no está publicada en la página del DOI. Al ejecutar, el servidor respondió «403 Forbidden». | Rechazada | La URL no estaba documentada por Mendeley Data. Se reemplazó por la API pública de Mendeley Data, con la descarga manual del .zip como respaldo. | Cuaderno, sección 1 | |

## Auditoría a la IA

Se documenta al menos un fallo real de la IA en el propio proyecto: salida literal (o captura con fecha y herramienta), ubicación en el cuaderno, corrección y fundamento.

| Campo | Detalle |
| --- | --- |
| Fallo de la IA | La IA (Claude, 2026-10-31) propuso descargar RoCoLe desde `https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/c5yvn32dzg-2.zip`, una URL que no aparece en la página del DOI. |
| Evidencia de origen | Salida literal al ejecutar el cuaderno en VS Code: `HTTPError: 403 Client Error: Forbidden for url: https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/c5yvn32dzg-2.zip` |
| Celda o sección afectada | `00_prueba_acoplamiento.ipynb`, sección 1 (descarga de RoCoLe) |
| Corrección | Descarga con la API pública de Mendeley Data (`/public-api/datasets/c5yvn32dzg/files`) y, como respaldo, el .zip de «Download All» guardado a mano en `datos/`. |
| Fundamento y medición | El test de procedencia exige que la descarga salga del productor primario y sea trazable: una URL no documentada no cumple esa condición. _(Para el nivel Estratégico, la auditoría debe reproducirse con un fallo que afecte una métrica de decisión del modelo; este caso cubre el nivel Autónomo.)_ |

## Declaración de no uso

_(Solo si un integrante no usó IA.)_
