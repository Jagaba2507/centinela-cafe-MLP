# Propuesta de Datos · Proyecto Centinela · Fase 1

Una página de texto (secciones 0 a 8) más tres anexos que no cuentan en la extensión: A. prueba de acoplamiento; B. evidencias del test de procedencia; C. checklist de protección de datos (uno por fuente).

## 0. Encabezado

| Campo | Detalle |
| --- | --- |
| Título del proyecto | Centinela del Café: alerta temprana de roya en hojas de café robusta |
| Integrantes | Jaime Andres Garcia Barros, Adrian Felipe Grateron Ramirez, Jhonatan Smith Doncel Murillo|
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

El dato es crudo: RoCoLe entrega fotografías de campo con fondo e iluminación variables, clases desbalanceadas y una etiqueta ordinal, sin partición ni rasgos tabulares. El artículo no publica las fechas de toma, pero las 1.560 fotografías las conservan en sus metadatos EXIF (del 2019-04-09 al 2019-05-02), así que el cruce con el clima debe construirse desde ese metadato. La búsqueda de espejos del 2026-10-31 no encontró una réplica en kaggle.com; sí existen copias fuera de Kaggle (Roboflow Universe, Dataset Ninja), que no se usan, porque la descarga se hace desde el DOI de Mendeley.

Hay trabajos públicos que clasifican RoCoLe con redes convolucionales, pero ninguno resuelve el problema de esta propuesta. Aquí el reto es elegir un umbral según el costo de cada error para el pequeño productor. En la Fase 2, además, se fusiona la hoja con el clima previo. Las evidencias están en el anexo B.

## 5. Plan de la Fase 1, clave de alineación y prueba de acoplamiento

- **Modalidad que se modela en la Fase 1 (aplanada a tabla):** la imagen, resumida por hoja en rasgos de color: media y desviación de los canales R, G y B y de H, S y V, más la proporción de píxeles en el rango amarillo-naranja de las pústulas.
- **Paso a la Fase 2:** una CNN procesa la imagen completa y una LSTM o GRU procesa la serie diaria de NASA POWER de los días previos a cada toma; ambas ramas se fusionan para emitir la alerta.
- **Clave de alineación (se marca una):**
  - [ ] Agregada, p. ej., (región, mes), con su salvedad de fuga de datos y de rasgo casi constante: no se usa, porque las fotografías traen la fecha de toma.
  - [x] Por muestra, p. ej., (finca, semana): llave concreta (entidad + ventana) y fuente fechada y georreferenciada que la habilita: (sitio, día de toma) = (CIIDEA–ESPAM MFL, Calceta, Manabí, Ecuador; lat −0,8342, lon −80,1772; fecha EXIF de cada fotografía). El sitio lo publican los autores y la fecha sale del metadato EXIF de las 1.560 imágenes (del 2019-04-09 al 2019-05-02). Cada imagen se une con el clima diario de NASA POWER de ese día y con la humedad relativa media de los 14 días previos, calculada sin mirar el futuro. Salvedad: todas las imágenes vienen de un solo sitio y de un periodo de 24 días, así que la variabilidad climática es baja y se reporta como límite de la fusión en la Fase 2. Para evitar fuga, la partición se agrupa por planta (390 plantas verificadas en `RoCoLe-classes.xlsx`, cada una con cuatro imágenes —dos del haz (H) y dos del envés (E)— identificadas por el prefijo `C{n}P{m}` del nombre de archivo).
- **Prueba de acoplamiento (obligatoria):** diez filas reales en el anexo A.
- **Si la modalidad aplanada es una serie temporal:** no aplica; la modalidad aplanada es la imagen.

## 6. Línea base comprometida

- **Clase mayoritaria:** exactitud y *recall* de la clase de riesgo en el conjunto de prueba (el *recall* vale 0 cuando la clase mayoritaria es «sin riesgo»). Con los conteos publicados (791 sanas y 602 con roya), la clase mayoritaria es «sana», con una exactitud esperada cercana a 0,57 y un *recall* de 0.
- **Escalar crudo** (solo si la modalidad aplanada resume un escalar): la modalidad aplanada es un vector de rasgos, no un escalar. Como referencia adicional, se reporta la proporción de píxeles amarillo-naranja usada sola, con un umbral elegido en validación.
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

Clave: (sitio, día de toma) = (CIIDEA–ESPAM MFL, fecha EXIF de la fotografía)

