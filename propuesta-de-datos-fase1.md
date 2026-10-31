# Propuesta de Datos · Proyecto Centinela · Fase 1

Una página de texto (secciones 0 a 8) más tres anexos que no cuentan en la extensión: A. prueba de acoplamiento; B. evidencias del test de procedencia; C. checklist de protección de datos (uno por fuente).

## 0. Encabezado

| Campo | Detalle |
| --- | --- |
| Título del proyecto | Centinela del Café: alerta temprana de roya en hojas de café robusta |
| Integrantes | |
| Fecha | 2026-10-31 |
| Versión | v1 en la Fase 1 |

## 1. Problema, cliente y objetivo binario

- **Evento de riesgo y cliente:** presencia de roya (*Hemileia vastatrix*) en hojas de café. El cliente son los técnicos de extensión rural que acompañan a pequeños productores de café robusta.
- **Impacto:** una roya detectada tarde reduce la cosecha, mientras que una falsa alarma lleva al productor a gastar en fungicidas que no necesita.
- **Objetivo binario:** «hoja con roya: sí/no». La clase positiva agrupa los cuatro niveles de severidad de la escala OIRSA (1–5 %, 6–20 %, 21–50 % y más del 50 % del área afectada); la negativa es «sana». Se agrupan todos los niveles porque omitir el nivel 1 es el error más costoso: es la etapa en la que todavía se puede contener el brote. Se pierde la información ordinal de severidad, que se retoma en la Fase 2. Las 167 imágenes con ácaro rojo se excluyen de la Fase 1, porque corresponden a otra plaga y no a la ausencia de roya.

## 2. Las dos modalidades del sistema completo

- **Rama de imagen:** fotografías de campo del haz y el envés de hojas de café robusta. Se tomaron con la cámara de 5 MP de un teléfono inteligente, a 200–300 mm de distancia. Aportan el color, la textura y la distribución espacial de las pústulas.
- **Rama temporal:** temperatura a 2 m (T2M), humedad relativa a 2 m (RH2M) y precipitación corregida (PRECTOTCORR), con frecuencia diaria y mensual. Provienen de NASA POWER, que combina el reanálisis MERRA-2 con observaciones satelitales en celdas de 0,5° × 0,625°.
- **Pregunta de control, «¿La imagen contiene algo que un número no contenga?»:** sí. La imagen muestra dónde y cuánto daño tiene cada hoja. La serie climática solo describe las condiciones del sitio, iguales para todas las hojas de una misma ventana. Son dos instrumentos físicamente independientes, una cámara y un sistema de reanálisis satelital, y ninguno se deriva del otro.

## 3. Fuentes (con enlaces y licencia)

| Modalidad | Fuente (productor primario) | Enlace o DOI | Licencia y versión | Dónde se verificó la licencia | ¿Datos de personas? |
| --- | --- | --- | --- | --- | --- |
| Imagen | RoCoLe v2 (Parraga-Alava et al., ESPAM MFL; Mendeley Data) | https://doi.org/10.17632/c5yvn32dzg.2 | CC BY 4.0 | Página del conjunto en Mendeley Data, consultada el 2026-10-31 | No (hojas de café) |
| Temporal | NASA POWER (NASA Langley Research Center) | https://power.larc.nasa.gov/ | Datos NASA de libre uso, con reconocimiento solicitado | Documentación de la fuente, consultada el 2026-10-31 | No |

## 4. Por qué NO es un reto resuelto

El dato es crudo: RoCoLe entrega fotografías de campo con fondo e iluminación variables, clases desbalanceadas y una etiqueta ordinal, sin partición ni rasgos tabulares. Tampoco trae fecha ni ubicación por imagen, así que el cruce con el clima debe construirse y declararse. La búsqueda de espejos del 2026-10-31 no encontró una réplica en kaggle.com; sí existen copias fuera de Kaggle (Roboflow Universe, Dataset Ninja), que no se usan, porque la descarga se hace desde el DOI de Mendeley.

Hay trabajos públicos que clasifican RoCoLe con redes convolucionales, pero ninguno resuelve el problema de esta propuesta. Aquí el reto es elegir un umbral según el costo de cada error para el pequeño productor. En la Fase 2, además, se fusiona la hoja con el clima previo. Las evidencias están en el anexo B.

## 5. Plan de la Fase 1, clave de alineación y prueba de acoplamiento

