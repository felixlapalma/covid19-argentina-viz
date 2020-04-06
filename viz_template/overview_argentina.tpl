{# D, table, newcases, np, pd  #}
{% set COL_REGION = COL_REGION or 'provincia' %}
{% set KPI_CASE = KPI_CASE or 'Argentina' %}
{% set KPIS_INFO = KPIS_INFO or [{'title': 'CABA', 'prefix': 'CABA'}, {'title': 'Buenos Aires', 'prefix': 'BSAS'}, {'title': 'Córdoba', 'prefix': 'CBA'}] %}
{% set LEGEND_DOMAIN = LEGEND_DOMAIN or [10, 50,100, 1000, np.inf] %}
{% set WIDTH_REGION, WIDTH_STRIP = 140, 140 %}
{% set STRIP_WIDTH = (WIDTH_REGION // newcases.shape[1] + 1) %}
{% set LEGEND_RANGE = ['rgba(255, 152, 0, 0.1)', 'rgba(255, 152, 0, 0.25)','rgba(255, 152, 0, 0.5)', 'rgba(255, 152, 0, 0.75)', 'rgba(255, 152, 0, 1)'] %}
{% set TOPLINKS = TOPLINKS or [{'title': 'Argentina Informe Diario', 'href': 'https://www.argentina.gob.ar/coronavirus/informe-diario'}] %}
{% set lastdays = (D['updated'] - D['since']).days %}

{% macro kpi(name, number, growth, growcls='') -%}
  <div class="kpi">
    <div class="kname">{{ name }}</div>
    <div class="num">{{ '{0:,.0f}'.format(number) }}</div>
    <div class="grow {{ growcls }}">(<b>{{ '{0:+,.0f}'.format(growth) }}</b>)</div>
  </div>
{%- endmacro %}

{% macro kpiblocksm(prefix='', title=KPI_CASE) -%}
  <div class="kpi-sm">
    <div class="kpi-hed">{{ title }}</div>
    <div class="d-flex kpi-box">
      {{ kpi(name='confirmados', number=D[prefix + ' confirmados'], growth=D[prefix + ' confirmados (+)']) }}
      {{ kpi(name='muertes', number=D[prefix + ' muertes'], growth=D[prefix + ' muertes (+)']) }}
    </div>
  </div>
{%- endmacro %}

{% macro toplinks() -%}
<div class="text-center toplinksgithub">
  {% for link in TOPLINKS %}<a href="{{ link['href'] }}">{{ link['title'] }}</a>{% endfor %}
</div>
{%- endmacro %}

{% macro narrative() -%}
{% if KPI_CASE == 'Argentina' %}
  En los últimos <b>{{ lastdays }} dias</b>, <b class="color-neg">{{ '{0:,.0f}'.format(D['confirmados (+)']) }}</b> nuevos casos de COVID19 se han reportado en Argentina.
  De los cuales <b class="color-neg">{{ '{0:,.0f}'.format(D['CABA confirmados (+)']) }}</b> ({{ "{0:.0%}".format(D['CABA confirmados (+)'] / D['confirmados (+)']) }}) son de <b>CABA</b>.
  <b>Buenos Aires</b> ha reportado <b class="color-neg">{{ '{0:,.0f}'.format(D['BSAS confirmados (+)']) }}</b> ({{ "{0:.0%}".format(D['BSAS confirmados (+)'] / D['confirmados (+)']) }}) casos nuevos en los  ultimos {{ lastdays }} dias.
{% else %}
  ''
{% endif %}
{%- endmacro %}

{% macro plotstrip(arr) -%}
  <div class="d-flex" style="height:15px;">
    {% set colors = np.digitize(arr, LEGEND_DOMAIN) %}
    {% for i, v in enumerate(arr) %}
    <div style="width:{{ STRIP_WIDTH }}px;background:{{ LEGEND_RANGE[colors[i]] if (v) else '#eee' }};border-right:1px solid rgba(255,255,255,0.5);"></div>
    {% endfor %}
  </div>
{%- endmacro %}

{% macro legend() -%}
<svg width="100" height="20" viewBox="0,0,100,20" style="overflow: visible; display: block;">
  <g>
    {% for i, _ in enumerate(LEGEND_DOMAIN) %}
    <rect x="{{ 25 * i }}"  y="8" width="25" height="10" fill="{{ LEGEND_RANGE[i] }}"></rect>
    {% endfor %}
  </g>
  <g style="font-size:10px;text-anchor:middle;">
    {% for i, x in enumerate(LEGEND_DOMAIN[:-1], 1) %}
    <g transform="translate({{ 25 * i }}, 6)"><text>{{ x }}</text></g>
    {% endfor %}
    </g>
</svg>
{%- endmacro %}

<div class="overview">
  {{ toplinks() }}
  <div>
    <div class="kpi-hed">{{ KPI_CASE }}</div>
    <div class="d-flex kpi-box">
      {{ kpi(name='Confirmados', number=D['confirmados'], growth=D['confirmados (+)']) }}
      {{ kpi(name='Muertes', number=D['muertes'], growth=D['muertes (+)']) }}
      {{ kpi(name='Recuperados', number=D['recuperados'], growth=D['recuperados (+)'], growcls='pos') }}
    </div>
  </div>
  <p class="text-center text-uppercase fs9">Actualizado <b>{{ D['updated'].strftime(' %d %B, %Y ') }}</b> ( +cambio desde hace {{ lastdays }} dias)</p>
  <div class="d-flex" style="justify-content:space-between;">
    {% for kpi in KPIS_INFO %}
    {{ kpiblocksm(**kpi) }}
    {% endfor %}
  </div>
  <p class="text-center" style="font-size: 14px;max-width: 400px;">{{ narrative() }}</p>
  <table class="table" style="width:650px;">
    <thead>
      <tr>
        <th class="text-right" style="width:{{ WIDTH_REGION }}px;"></th>
        <th class="text-left" style="width:{{ WIDTH_STRIP }}px;">{{ legend() }}</th>
        <th colspan="7"></th>
      </tr>
      <tr>
        <th class="text-right" style="width:{{ WIDTH_REGION }}px;">{{ {'provincia': 'Provincia'}.get(COL_REGION, 'Location') }}</th>
        <th class="text-left" style="width:{{ WIDTH_STRIP }}px;">Nuevos confirmados</th>
        <th class="text-left" colspan="2">Total confirmados</th>
        <th colspan="2">Muertes</th>
        <th class="fs9" >Fatalidad</th>
        <th class="fs9" colspan="2">Recuperados</th>
      </tr>
    </thead>
    <tbody>
      <tr style="font-size:9px;">
        <td></td>
        <td style="display:flex;justify-content:space-between;">
          <div>{{ pd.to_datetime(newcases.columns[0]).strftime('%b. %d') }}</div>
          <div>{{ pd.to_datetime(newcases.columns[-1]).strftime('%b. %d') }}</div>
        </td>
        <td></td>
        <td colspan="4" class="text-left change" style="font-size: 9px;">(+NUEVOS) desde {{ D['since'].strftime('%b, %d') }}</td>
        <td></td>
        <td></td>
      </tr>
    {% for index, row in table.iterrows() %}
      <tr>
        <td class="mw"><b>{{ row[COL_REGION] }}</b></td>
        <td style="vertical-align: middle;">{{ plotstrip(arr=newcases.loc[row[COL_REGION]].values) }}</td>
        <td class="pl1"><b>{{ '{0:,.0f}'.format(row['confirmados']) }}</b></td>
        <td class="change neg">(<b>{{ '{0:+,.0f}'.format(row['confirmados (+)']) }}</b>)</td>
        <td class="pl1">{{ '{0:,.0f}'.format(row['muertes']) }}</td>
        <td class="change neg">(<b>{{ '{0:+,.0f}'.format(row['muertes (+)']) }}</b>)</td>
        <td class="pl1">{{ row['Tasa Fatalidad'] }}%</td>
        <td>{{ '{0:,.0f}'.format(row['recuperados']) }}</td>
        <td class="change pos">(<b>{{ '{0:+,.0f}'.format(row['recuperados (+)']) }}</b>)</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
<style>
.overview {
  min-width: 500px;
  font-size: 10px;
  font-family: "Segoe UI", SegoeUI, Roboto, "Segoe WP", "Helvetica Neue", "Helvetica", "Tahoma", "Arial", sans-serif !important;
}
.overview .toplinksgithub a {
  background: #d3d3d3;
  font-size: 14px;
  color: #1d87ae;
  margin: 10px;
  padding: 2px 10px;
}
.overview p {
  margin: 6px auto !important;
  padding: 0;
}
@media screen and (max-width: 660px) {
  .overview p { max-width: none !important; }
}
.overview b {
  font-weight: bolder;
}
.overview .kpi-hed {
  font-weight: bold;
  font-size: 20px;
}
.overview .kpi-box {
  justify-content: space-around;
  background: #ececec;
  padding: 10px 0 !important;
  margin: 5px 0 !important;
  min-width: 180px;
}
.overview .kpi .num {
  font-size: 40px;
  line-height: 40px;
  font-weight: bold;
}
.overview .kpi .grow {
  line-height: 12px;
  font-size: 12px;
}
.overview .table .change.pos , .overview .kpi .grow.pos {
  color: #118822;
}
.overview .table .change.neg, .overview .kpi .grow, .color-neg {
  color: #cc1100;
}
.overview p .color-neg {
  background: #ececec;
  padding: 0 5px;
}
.overview .kpi .kname {
  font-size: 12px;
}
.overview .kpi-sm .kpi-hed {
  font-size: 14px;
  line-height: 10px;
  padding-top: 10px !important;
}
.overview .kpi-sm .num {
  font-size: 20px;
  line-height: 20px;
}
.overview .kpi-sm .kname {
  font-size: 11px;
  line-height: 10px;
}
.overview .table {
  border-collapse: collapse;
  margin: auto !important;
  text-align: right;
  margin-top: 14px;
  color: black;
  font-size: 13px;
  display: table !important;
}
.overview .table .change {
  color: #999;
  font-size: 80%;
  text-align: start;
  vertical-align: inherit;
  font-weight: normal;
  padding-left: 1px !important;
}
.overview .table th {
  font-weight: normal;
}
.overview .table tbody tr {
  border-bottom: 1px solid #eee;
  background: none;
}
.overview .table td, .overview .table th {
  padding: 1px 1px 1px 10px !important;
  vertical-align: middle;
  border: none;
  background: none;
}
.overview .table th {
  text-align: center;
  text-transform: uppercase;
}
.overview .table thead {
  border-bottom: 1px solid black;
}
.overview .fs9 {
  font-size: 9px;
}
.overview .d-flex {
  display: flex;
}
.overview .text-center { text-align: center !important; }
.overview .text-left { text-align: left !important; }
.overview .text-right { text-align: right !important; }
.overview .text-uppercase { text-transform: uppercase !important; }
.overview div {
  margin: 0 !important;
  padding: 0 !important;
}
</style>
