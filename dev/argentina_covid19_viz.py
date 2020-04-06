#!/usr/bin/env python
# coding: utf-8

# 
# # "COVID19- Argentina"
# > "Visualización de casos basado en [jupyter-nb](https://github.com/pratapvardhan/notebooks/blob/master/covid19/covid19-overview.ipynb) de [@PratapVardhan](https://twitter.com/PratapVardhan) "
# - toc: false
# - branch: master
# - badges: true
# - hide_binder_badge: true
# - comments: false 
#  
#  
#  
#  
#  
#  

# In[1]:


#hide
import os
import numpy as np
import pandas as pd
import glob
import locale
import arcovid19 as arc19
import altair as alt
from altair import datum
#
from jinja2 import Template
from IPython.display import HTML,display
# Set Language
_=locale.setlocale(locale.LC_TIME,'es_ES.utf8')


# In[2]:


#hide
running_nb=False
write_products=True


# In[3]:


#hide

## readers
def get_prc_df_local(data_src,sheets=['casos','casos_fix','casos_vespertinos']):
    """
    """
    lst_df_=[]
    for sn in sheets:
        df_=pd.read_excel(data_src,sheet_name=sn,parse_dates=[0])
        lst_df_.append(df_)
    df_cat_=pd.concat(lst_df_,axis=0,)
    df_cat_['fecha']=pd.to_datetime(df_cat_['fecha'].dt.strftime('%Y-%m-%d'))
    # Group all with "FIX"
    df_cat_=df_cat_.groupby(['provincia','fecha'])[['confirmados','muertes','recuperados']].sum().reset_index()
    #
    df_cumsum_=df_cat_.groupby(['provincia'])[['confirmados','muertes','recuperados']].cumsum().add_prefix('cumsum_')
    # concat dfs
    df_cat=pd.concat([df_cat_,df_cumsum_],axis=1)

    return df_cat


def get_prc_df_arc19(url=arc19.CASES_URL,cached=True):
    """
    """
    #
    df_tmp=arc19.load_cases(cached=cached)
    df_tmp.reset_index(inplace=True)
    df_tmp.drop(['provincia_status','Pcia_status'],axis=1,inplace=True)
    df_tmp.dropna(inplace=True)
    # arc19 nos da los acumulados diarios
    cmra_daily={'C':'confirmados','R':'recuperados','D':'muertes','A':'activos'}
    cmra_cumsum={'C':'cumsum_confirmados','R':'cumsum_recuperados','D':'cumsum_muertes','A':'cumsum_activos'}
    cmra_cumsum_list=list(cmra_cumsum)
    cmra_daily_list=list(cmra_daily)

    df_cat_list=[]

    for provincia in list(set(df_tmp.cod_provincia)):
        #provincia='ARG'
        df_tmp_prov=df_tmp[df_tmp.cod_provincia==provincia].T
        status_names=df_tmp_prov.loc['cod_status'].to_dict()
        df_tmp_prov.rename(columns=status_names,inplace=True)
        df_tmp_prov.drop(['cod_provincia','cod_status'],inplace=True)
        df_tmp_prov.reset_index(inplace=True)
        df_tmp_prov['provincia']=provincia
        df_tmp_prov.rename(columns={'index':'fecha'},inplace=True)
        df_tmp_prov['fecha']=pd.to_datetime(df_tmp_prov['fecha'].dt.strftime('%Y-%m-%d'))
        d=df_tmp_prov[cmra_cumsum_list].diff()
        d.loc[0]=df_tmp_prov[cmra_cumsum_list].loc[0]
        d.rename(columns=cmra_daily,inplace=True)
        df_prov=pd.concat([df_tmp_prov,d],axis=1).rename(columns=cmra_cumsum)
        df_cat_list.append(df_prov)
    df_=pd.concat(df_cat_list)
    provDict=arc19.CODE_TO_POVINCIA
    provDict.update({'ARG':'Argentina_Nacion','BA': 'Buenos Aires'})
    #
    df_['provincia']=df_['provincia'].map(provDict)
    return df_

#

def get_frame_unstack(df_,oncol,group_by_lst=['provincia','fecha']):
    s=df_.groupby(group_by_lst)[oncol].sum().unstack()
    return s