- **Modalidad que se modela en la Fase 1 (aplanada a tabla):** la imagen, resumida por hoja en rasgos de color: media y desviación de los canales R, G y B y de H, S y V, más la proporción de píxeles en el rango amarillo-naranja de las pústulas.
- **Paso a la Fase 2:** una CNN procesa la imagen completa y una LSTM o GRU procesa la serie diaria de NASA POWER; ambas ramas se fusionan para emitir la alerta.
- **Clave de alineación (se marca una):**
  - [x] Agregada: (sitio, ventana de colecta) = (CIIDEA–ESPAM MFL, Calceta, Manabí, Ecuador; lat −0,8342, lon −80,1772; 2018-05 a 2019-04). Los autores no publican la fecha de cada imagen; la ventana se asume como los doce meses previos a la publicación del conjunto (2019-05-17) y se contrasta con los metadatos EXIF de las fotografías. **Salvedad:** todas las imágenes heredan el mismo vector climático. En la Fase 1 ese vector no discrimina entre clases, y en la Fase 2 limita lo que la fusión puede aprender. Para evitar fuga, la partición se agrupa por planta (cuatro imágenes por planta), de modo que una misma planta no quede en entrenamiento y en prueba.
  - [ ] Por muestra: solo se activa si los metadatos EXIF traen la fecha de toma; en ese caso, la clave pasa a ser (sitio, semana).
- **Prueba de acoplamiento (obligatoria):** diez filas reales en el anexo A.

## 6. Línea base comprometida

- **Clase mayoritaria:** se reporta la exactitud y el *recall* de la clase «con roya» en el conjunto de prueba. Con los conteos publicados (791 sanas y 602 con roya), la clase mayoritaria es «sana», con una exactitud esperada cercana a 0,57 y un *recall* de 0.
- **Escalar crudo:** la modalidad aplanada es un vector de rasgos, no un escalar. Como referencia adicional, se reporta la proporción de píxeles amarillo-naranja usada sola, con un umbral elegido en validación.
- La partición, la semilla y estas cifras se conservan: son el punto de comparación de la Fase 2.

## 7. Riesgos éticos y protección de datos

| Riesgo | Daño para el cliente | Mitigación |
| --- | --- | --- |
| Sesgo de muestreo o representatividad | Todas las hojas vienen de un solo sitio en Ecuador, de café robusta y con una sola cámara. En Colombia predomina el café arábica, así que el modelo podría fallar en fincas colombianas. | Declarar el alcance en el informe, reportar el error por nivel de severidad y no recomendar su uso en arábica sin validarlo con imágenes locales. |
| Falsa alarma | El productor aplica fungicida sin necesidad, con costo económico y ambiental. | La alerta pide una verificación en campo del técnico antes de aplicar, y el umbral se ajusta en validación según el costo de cada error. |
| Alarma omitida | La roya avanza sin control y reduce la cosecha. | Priorizar el *recall* de la clase «con roya» al elegir el umbral en validación y reportar aparte el *recall* del nivel 1. |

El checklist de protección de datos va en el anexo C, uno por fuente.

## 8. Cita APA 7 de cada fuente

- Parraga-Alava, J., Cusme, K., Loor, A. y Santander, E. (2019). *RoCoLe: A robusta coffee leaf images dataset* (Versión 2) [Conjunto de datos]. Mendeley Data. https://doi.org/10.17632/c5yvn32dzg.2
- Parraga-Alava, J., Cusme, K., Loor, A. y Santander, E. (2019). RoCoLe: A robusta coffee leaf images dataset for evaluation of machine learning based methods in plant diseases recognition. *Data in Brief, 25*, 104414. https://doi.org/10.1016/j.dib.2019.104414
- NASA Langley Research Center. (2026). *Prediction of Worldwide Energy Resources (POWER) Project* [Conjunto de datos y API]. https://power.larc.nasa.gov/

---

## Anexo A · Prueba de acoplamiento

Clave: (sitio, ventana de colecta) = (CIIDEA–ESPAM MFL, 2018-05 a 2019-04).

> Se completa al ejecutar `00_prueba_acoplamiento.ipynb`, que imprime esta tabla con datos reales.

| N.º | Clave | Dato de la rama de imagen (archivo o rasgo) | Dato de la serie (variable y valor) |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

Código o consulta que produjo las filas: celda «Anexo A» del cuaderno `00_prueba_acoplamiento.ipynb`, con la consulta a la API mensual de NASA POWER (`/api/temporal/monthly/point`, parámetros T2M, RH2M y PRECTOTCORR, comunidad AG).

## Anexo B · Evidencias del test de procedencia

1. **Cadena de procedencia** (un archivo por fila):

| Archivo (nombre exacto) | URL o DOI del productor primario | Fecha de descarga | Huella SHA-256 |
| --- | --- | --- | --- |
| _(lo imprime el cuaderno)_ | https://doi.org/10.17632/c5yvn32dzg.2 | _(AAAA-MM-DD)_ | _(lo imprime el cuaderno)_ |
| `nasa_power_ciidea_mensual.csv` | https://power.larc.nasa.gov/api/temporal/monthly/point | _(AAAA-MM-DD)_ | _(lo imprime el cuaderno)_ |

