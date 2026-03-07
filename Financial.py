import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _skpi, _cc, _tbl, _page_header, _lo, BLK, MN
)
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="LabCare · Financial",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("Financial")
render_sidebar("Financial")

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Financial", "💰 Financial",
             "Revenue performance by lab, province and customer type.")

start, end = date_range_picker("rev", df)
flt, _, n  = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

# ── KPI sparklines ──
rev_by_m  = df.groupby(df['Service Date'].dt.month)['Revenue'].sum()
cnt_by_m  = df.groupby(df['Service Date'].dt.month).size()
priv_by_m = df[df['Customer Type']=='Private Company'].groupby(df['Service Date'].dt.month)['Revenue'].sum()
ot_by_m   = df[df['On time/Late']=='On-Time'].groupby(df['Service Date'].dt.month).size() / cnt_by_m * 100

to_m = end.month; fr_m = start.month; pr_m = to_m - 1

total_rev  = flt['Revenue'].sum()
total_cnt  = len(flt)
total_priv = flt[flt['Customer Type']=='Private Company']['Revenue'].sum()
total_ot   = (flt['On time/Late']=='On-Time').mean() * 100 if n else 0

_skpi(None, [
    ('Revenue',     f'Total {MN[fr_m]}–{MN[to_m]}', '#ff6b6b','#000', rev_by_m,  total_rev,  'dollar', rev_by_m.get(pr_m,0),  rev_by_m.get(to_m,0)),
    ('Samples',     f'Total {MN[fr_m]}–{MN[to_m]}', '#ffd93d','#000', cnt_by_m,  total_cnt,  'num',    cnt_by_m.get(pr_m,0),  cnt_by_m.get(to_m,0)),
    ('Private Rev', f'Total {MN[fr_m]}–{MN[to_m]}', '#6bcb77','#000', priv_by_m, total_priv, 'dollar', priv_by_m.get(pr_m,0), priv_by_m.get(to_m,0)),
    ('On-Time %',   f'Avg {MN[fr_m]}–{MN[to_m]}',   '#4d96ff','#000', ot_by_m,   total_ot,   'pct',    ot_by_m.get(pr_m,0),   ot_by_m.get(to_m,0)),
], start, end)

# ── Revenue charts ──
rev_lab  = flt.groupby('Laboratory')['Revenue'].sum().sort_values(ascending=False)
rev_prov = flt.groupby('Province')['Revenue'].sum().sort_values(ascending=False)
ct       = flt.groupby('Customer Type')['Revenue'].sum().sort_values(ascending=False)

PIE_COLORS = ['#7c3aed','#3b82f6','#059669','#f59e0b','#ef4444','#ec4899','#06b6d4']


def _pie(labels, values, title, subtitle, colors=PIE_COLORS):
    fig = px.pie(names=labels, values=values,
                 color_discrete_sequence=colors, hole=0.42)
    fig.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )
    lo = _lo(300)
    lo['showlegend'] = True
    lo['legend'] = dict(orientation='v', x=1.02, y=0.5,
                        font=dict(size=10, color=BLK), bgcolor='rgba(255,255,255,.9)')
    fig.update_layout(**lo)
    _cc(title, subtitle, fig, h=300)


def _hist_h(labels, values, title, subtitle, color='#7c3aed'):
    df_h = pd.DataFrame({'label': labels, 'value': values}).sort_values('value')
    fig  = px.bar(df_h, x='value', y='label', orientation='h',
                  text='value', color_discrete_sequence=[color])
    fig.update_traces(
        textposition='outside',
        texttemplate='$%{text:,.0f}',
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>',
        marker=dict(line=dict(color='white', width=1))
    )
    lo = _lo(max(260, len(labels) * 34))
    lo['xaxis_title'] = None; lo['yaxis_title'] = None
    lo['bargap'] = 0.28; lo['margin'] = dict(l=10, r=80, t=16, b=10)
    fig.update_layout(**lo)
    fig.update_xaxes(tickformat='$,.0f')
    _cc(title, subtitle, fig)


c1, c2, c3 = st.columns(3)
with c1:
    _pie(rev_lab.index.tolist(), rev_lab.values.tolist(),
         "Revenue by Lab", "Share per laboratory")
with c2:
    _hist_h(rev_prov.index.tolist(), rev_prov.values.tolist(),
            "Revenue by Province", "Total revenue per province", color='#059669')
with c3:
    ct_labels = [c.replace(' Company','').replace(' Department','') for c in ct.index]
    _pie(ct_labels, ct.values.tolist(),
         "Revenue by Customer Type", "Private vs Government",
         colors=['#7c3aed','#059669','#f59e0b','#ef4444'])

render_footer()