| N.º | Clave | Dato de la rama de imagen (archivo o rasgo) | Dato de la serie (variable y valor) |
| --- | --- | --- | --- |
| 1 | (CIIDEA-ESPAM MFL, 2019-04-10) | `C10P7E2.jpg` (rust_level_2) · RGB medio = (110.9, 131.3, 97.0) | T2M = 25.83 °C · RH2M = 81.17 % · PRECTOTCORR = 0.52 mm/día · RH2M 14 d previos = 86.63 % |
| 2 | (CIIDEA-ESPAM MFL, 2019-04-10) | `C7P19E2.jpg` (healthy) · RGB medio = (106.7, 117.1, 85.2) | T2M = 25.83 °C · RH2M = 81.17 % · PRECTOTCORR = 0.52 mm/día · RH2M 14 d previos = 86.63 % |
| 3 | (CIIDEA-ESPAM MFL, 2019-04-10) | `C10P8H1.jpg` (healthy) · RGB medio = (86.1, 118.5, 72.4) | T2M = 25.83 °C · RH2M = 81.17 % · PRECTOTCORR = 0.52 mm/día · RH2M 14 d previos = 86.63 % |
| 4 | (CIIDEA-ESPAM MFL, 2019-05-01) | `C5P39E1.jpg` (healthy) · RGB medio = (103.7, 116.8, 79.2) | T2M = 26.35 °C · RH2M = 85.81 % · PRECTOTCORR = 15.64 mm/día · RH2M 14 d previos = 86.63 % |
| 5 | (CIIDEA-ESPAM MFL, 2019-04-11) | `C3P19H1.jpg` (healthy) · RGB medio = (83.1, 107.0, 42.0) | T2M = 25.59 °C · RH2M = 82.17 % · PRECTOTCORR = 0.08 mm/día · RH2M 14 d previos = 86.22 % |
| 6 | (CIIDEA-ESPAM MFL, 2019-04-11) | `C3P15E2.jpg` (rust_level_2) · RGB medio = (101.0, 120.0, 36.5) | T2M = 25.59 °C · RH2M = 82.17 % · PRECTOTCORR = 0.08 mm/día · RH2M 14 d previos = 86.22 % |
| 7 | (CIIDEA-ESPAM MFL, 2019-04-10) | `C6P22H1.jpg` (healthy) · RGB medio = (91.5, 117.4, 62.3) | T2M = 25.83 °C · RH2M = 81.17 % · PRECTOTCORR = 0.52 mm/día · RH2M 14 d previos = 86.63 % |
| 8 | (CIIDEA-ESPAM MFL, 2019-04-11) | `C11P10H1.jpg` (healthy) · RGB medio = (93.1, 135.0, 62.5) | T2M = 25.59 °C · RH2M = 82.17 % · PRECTOTCORR = 0.08 mm/día · RH2M 14 d previos = 86.22 % |
| 9 | (CIIDEA-ESPAM MFL, 2019-04-11) | `C12P21H1.jpg` (healthy) · RGB medio = (85.5, 147.7, 77.1) | T2M = 25.59 °C · RH2M = 82.17 % · PRECTOTCORR = 0.08 mm/día · RH2M 14 d previos = 86.22 % |
| 10 | (CIIDEA-ESPAM MFL, 2019-04-11) | `C8P17H2.jpg` (rust_level_1) · RGB medio = (111.7, 138.2, 77.1) | T2M = 25.59 °C · RH2M = 82.17 % · PRECTOTCORR = 0.08 mm/día · RH2M 14 d previos = 86.22 % |

Las diez imágenes se eligieron al azar con semilla 42. El valor de RH2M de los 14 días previos coincide en las filas del 2019-04-10 y del 2019-05-01 (86,63 %); se verificó contra `nasa_power_ciidea_diario.csv` y es una coincidencia de los datos.

Código o consulta que produjo las filas: secciones 4b y 5 del cuaderno `00_prueba_acoplamiento.ipynb`, con la consulta a la API diaria de NASA POWER (`/api/temporal/daily/point`, parámetros T2M, RH2M y PRECTOTCORR, comunidad AG).

## Anexo B · Evidencias del test de procedencia

1. **Cadena de procedencia** (un archivo por fila):