def get_template(path):
    from urllib.parse import urlparse
    if bool(urlparse(path).netloc):
        from urllib.request import urlopen
        return urlopen(path).read().decode('utf8')
    return open(path).read()

def write_report(hmtl,out_name):
    with open(out_name,'w') as f:
        f.write(html)
    
#
provDict={'Ciudad Autónoma de Buenos Aire':'CABA'}


# In[4]:


#hide
## make products folders
data_prod = '../products'
data_includes_ = '../_includes'
os.makedirs(data_prod, exist_ok=True)
os.makedirs(data_includes_, exist_ok=True)


# ### Pre-Procesamiento
# 
# #### Unimos los DataFrames
# 
# Importamos los datos como DataFrames y los unimos.

# In[5]:


#hide_input
# CSV sources
local=True # if false import from arcovid
if local:
    data_src_= '../data/casos.xlsx'
    #
    df_ = get_prc_df_local(data_src_)
    df_['provincia'] = df_['provincia'].apply(
        lambda x: provDict[x] if x in provDict else x)
else:
    data_src_=arc19.CASES_URL
    df_=get_prc_df_arc19(url=data_src_,cached=True)
    arc19.load_cases()
print('Importando desde: {}'.format(data_src_))
df_.head()


# ### Procesamiento
# 
# Procesamos los datos y dejamos los mismos en el formato que seran utilizados en el reporte.

# In[6]:


#hide_input
ndays_=-3

# Get cases
dft_cases = get_frame_unstack(df_,'confirmados')
dft_deaths = get_frame_unstack(df_,'muertes')
dft_recovered = get_frame_unstack(df_,'recuperados')
# dates
last_=dft_cases.columns[-1]
nlast_=dft_cases.columns[ndays_]

# stats
dfc_cases = dft_cases.cumsum(axis=1)[last_]
dfc_deaths = dft_deaths.cumsum(axis=1)[last_]
dfc_recovered = dft_recovered.cumsum(axis=1)[last_]
dfp_cases = dft_cases.cumsum(axis=1)[nlast_]
dfp_deaths = dft_deaths.cumsum(axis=1)[nlast_]
dfp_recovered = dft_recovered.cumsum(axis=1)[nlast_]
#
cstr=['confirmados','muertes','recuperados']
#hide
df_table = (pd.DataFrame(dict(
    confirmados=dfc_cases, muertes=dfc_deaths, recuperados=dfc_recovered,
    Pconfirmados=dfp_cases, Pmuertes=dfp_deaths, Precuperados=dfp_recovered))
             .sort_values(by=['confirmados', 'muertes'], ascending=[False, False])
             .reset_index())

for c in cstr:
    df_table[f'{c} (+)'] = (df_table[c] - df_table[f'P{c}']).clip(0)  # DATA BUG
df_table['Tasa Fatalidad'] = (100 * df_table['muertes'] / df_table['confirmados']).round(1)
df_table=df_table.fillna(0)
#
metrics = ['confirmados', 'muertes', 'recuperados', 'confirmados (+)', 'muertes (+)', 'recuperados (+)']
s_caba = df_table[df_table['provincia'].eq('CABA')][metrics].sum().add_prefix('CABA ')
s_bsas = df_table[df_table['provincia'].eq('Buenos Aires')][metrics].sum().add_prefix('BSAS ')
s_cba = df_table[df_table['provincia'].eq('Córdoba')][metrics].sum().add_prefix('CBA ')
s_nacion=df_table[df_table['provincia'].eq('Argentina_Nacion')][metrics].sum().add_prefix('')

summary = {'updated': pd.to_datetime(last_), 'since': pd.to_datetime(nlast_)}
summary = {**summary, **s_nacion, **s_caba, **s_bsas, **s_cba}
#
dft_ct_cases = dft_cases.cumsum(axis=1)
dft_ct_new_cases = dft_ct_cases.diff(axis=1).fillna(0).astype(int)

#
print('Visualizamos algunos:')
df_table.head(10)


# In[7]:


#hide_input
template = Template(get_template('../viz_template/overview_argentina.tpl'))
html = template.render(
    D=summary, table=df_table,  
    newcases=dft_ct_new_cases.loc[:,:],
    np=np, pd=pd, enumerate=enumerate)