2. **Descarga trazable:** el cuaderno descarga RoCoLe desde el enlace de Mendeley Data asociado al DOI y el clima desde la API de NASA POWER. La búsqueda `grep -inE "kaggle|kagglehub|/kaggle/input" *.ipynb` se ejecuta sobre el cuaderno entregado y no debe devolver coincidencias.
3. **Búsqueda declarada de espejos** (2026-10-31): sin coincidencias en kaggle.com para «RoCoLe». Copias fuera de Kaggle identificadas y no usadas: https://universe.roboflow.com/coffee-leaf-detection/rocole-xot5m y https://datasetninja.com/rocole.
4. **Huella de crudeza** (antes de limpiar): filas × columnas _(lo imprime el cuaderno)_ · faltantes _(… %)_ · balance de la etiqueta: 791 sanas, 344 roya nivel 1, 166 nivel 2, 62 nivel 3, 30 nivel 4 y 167 ácaro rojo (conteos publicados por los autores; el cuaderno los confirma).
5. **Contraste con el espejo:** no aplica, porque no se encontró una réplica en Kaggle.

## Anexo C · Checklist de protección de datos personales (uno por fuente)

### Fuente: RoCoLe v2 (Mendeley Data)

**Resultado:** [x] Sin datos de personas.

- **A. Datos personales:** [x] Se revisaron columnas, imágenes y metadatos: las imágenes muestran hojas, sin rostros ni identificadores. [x] Se revisan los metadatos EXIF/GPS en el cuaderno. [x] No hay identificadores seudonimizados de personas.
- **B. Datos sensibles:** [x] No hay datos de salud humana, biométricos ni otros datos sensibles.
- **C. Niños, niñas o adolescentes:** [x] No aplica.
- **D. Base legal:** [x] Fuente pública con licencia CC BY 4.0; se citan sus términos.
- **E. Finalidad:** [x] «Uso académico para entrenar y evaluar un modelo en el curso; no se toman decisiones sobre personas identificadas».
- **F. Anonimización:** [x] Se borran los metadatos EXIF/GPS antes de subir imágenes a Colab, Drive o GitHub. [x] Prueba de reidentificación: el único dato de ubicación es el de un centro de investigación público, no el de una persona.
- **G. Licencia:** [x] CC BY 4.0, verificada en la página del conjunto en Mendeley Data. [x] Obligación BY: atribuir e indicar los cambios («características tabulares derivadas de RoCoLe»).
- **H. Transferencia internacional:** [x] Colab, Drive y GitHub procesan los datos fuera de Colombia; solo se suben datos sin personas. [x] A los asistentes de IA no se les pegan registros reales, solo el esquema.
- **I. Minimización y conservación:** [x] Se conservan las imágenes y las etiquetas necesarias. [x] Los datos crudos se guardan en Drive y se borran al terminar la Fase 3.
- **J. Repositorio:** [x] La carpeta de datos va en `.gitignore` y el repositorio trae el script de descarga desde el DOI.

### Fuente: NASA POWER

**Resultado:** [x] Sin datos de personas.

- **A. Datos personales:** [x] Series meteorológicas por coordenadas, sin identificadores de personas.
- **B. Datos sensibles:** [x] No aplica.
- **C. Niños, niñas o adolescentes:** [x] No aplica.
- **D. Base legal:** [x] Datos públicos de la NASA, de libre uso; se incluye el reconocimiento que solicita la fuente.
- **E. Finalidad:** [x] «Uso académico para entrenar y evaluar un modelo en el curso; no se toman decisiones sobre personas identificadas».
- **F. Anonimización:** [x] No aplica: la coordenada corresponde a un centro de investigación, no a una persona.
- **G. Licencia:** [x] Datos NASA de libre uso, verificado en la documentación de la fuente. [x] Reconocimiento: «The data was obtained from the National Aeronautics and Space Administration (NASA) Langley Research Center (LaRC) Prediction of Worldwide Energy Resource (POWER) Project funded through the NASA Earth Science/Applied Science Program».
- **H. Transferencia internacional:** [x] Solo se suben datos sin personas.
- **I. Minimización y conservación:** [x] Solo se descargan T2M, RH2M y PRECTOTCORR para el sitio y la ventana declarados.
- **J. Repositorio:** [x] El CSV puede redistribuirse; aun así, el cuaderno lo regenera desde la API.

**Declaración.** Lo consignado en este checklist es verdadero y se revisó para cada fuente de la Propuesta.

| Integrante | Firma | Fecha (AAAA-MM-DD) |
| --- | --- | --- |
| | | |
| | | |
| | | |
