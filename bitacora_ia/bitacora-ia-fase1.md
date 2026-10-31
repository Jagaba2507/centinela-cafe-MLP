# Bitácora de IA · Proyecto Centinela del Café · Fase 1

Registro de cada interacción relevante con asistentes de IA (Claude en el chat y Claude Code en VS Code): qué se pidió, qué devolvió la IA y qué se decidió (Aceptada, Modificada o Rechazada), con su justificación, su fecha y la sección del cuaderno o de la Propuesta que afecta.

A los asistentes de IA no se les entregan registros reales con datos personales: solo el esquema o filas sintéticas.

| N.º | Fecha (AAAA-MM-DD) | Herramienta | Qué se pidió | Qué devolvió la IA | Decisión | Justificación y cómo se verificó | Sección afectada | Integrante |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-10-31 | Claude | Comparar Copernicus (Sentinel-1/2) frente a RoCoLe + NASA POWER como fuentes del proyecto. | Recomendó RoCoLe + NASA POWER: Copernicus no trae etiquetas del evento de riesgo y exige un preprocesamiento pesado. | _(Aceptada / Modificada / Rechazada)_ | _(…)_ | Propuesta, sección 3 | |
| 2 | 2026-10-31 | Claude | Verificar el sitio y las fechas de colecta de RoCoLe. | Según el artículo de datos, todas las imágenes vienen de un solo sitio (CIIDEA, Calceta, Ecuador) y no tienen fecha por imagen. | _(…)_ | _(contrastar con el artículo: Parraga-Alava et al., 2019)_ | Propuesta, sección 5 | |
| 3 | 2026-10-31 | Claude | Diligenciar la Propuesta de Datos con la plantilla del curso. | Borrador de las secciones 0 a 8 y de los anexos A, B y C. Propuso excluir el ácaro rojo y agrupar los cuatro niveles de roya como clase positiva. | _(…)_ | _(…)_ | Propuesta, secciones 1 y 6 | |
| 4 | 2026-10-31 | Claude | Escribir la celda de descarga de RoCoLe en `00_prueba_acoplamiento.ipynb`. | Usó una URL de descarga directa en Amazon S3 que no está publicada en la página del DOI. Al ejecutar, el servidor respondió «403 Forbidden». | Rechazada | La URL no estaba documentada por Mendeley Data. Se reemplazó por la API pública de Mendeley Data, con la descarga manual del .zip como respaldo. | Cuaderno, sección 1 | |
| 5 | 2026-10-31 | Claude | Definir la clave de alineación entre RoCoLe y NASA POWER. | Afirmó que RoCoLe no trae fecha por imagen y propuso una clave agregada con una ventana asumida (2018-05 a 2019-04). Al ejecutar el cuaderno, las 1.560 fotos traen fecha EXIF del 2019-04-09 al 2019-05-02, fuera de casi toda la ventana asumida. | Modificada | La evidencia del EXIF contradice el supuesto. La clave pasa a ser por muestra (sitio, día de toma), con clima diario de NASA POWER. | Propuesta, sección 5; cuaderno, secciones 3, 4b y 5 | |
| 6 | 2026-10-31 | Claude Code (VS Code) | Revisar y ejecutar `00_prueba_acoplamiento.ipynb`. | Detectó que la selección automática de la columna de etiqueta tomaba la primera que coincidía, `Binary.Label` (sana/no sana), en lugar de `Multiclass.Label`. Cambió el criterio para preferir la columna con más categorías (máximo 20). | Aceptada | Con `Binary.Label` el anexo B no podía reportar los conteos por nivel de roya y ácaro rojo, que también definen la línea base. Se verificó con la salida: 791 / 344 / 167 / 166 / 62 / 30. | Cuaderno, sección 2 | |
| 7 | 2026-10-31 | Claude Code (VS Code) | Revisar la lectura de metadatos EXIF. | Corrigió tres fallos de la versión escrita por Claude: priorizaba `DateTime` (fecha de modificación) sobre `DateTimeOriginal` (fecha de toma); revisaba solo las primeras 200 imágenes; y no cerraba los archivos abiertos. | Aceptada | La clave de alineación depende de la fecha de toma, y el anexo C declara que se revisaron las 1.560 imágenes. Se verificó con la salida: 1.560 con fecha EXIF y 0 con GPS. | Cuaderno, sección 3 | |
| 8 | 2026-10-31 | Claude Code (VS Code) | Revisar la descarga y la extracción de RoCoLe. | Evitó extraer de nuevo el .zip de 2.245,6 MB en cada ejecución y registró la ruta y el origen de cada archivo para el anexo B. | Aceptada | Reduce el tiempo de «Ejecutar todo» sin cambiar los datos: la huella SHA-256 de `RoCoLe.zip` es la misma en ambas ejecuciones. | Cuaderno, sección 1 | |
| 9 | 2026-10-31 | Claude Code (VS Code) | Revisar la consulta mensual a NASA POWER. | Agregó un respaldo: si la API no responde, el cuaderno usa el CSV ya descargado de la misma API. | Aceptada | Permite que el cuaderno corra completo sin conexión; la huella del CSV mensual no cambió entre ejecuciones. | Cuaderno, sección 4 | |

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

### Evidencia de las entradas 6 a 9

Las correcciones de Claude Code se ven en el historial del repositorio, al comparar el cuaderno del commit `7e2d743` (versión escrita por Claude) con el del commit `83171e2` (versión revisada por Claude Code), en las secciones 1, 2, 3 y 4.
