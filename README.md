# covid19-argentina-viz
Repository to leave a nice (credits to @PratapVardhan) viz regarding covid19 cases in Argentina. 

The base jnb was taken from [base_jnb](https://github.com/pratapvardhan/notebooks/blob/master/covid19/covid19-overview.ipynb)
and the base template (for viz) was taken from [base_template](https://github.com/pratapvardhan/notebooks/blob/master/covid19/overview.tpl)

## Fuentes

La fuente principal corresponde a los reportes diarios del [ministerio de salud](https://www.argentina.gob.ar/salud/coronavirus-COVID-19).

Sin embargo existen ciertos casos en los cuales los mismos no brindan precisiones geográficas. En esas instancias
se busco en diarios la información o en ultima instancia se asumio alguna distribución. Estos casos se pueden encontrar en
[README_DATOS](data/README_DATOS.md)

## Viz

Se genera un [html](https://htmlpreview.github.io/?https://github.com/felixlapalma/covid19-argentina-viz/master/products/ultimo_reporte.html) con información relativa a casos confirmados/muertes/recuperados.
{% include ultimo_reporte.html %}

## WIP

Los casos recuperados se encuentran en análisis para su actualizacion (la discriminación de recuperados no es clara en la información actual)
