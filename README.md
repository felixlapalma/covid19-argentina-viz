# Covid19 en Argentina

## Viz

Reporte en [html](https://htmlpreview.github.io/?https://github.com/felixlapalma/covid19-argentina-viz/master/products/ultimo_reporte.html) con información relativa a casos confirmados/muertes/recuperados de COVID19 en Argentina.

{% include ultimo_reporte.html %}

## Fuentes

La fuente principal corresponde a los reportes diarios del [ministerio de salud](https://www.argentina.gob.ar/salud/coronavirus-COVID-19).

Sin embargo existen ciertos casos en los cuales los mismos no brindan precisiones geográficas. En esas instancias
se busco en diarios la información o en ultima instancia se asumio alguna distribución. Estos casos se pueden encontrar en
[README_DATOS](data/README_DATOS.md)

## **WIP**

Los casos recuperados se encuentran en análisis para su actualizacion (la discriminación de recuperados no es clara en la información actual)


## Credits

Credits to [@PratapVardhan](https://twitter.com/PratapVardhan)). 

The base jnb was taken from [base_jnb](https://github.com/pratapvardhan/notebooks/blob/master/covid19/covid19-overview.ipynb)
and the base template (for viz) was taken from [base_template](https://github.com/pratapvardhan/notebooks/blob/master/covid19/overview.tpl)
