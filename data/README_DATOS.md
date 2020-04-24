## Datos Faltantes

### Comentarios Generales

- En el reporte del 20200318 se comenta que en el reporte del 20200317 se indico un caso en Provincia de Buenos Aires que no correspondia -> Borro el
registro del csv 20200317_provincias_* (esto deja inconsitente la suma para ese día).

- En el reporte del 20200323 se menciona un caso duplicado (ver en confirmados 9).

- Se utilizaron algunos graficos de [infobae](https://www.infobae.com/sociedad/2020/03/18/coronavirus-en-la-argentina-4-graficos-para-comprender-el-avance-de-la-pandemia/) para contrastar
ciertos casos. 

- Se incorpora los casos reportados por [@jorgeluisaliaga](https://twitter.com/jorgeluisaliaga) en [src](https://t.co/A6X5GTltVQ?amp=1) como recopilación
de los casos nacionales. En general existen inconvenientes para mapear las sumas totales de las provincias al total nacional.

- 20200327_provincias_FIXfilled.csv: incorpora 16 casos reubicados informados en informer del dia 28 (en funcion de los datos del dia 29, donde el ministerio informa los casos por provincia).

- 2020040XXXX_argentina_filled.csv: se corrige el dia 01-04 , notar que dos reportes supestamente identicos fueron cambiados (la version del 20200401 cambia)

- *20200404: Se cambia a casos.xlsx (quedan en desuso los csv - [Tag v0.0.1](https://github.com/felixlapalma/covid19-argentina-viz/releases/tag/v0.0.1))* 

- 20200406: Falta reporte matutino (informe de recuperados y posibles decesos). Existen dos (2) fallecidos que no se reportan por provincia. La cuenta salta de 46 (infome vespertino 20200405) 
a 53 (informe vespertino 20200406), pero en este ultimo caso solo reportan 5 casos. 

- 20200417: En el reportes se menciona que un caso de chubut se relocaliza a Buenos Aires (corregido en reporte_fix @ casos.xlsx)

- 20200420: Los reportes e imagenes que originan los datos se mudan a [src](https://drive.google.com/drive/folders/1RrV39e8ZBR2GGdHf-zQSpgpAIk7UALoO?usp=sharing)


#### Confirmados

1. [link](https://www.bbc.com/mundo/noticias-america-latina-51728654): 20200303 -> 1 caso (primer caso)

2. [link](https://www.primeraedicion.com.ar/nota/100240451/coronavirus-se-registro-la-primera-muerte-en-argentina/): 20200307 -> Se registra el caso despues del fallecimiento 

3. [link](https://tapas.clarin.com/tapa.html#20200307):
  * 20200307 -> 6 casos (4 CABA /1 BSAS /1 CBA) corresponden al 20200306 OK!!)
  * [link](https://www.diarionorte.com/tapa-del-dia/?page=2): Consistente con 6 casos nuevos el 20200306

4. [link](https://www.lavoz.com.ar/ciudadanos/coronavirus-dos-nuevos-casos-en-cordoba-y-ya-son-30-en-pais): 20200312 -> 2 casos

5. [link](https://www.diarionorte.com/tapa-del-dia/)
  * 20200312 -> 2 casos (Chaco)
  * 20200314 -> 1 caso  (Chaco)

6. [link](https://www.ellitoral.com/index.php/diarios/2020/03/14/tapa/index.html): 20200314 -> 1 caso (Santa Fe)

7. [link](https://www.infobae.com/sociedad/2020/03/12/confirmaron-otros-nueve-casos-de-coronavirus-en-la-argentina-y-cuatro-de-ellos-son-autoctonos/)
  * 20200312 -> 2 Internados en Capital -> Asumo 3 en BsAs -> 1 Entre Rios

8. [link](http://diariotextual.com/inicio/index.php/2020/03/14/11-nuevos-casos-coronavirus-la-argentina-total-infectados-asciende-45/)
  * 20200314 -> 2 Casos confirmados en BSAS (1 en chaco/ 1 en Santa Fe - ver links anteriores). Sin confirmación,**ELIJO**, 3 en CABA > quedan 6 en BsAs


9. [link](https://www.lavoz.com.ar/ciudadanos/tercer-fallecido-en-pais-y-un-nuevo-contagio-en-cordoba)
  * 1 Caso en Cordoba (diferencia con nación ->6 nacion contra 5 reportados en CBA) - **ELIJO** sacarselo al 20200319_provincias_ (*Deja inconsistente la suma ese dia*)

10. 20200325 reporte diario: se descartan 2 reportados el 20200324. 

#### Muertes:

1. [link](https://www.infobae.com/coronavirus/2020/03/22/confirmaron-41-nuevos-casos-de-coronavirus-en-la-argentina-y-el-total-de-infectados-asciende-a-266/)
  * 1 Muerto en CABA (7 de Marzo)
  * 1 Muerto en Chaco (13 de Marzo) (tambien en /minsal reporte diario)
  * 1 Muerto en CABA (18 de Marzo)
  * 1 Muerto en BsAs (21 de Marzo) 

2. [link](https://www.infobae.com/sociedad/2020/03/24/confirmaron-86-nuevos-casos-de-coronavirus-en-la-argentina-y-el-total-de-infectados-asciende-a-387/)



#### Recuperados - WIP

1. [link](https://www.infobae.com/coronavirus/2020/03/14/hay-11-nuevos-casos-de-coronavirus-en-la-argentina-y-el-total-de-infectados-asciende-a-45/)
  * 1 Recuperado (el primero) -> Jueves 12 de Marzo

2. [link](http://chaco.gov.ar/covid19/): Recuperados de Chaco a partir de información del Ministerio de Salud de Chaco y su cuenta de Twitter @ChacoSalud 

3. [link](https://www.santafe.gob.ar/index.php/web/content/view/full/234420/(subtema)/93802): Recuperados Santa Fe

4. [link](http://www.prensa.mendoza.gov.ar/comunicados/): Recuperados Mendoza

5. [link](https://twitter.com/minsaludcba): Recuperados Córdoba

6. [link](https://www.bariloche2000.com/noticias/leer/anunciaron-restricciones-de-actividades-que-habian-sido-habilitadas-en-bariloche/126576): Rio Negro (No oficial)

7. [link](https://www.gba.gob.ar/saludprovincia/boletin_epidemiologico): Buenos Aires (informe semanales)