| Archivo (nombre exacto) | URL o DOI del productor primario | Fecha de descarga | Huella SHA-256 |
| --- | --- | --- | --- |
| `RoCoLe.zip` | https://doi.org/10.17632/c5yvn32dzg.2 | 2026-10-31 | `31daa765fb0cc27d4b9b897fa6350aacf0087ee5771d3c7599d2ac7041b866ff` |
| `RoCoLe-classes.xlsx` | https://doi.org/10.17632/c5yvn32dzg.2 | 2026-10-31 | `0040a57ffd441bd69ead997309d14c8d7f6fdfc83c5dbdc47805e0bc4da05ef2` |
| `nasa_power_ciidea_mensual.csv` | https://power.larc.nasa.gov/api/temporal/monthly/point | 2026-10-31 | `75982bc2473818310e75bd265a0f0a08c710a724d7d16f9f873221282710cdfc` |
| `nasa_power_ciidea_diario.csv` | https://power.larc.nasa.gov/api/temporal/daily/point | 2026-10-31 | `eabc2fd50a5a85a05cf6996402381fc2b64ad300771b4c55c09d99e4e6afdfbe` |

2. **Descarga trazable:** RoCoLe se descargó desde la página del DOI en Mendeley Data (`RoCoLe.zip`, 2.245,6 MB) y el clima desde la API de NASA POWER; el cuaderno verifica las huellas. La búsqueda `grep -inE "kaggle|kagglehub|/kaggle/input" *.ipynb` se ejecuta sobre el cuaderno entregado y no debe devolver coincidencias.
3. **Búsqueda declarada de espejos** (fecha 2026-10-31): sin coincidencias en kaggle.com para «RoCoLe». Copias fuera de Kaggle identificadas y no usadas: https://universe.roboflow.com/coffee-leaf-detection/rocole-xot5m y https://datasetninja.com/rocole.
4. **Huella de crudeza** (antes de limpiar): `RoCoLe-classes.xlsx`, 1.560 × 3, 0 % de faltantes. Las exportaciones originales de Labelbox tienen más faltantes: `RoCoLE-csv.csv`, 1.560 × 18, 22,17 %; `RoCoLE-json.json`, 1.560 × 19, 21,0 %. Balance de la etiqueta: 791 sanas, 344 roya nivel 1, 166 nivel 2, 62 nivel 3, 30 nivel 4 y 167 ácaro rojo, verificado en el cuaderno. Las 1.560 imágenes traen fecha EXIF y ninguna trae GPS.
5. **Contraste con el espejo** (si existe): no aplica, porque no se encontró una réplica en Kaggle.

## Anexo C · Checklist de protección de datos personales (uno por fuente)

Fuente: RoCoLe v2 (Mendeley Data)

Regla de la Fase 1: sin personas identificables. Solo se usan datos públicos, agregados o anonimizados por la fuente oficial. «Ley» = Ley 1581 de 2012; «DUR» = Decreto 1074 de 2015, que compila el Decreto 1377 de 2013.

**Resultado** (se marca uno):

- [x] Sin datos de personas.
- [ ] Datos de personas anonimizados por la fuente.
- [ ] Datos personales o sensibles → no admisibles en la Fase 1; en fases posteriores requieren el visto bueno del docente antes de modelar.

### A. ¿Hay datos personales? (Ley, art. 3 lit. c)

- [x] Se revisaron todas las columnas, imágenes y metadatos en busca de identificadores directos (nombre, documento, correo, teléfono, dirección, número de cuenta, contrato, NIU, matrícula, placa, rostro, voz). → Las imágenes muestran solo hojas, sin rostros. Las exportaciones de Labelbox (`RoCoLE-csv.csv`, `RoCoLE-json.json`) incluyen el correo del anotador en la columna «Created By»; esos archivos no se usan, y el proyecto trabaja solo con `RoCoLe-classes.xlsx` (columnas File, Binary.Label y Multiclass.Label).
- [x] Se revisaron los identificadores indirectos, que combinados permiten señalar a alguien: coordenadas exactas, fecha + municipio pequeño, edad + sexo + institución, metadatos EXIF/GPS de fotos. → Se revisó el EXIF de las 1.560 imágenes: todas traen fecha de toma y ninguna trae GPS. El único dato de ubicación es el de un centro de investigación público.
- [x] Un identificador seudonimizado (p. ej., un NIU o un documento cifrado) se trata como dato personal: sigue siendo «asociable» a la persona. → No hay identificadores de personas.

### B. ¿Hay datos sensibles? (Ley, art. 5)

- [ ] Si los hay, la base es una de estas dos: autorización explícita del titular (art. 6 lit. a; DUR 2.2.2.25.2.3) o finalidad científica o estadística con supresión de identidad (art. 6 lit. e). En este curso, la regla práctica es usar solo conjuntos anonimizados por la fuente oficial. → No aplica: no hay datos sensibles.
- [ ] Imágenes médicas y conteos de salud (p. ej., SIVIGILA): se declaran como datos de salud y no se cruzan con fuentes que permitan reidentificar. → No aplica.

### C. ¿Hay niños, niñas o adolescentes? (Ley, art. 7; DUR 2.2.2.25.2.9)

- [ ] Si los titulares pueden ser menores (p. ej., pruebas de Estado escolares, matrícula, registros pediátricos), solo se usan datos públicos o anonimizados y agregados de fuente oficial. No se recolectan datos propios de menores en este proyecto. → No aplica: no hay personas.

### D. Base legal o autorización para datos de terceros

- [x] Fuente pública oficial: se citan sus términos de uso. Que algo esté «en internet» no lo convierte en dato público (DUR 2.2.2.25.2.2: los datos de fuentes de acceso público solo pueden tratarse libremente si «por su naturaleza, sean datos públicos»). → Conjunto público con licencia CC BY 4.0.
- [ ] Datos propios o de una organización (finca, cooperativa, empleador): hay autorización previa, expresa e informada del titular o permiso escrito de la entidad (Ley, arts. 3 lit. a y 9; DUR 2.2.2.25.2.4: escrita, oral o por conducta inequívoca, «en ningún caso el silencio»), y se conserva la prueba (DUR 2.2.2.25.2.5). En la Fase 1, además, con las salvaguardas de los datos propios no queda ninguna persona identificable. → No aplica.
- [ ] Datos de un empleador: además, hay permiso para usarlos fuera de la empresa y se respeta su confidencialidad (Ley, art. 4 lit. h). → No aplica.

### E. Finalidad (Ley, art. 4 lit. b)

- [x] Finalidad declarada: «uso académico para entrenar y evaluar un modelo en el curso; no se toman decisiones sobre personas identificadas».

### F. Anonimización y riesgo de reidentificación

- [ ] Se eliminaron los identificadores directos y se generalizaron los indirectos (p. ej., coordenadas → vereda o municipio; fecha → semana o mes; edad → rangos). → No aplica: no hay identificadores de personas.
- [ ] Se borraron los metadatos EXIF/GPS de las imágenes. → No se borran: ninguna de las 1.560 imágenes trae GPS, y la fecha EXIF se conserva porque es la clave de alineación y no identifica a ninguna persona. Las imágenes no se suben a GitHub.
- [x] Prueba de reidentificación respondida por escrito: «¿podría alguien identificar a una persona combinando estas columnas con información pública?». Las celdas con conteos muy pequeños (p. ej., 1 caso por municipio y semana) no se publican sin agregar. → No: la ubicación corresponde a un centro de investigación, no a una persona.

### G. Licencia de uso (de cada fuente, verificada en la fuente primaria)

- [x] Nombre y versión de la licencia, con el enlace donde se verificó (p. ej., «CC BY 4.0, ficha DataCite del DOI»). → CC BY 4.0, página del conjunto en Mendeley Data.
- [x] Obligaciones anotadas: BY = atribuir e indicar los cambios (p. ej., «características tabulares derivadas de RoCoLe»); SA = los derivados redistribuidos, y en algunos casos los modelos entrenados (PlantVillage), van con la misma licencia; NC = sin uso comercial (pertinente si el cliente es una empresa); ND = sin obras derivadas. → BY: se atribuye a los autores y se indica el cambio («características tabulares derivadas de RoCoLe»).
- [x] Se cumplen los términos del portal (registro, prohibición de reidentificar, cita obligatoria). → Cita obligatoria incluida en la sección 8.

### H. Transferencia o transmisión internacional (Colab, Drive, GitHub, asistentes de IA)

- [x] Se sabe que estos servicios procesan los datos fuera de Colombia (Ley, art. 26; DUR 2.2.2.25.1.3, nums. 4–5, y 2.2.2.25.5.1). Aunque el país de destino figure en la lista de la SIC (Circular Única, Título V, num. 3.2), se exige responsabilidad demostrada.
- [x] A Colab, Drive y GitHub solo se suben datos sin personas identificables (públicos, anonimizados o agregados).
- [x] A los asistentes de IA no se les pegan registros reales con datos personales: solo el esquema o filas sintéticas. → Solo el esquema.