reporte_html=f'<div>{html}</div>'
if write_products:
    name_html=os.path.join(data_prod,last_.strftime('%Y%m%d')+'_reporte.html')
    latest_html=os.path.join(data_includes_,'ultimo_reporte.html')
    write_report(reporte_html,name_html)
    write_report(reporte_html,latest_html)
#
if running_nb:
    display(HTML(reporte_html))


# ### Curvas
# 
# Visualizamos algunas curvas y graficos relacionados al covid 19.
# En el grafico central podemos ver la evolucion de casos confirmados:
# - el radio indica la cantidad de casos confirmados en el dia (tooltip)
# - la selección de un dado dia activa el grafico de barra indicando la distribucion por provincia.

# In[8]:


#hide_input
width_=660
height_curve_=400
height_bar_=220

source=df_
pts = alt.selection(type="single", encodings=['x'],empty='none')
#

tooltip_points=[alt.Tooltip('confirmados:Q', title='#Confirmados @Fecha'),                alt.Tooltip('fecha:T', title='Fecha'),                alt.Tooltip('provincia:N', title='Provincia'),                alt.Tooltip('muertes:Q', title='Muertes'),                alt.Tooltip('recuperados:Q', title='Recuperados')]

points = alt.Chart(source).mark_circle(color='orange').encode(
    alt.X('fecha:T',title='Fecha'),
    alt.Y('cumsum_confirmados:Q',scale=alt.Scale(type='log'),title='#Confirmados Totales en Argentina (log scale)'),
    size=alt.Size('confirmados',title='Confirmados x dia'),
    color=alt.condition(pts, 'confirmados:Q', alt.value('orange'),legend=None),
    tooltip=tooltip_points
).properties(        width=width_,
        height=height_curve_).transform_filter((datum.provincia == 'Argentina_Nacion')).add_selection(pts)


tooltip_bars=[alt.Tooltip('cumsum_confirmados:Q', title='#Confirmados Totales'),alt.Tooltip('fecha:T', title='Fecha'),alt.Tooltip('provincia:N', title='Provincia')]

bars = alt.Chart(source).mark_bar().encode(
       alt.X('provincia:N',axis=alt.Axis(minExtent=100),title='Provincia de Residencia'),
        alt.Y('cumsum_confirmados:Q',title='Confirmados x Provincia'),
        color=alt.Color('cumsum_confirmados:Q',title='Confirmados x Provincia',legend=None),
        tooltip=tooltip_bars).properties(  
    width=width_,
        height=height_bar_
    ).transform_filter(datum.provincia != 'Argentina_Nacion').transform_filter((pts)).interactive()

texts = alt.Chart(source).mark_text(dy=0, size=20).encode(
    text='fecha:T'
).transform_filter(
    pts
)
if write_products:
    lines_html=os.path.join(data_includes_,'ultimo_reporte_lines.html')
    alt.vconcat(points, bars+texts,data=source).save(lines_html)
if running_nb:
    display(alt.vconcat(points, bars+texts))


# #### Heatmap
# 
# Y observamos el heatmap correspondiente a los casos confirmados por dia

# In[9]:


#hide_input
#
width_=660
height_heatmap_=660
#
source_provincia=source[source.provincia!='Argentina_Nacion']

tooltip_bars=[alt.Tooltip('cumsum_confirmados:Q', title='#Confirmados Totales'),              alt.Tooltip('fecha:T', title='Fecha'),              alt.Tooltip('provincia:N', title='Provincia')]

rect=alt.Chart(source_provincia).mark_rect().encode(
    alt.Y('provincia:O', title='Provincias',scale=alt.Scale(paddingInner=0)),
    alt.X('monthdate(fecha):O', title='Fecha',scale=alt.Scale(paddingInner=0)),
    alt.Color('confirmados:Q', title='#Confirmados x dia',scale=alt.Scale(scheme='lightgreyred')),
tooltip=tooltip_bars
).properties(width=width_, height=height_heatmap_)

# Configure text
text = rect.mark_text(baseline='middle').encode(
    text=alt.Text('confirmados:Q'),
    color=alt.condition(
        alt.datum.confirmados < 20,
        alt.value('black'),
        alt.value('white')
    )
)

heatmap_=(rect + text).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

if write_products:
    heatmap_html=os.path.join(data_includes_,'ultimo_reporte_heatmap.html')
    heatmap_.save(heatmap_html)
if running_nb:
    display(heatmap_)


# In[ ]:




