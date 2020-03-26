#!/usr/bin/env python
# coding: utf-8

# ## COVID19- Argentina
#
# Visualización de casos basado en:
#
# - https://github.com/pratapvardhan/notebooks/blob/master/covid19/covid19-overview.ipynb
#

# In[1]:


# hide
import os
import numpy as np
import pandas as pd
import glob
import locale
#
from jinja2 import Template
from IPython.display import HTML
# Set Language
_ = locale.setlocale(locale.LC_TIME, 'es_ES.utf8')


# In[2]:


# helpers
def cat_df(data_src):
    lst_ = glob.glob(data_src)
    lst_.sort()
    lst_df_ = []
    for l in lst_:
        df_ = pd.read_csv(l, parse_dates=[0])
        lst_df_.append(df_)
    df_cat_ = pd.concat(lst_df_, axis=0,)
    df_cat_['fecha'] = pd.to_datetime(df_cat_['fecha'].dt.strftime('%Y-%m-%d'))
    return df_cat_
#


def get_frame_unstack(df_, oncol, group_by_lst=['provincia', 'fecha']):
    s = df_.groupby(group_by_lst)[oncol].sum().unstack()
    return s


def get_template(path):
    from urllib.parse import urlparse
    if bool(urlparse(path).netloc):
        from urllib.request import urlopen
        return urlopen(path).read().decode('utf8')
    return open(path).read()


def write_report(hmtl, out_name):
    with open(out_name, 'w') as f:
        f.write(html)


#
provDict = {'Ciudad Autónoma de Buenos Aire': 'CABA'}


# In[3]:


# CSV sources
data_src = '../data/filled/*.csv'
data_prod = '../products'
os.makedirs(data_prod, exist_ok=True)
#
df_ = cat_df(data_src)
df_['provincia'] = df_['provincia'].apply(
    lambda x: provDict[x] if x in provDict else x)
df_.head()


# In[4]:


# Get cases
dft_cases = get_frame_unstack(df_, 'confirmados')
dft_deaths = get_frame_unstack(df_, 'muertes')
dft_recovered = get_frame_unstack(df_, 'recuperados')
# dates
last_ = dft_cases.columns[-1]
nlast_ = dft_cases.columns[-3]


# In[5]:


# stats
dfc_cases = dft_cases.cumsum(axis=1)[last_]
dfc_deaths = dft_deaths.cumsum(axis=1)[last_]
dfc_recovered = dft_recovered.cumsum(axis=1)[last_]
dfp_cases = dft_cases.cumsum(axis=1)[nlast_]
dfp_deaths = dft_deaths.cumsum(axis=1)[nlast_]
dfp_recovered = dft_recovered.cumsum(axis=1)[nlast_]
#
cstr = ['confirmados', 'muertes', 'recuperados']
# hide
df_table = (pd.DataFrame(dict(
    confirmados=dfc_cases, muertes=dfc_deaths, recuperados=dfc_recovered,
    Pconfirmados=dfp_cases, Pmuertes=dfp_deaths, Precuperados=dfp_recovered))
    .sort_values(by=['confirmados', 'muertes'], ascending=[False, False])
    .reset_index())
for c in cstr:
    df_table[f'{c} (+)'] = (df_table[c] -
                            df_table[f'P{c}']).clip(0)  # DATA BUG
df_table['Tasa Fatalidad'] = (
    100 * df_table['muertes'] / df_table['confirmados']).round(1)
df_table = df_table.fillna(0)
#
metrics = ['confirmados', 'muertes', 'recuperados',
           'confirmados (+)', 'muertes (+)', 'recuperados (+)']
s_caba = df_table[df_table['provincia'].eq(
    'CABA')][metrics].sum().add_prefix('CABA ')
s_bsas = df_table[df_table['provincia'].eq(
    'Buenos Aires')][metrics].sum().add_prefix('BSAS ')
s_cba = df_table[df_table['provincia'].eq(
    'Córdoba')][metrics].sum().add_prefix('CBA ')
summary = {'updated': pd.to_datetime(last_), 'since': pd.to_datetime(nlast_)}
summary = {**summary, **df_table[metrics].sum(), **s_caba, **s_bsas, **s_cba}
#
dft_ct_cases = dft_cases.cumsum(axis=1)
dft_ct_new_cases = dft_ct_cases.diff(axis=1).fillna(0).astype(int)


# ### Template

# In[6]:


# hide_input
template = Template(get_template('overview_argentina.tpl'))
html = template.render(
    D=summary, table=df_table,
    newcases=dft_ct_new_cases.loc[:, :],
    np=np, pd=pd, enumerate=enumerate)
name_html = os.path.join(data_prod, last_.strftime('%Y%m%d')+'_reporte.html')
latest_html = os.path.join(data_prod, 'ultimo_reporte.html')
reporte_html = f'<div>{html}</div>'
write_report(reporte_html, name_html)
write_report(reporte_html, latest_html)
#
HTML(reporte_html)