### I. Minimización y conservación

- [x] Solo se descargan y conservan las columnas necesarias para el problema (DUR 2.2.2.25.2.1). → Imágenes y `RoCoLe-classes.xlsx`; no se usan las columnas de Labelbox con datos del anotador.
- [x] Se declara dónde se guardan los datos crudos y que se borran al terminar el curso o la Fase 3 (DUR 2.2.2.25.2.8), con medidas de seguridad razonables (Ley, art. 4 lit. g). → Los datos crudos se guardan en Drive y se borran al terminar la Fase 3.

### J. Publicación del repositorio (Ley, art. 4 lit. f)

- [x] El repositorio es privado y compartido con el docente, o es público y no contiene datos personales y la licencia de los datos permite redistribuirlos. → Repositorio privado compartido con el docente.
- [x] Si los datos no se pueden redistribuir, el repositorio trae el script de descarga desde la fuente primaria; la carpeta de datos va en `.gitignore`. → La carpeta `datos/` va en `.gitignore` y el repositorio trae `scripts/descargar_datos.py`.
- [x] Las salidas del cuaderno (`df.head()`, ejemplos de imágenes, capturas) no muestran registros con datos personales.

---

Fuente: NASA POWER

Regla de la Fase 1: sin personas identificables. Solo se usan datos públicos, agregados o anonimizados por la fuente oficial. «Ley» = Ley 1581 de 2012; «DUR» = Decreto 1074 de 2015, que compila el Decreto 1377 de 2013.

**Resultado** (se marca uno):

- [x] Sin datos de personas.
- [ ] Datos de personas anonimizados por la fuente.
- [ ] Datos personales o sensibles → no admisibles en la Fase 1; en fases posteriores requieren el visto bueno del docente antes de modelar.

### A. ¿Hay datos personales? (Ley, art. 3 lit. c)

- [x] Se revisaron todas las columnas, imágenes y metadatos en busca de identificadores directos (nombre, documento, correo, teléfono, dirección, número de cuenta, contrato, NIU, matrícula, placa, rostro, voz). → Series meteorológicas por coordenadas, sin identificadores de personas.
- [x] Se revisaron los identificadores indirectos, que combinados permiten señalar a alguien: coordenadas exactas, fecha + municipio pequeño, edad + sexo + institución, metadatos EXIF/GPS de fotos. → La coordenada corresponde a un centro de investigación, no a una persona.
- [x] Un identificador seudonimizado (p. ej., un NIU o un documento cifrado) se trata como dato personal: sigue siendo «asociable» a la persona. → No hay identificadores de personas.

### B. ¿Hay datos sensibles? (Ley, art. 5)

- [ ] Si los hay, la base es una de estas dos: autorización explícita del titular (art. 6 lit. a; DUR 2.2.2.25.2.3) o finalidad científica o estadística con supresión de identidad (art. 6 lit. e). En este curso, la regla práctica es usar solo conjuntos anonimizados por la fuente oficial. → No aplica.
- [ ] Imágenes médicas y conteos de salud (p. ej., SIVIGILA): se declaran como datos de salud y no se cruzan con fuentes que permitan reidentificar. → No aplica.

### C. ¿Hay niños, niñas o adolescentes? (Ley, art. 7; DUR 2.2.2.25.2.9)

- [ ] Si los titulares pueden ser menores (p. ej., pruebas de Estado escolares, matrícula, registros pediátricos), solo se usan datos públicos o anonimizados y agregados de fuente oficial. No se recolectan datos propios de menores en este proyecto. → No aplica.

### D. Base legal o autorización para datos de terceros

- [x] Fuente pública oficial: se citan sus términos de uso. Que algo esté «en internet» no lo convierte en dato público (DUR 2.2.2.25.2.2: los datos de fuentes de acceso público solo pueden tratarse libremente si «por su naturaleza, sean datos públicos»). → Datos públicos de la NASA, de libre uso, con reconocimiento solicitado.
- [ ] Datos propios o de una organización (finca, cooperativa, empleador): hay autorización previa, expresa e informada del titular o permiso escrito de la entidad (Ley, arts. 3 lit. a y 9; DUR 2.2.2.25.2.4: escrita, oral o por conducta inequívoca, «en ningún caso el silencio»), y se conserva la prueba (DUR 2.2.2.25.2.5). En la Fase 1, además, con las salvaguardas de los datos propios no queda ninguna persona identificable. → No aplica.
- [ ] Datos de un empleador: además, hay permiso para usarlos fuera de la empresa y se respeta su confidencialidad (Ley, art. 4 lit. h). → No aplica.

### E. Finalidad (Ley, art. 4 lit. b)

- [x] Finalidad declarada: «uso académico para entrenar y evaluar un modelo en el curso; no se toman decisiones sobre personas identificadas».

### F. Anonimización y riesgo de reidentificación

- [ ] Se eliminaron los identificadores directos y se generalizaron los indirectos (p. ej., coordenadas → vereda o municipio; fecha → semana o mes; edad → rangos). → No aplica.
- [ ] Se borraron los metadatos EXIF/GPS de las imágenes. → No aplica: no hay imágenes.
- [x] Prueba de reidentificación respondida por escrito: «¿podría alguien identificar a una persona combinando estas columnas con información pública?». Las celdas con conteos muy pequeños (p. ej., 1 caso por municipio y semana) no se publican sin agregar. → No: no hay personas en la serie.

### G. Licencia de uso (de cada fuente, verificada en la fuente primaria)

- [x] Nombre y versión de la licencia, con el enlace donde se verificó (p. ej., «CC BY 4.0, ficha DataCite del DOI»). → Datos NASA de libre uso, documentación de la fuente.
- [x] Obligaciones anotadas: BY = atribuir e indicar los cambios (p. ej., «características tabulares derivadas de RoCoLe»); SA = los derivados redistribuidos, y en algunos casos los modelos entrenados (PlantVillage), van con la misma licencia; NC = sin uso comercial (pertinente si el cliente es una empresa); ND = sin obras derivadas. → Reconocimiento: «The data was obtained from the National Aeronautics and Space Administration (NASA) Langley Research Center (LaRC) Prediction of Worldwide Energy Resource (POWER) Project funded through the NASA Earth Science/Applied Science Program».
- [x] Se cumplen los términos del portal (registro, prohibición de reidentificar, cita obligatoria). → Se incluye el reconocimiento solicitado.

### H. Transferencia o transmisión internacional (Colab, Drive, GitHub, asistentes de IA)

- [x] Se sabe que estos servicios procesan los datos fuera de Colombia (Ley, art. 26; DUR 2.2.2.25.1.3, nums. 4–5, y 2.2.2.25.5.1). Aunque el país de destino figure en la lista de la SIC (Circular Única, Título V, num. 3.2), se exige responsabilidad demostrada.
- [x] A Colab, Drive y GitHub solo se suben datos sin personas identificables (públicos, anonimizados o agregados).
- [x] A los asistentes de IA no se les pegan registros reales con datos personales: solo el esquema o filas sintéticas. → Solo el esquema.

### I. Minimización y conservación

- [x] Solo se descargan y conservan las columnas necesarias para el problema (DUR 2.2.2.25.2.1). → Solo T2M, RH2M y PRECTOTCORR para el sitio y la ventana declarados.
- [x] Se declara dónde se guardan los datos crudos y que se borran al terminar el curso o la Fase 3 (DUR 2.2.2.25.2.8), con medidas de seguridad razonables (Ley, art. 4 lit. g). → El CSV se guarda en Drive y se borra al terminar la Fase 3.

### J. Publicación del repositorio (Ley, art. 4 lit. f)

- [x] El repositorio es privado y compartido con el docente, o es público y no contiene datos personales y la licencia de los datos permite redistribuirlos. → Repositorio privado compartido con el docente.
- [x] Si los datos no se pueden redistribuir, el repositorio trae el script de descarga desde la fuente primaria; la carpeta de datos va en `.gitignore`. → El cuaderno regenera el CSV desde la API.
- [x] Las salidas del cuaderno (`df.head()`, ejemplos de imágenes, capturas) no muestran registros con datos personales.

**Declaración.** Lo consignado en este checklist es verdadero y se revisó para cada fuente de la Propuesta.

| Integrante | Firma | Fecha (AAAA-MM-DD) |
| --- | --- | --- |
| | | |
| | | |
| | | |
