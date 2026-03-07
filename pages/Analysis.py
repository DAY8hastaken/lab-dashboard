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
    page_title="LabCare · NISTI Performance",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login()
render_sidebar("Analysis")

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / NISTI Performance", "🔬 NISTI Performance",
             "Laboratory turnaround · delay analysis · parameter testing · service types.")

start, end         = date_range_picker("nisti", df)
flt, flt_params, n = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

# ── KPI sparklines ──
price_map    = dict(zip(params_df['Parameter Name'], params_df['Cost per Parameter']))
param_cnt_m  = param_rows.groupby(param_rows['Service Date'].dt.month).size()
cost_m       = pd.Series({
    m: sum(price_map.get(p, 0) for p in param_rows[param_rows['Service Date'].dt.month == m]['Parameter'])
    for m in range(1, 13)
})
ot_cnt_m    = df[df['On time/Late']=='On-Time'].groupby(df['Service Date'].dt.month).size()
cert_late_m = df[df['cert_late_days'] > 0].groupby(df['Service Date'].dt.month).size()

to_m = end.month; fr_m = start.month; pr_m = to_m - 1

total_params     = len(flt_params)
total_cost       = sum(price_map.get(p, 0) for p in flt_params['Parameter'])
total_ot         = int((flt['On time/Late']=='On-Time').sum())
total_cert_late  = int((flt['cert_late_days'] > 0).sum())

_skpi(None, [
    ('Params Tested', f'Total {MN[fr_m]}–{MN[to_m]}', '#7c3aed','#000', param_cnt_m, total_params,    'num',    param_cnt_m.get(pr_m,0), param_cnt_m.get(to_m,0)),
    ('Total Cost',    f'Total {MN[fr_m]}–{MN[to_m]}', '#f59e0b','#000', cost_m,      total_cost,      'dollar', cost_m.get(pr_m,0),      cost_m.get(to_m,0)),
    ('Lab On-Time',   f'Total {MN[fr_m]}–{MN[to_m]}', '#059669','#000', ot_cnt_m,    total_ot,        'num',    ot_cnt_m.get(pr_m,0),    ot_cnt_m.get(to_m,0)),
    ('Cert Late',     f'Total {MN[fr_m]}–{MN[to_m]}', '#ef4444','#000', cert_late_m, total_cert_late, 'num',    cert_late_m.get(pr_m,0), cert_late_m.get(to_m,0)),
], start, end)

# ══════════════════════════════════════════════════ LAB BREAKDOWN ══
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#3b82f6;text-transform:uppercase;letter-spacing:.14em;">🧪 Laboratory Analysis</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(59,130,246,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True)

lab_service = flt.groupby(['Laboratory','Service Type']).size().unstack(fill_value=0)
lab_counts  = flt['Laboratory'].value_counts()

c_lab1, c_lab2 = st.columns(2)

with c_lab1:
    fig_pie_lab = px.pie(
        names=lab_counts.index.tolist(), values=lab_counts.values.tolist(),
        color_discrete_sequence=['#3b82f6','#7c3aed','#059669','#f59e0b','#ef4444'],
        hole=0.42
    )
    fig_pie_lab.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:,} samples<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )
    lo = _lo(300)
    lo['showlegend'] = True
    lo['legend'] = dict(orientation='v', x=1.02, y=0.5,
                        font=dict(size=10, color=BLK), bgcolor='rgba(255,255,255,.9)')
    fig_pie_lab.update_layout(**lo)
    _cc("Samples by Lab",
        f"Distribution per lab ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
        fig_pie_lab, h=300)

with c_lab2:
    service_dist = flt['Service Type'].value_counts()
    fig_pie_svc  = px.pie(
        names=service_dist.index.tolist(), values=service_dist.values.tolist(),
        color_discrete_sequence=['#059669','#7c3aed','#f59e0b'],
        hole=0.42
    )
    fig_pie_svc.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:,} tests<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )
    fig_pie_svc.update_layout(**lo)
    _cc("Service Type Distribution",
        f"Basic / Standard / Premium ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
        fig_pie_svc, h=300)

# ── Lab × Service Type table ──
st.markdown(
    '<div style="background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);'
    'border-radius:28px;padding:20px;margin:20px 0 0 0;'
    'box-shadow:0 4px 28px rgba(59,130,246,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(59,130,246,.15);">',
    unsafe_allow_html=True
)

all_services     = ['Basic','Standard','Premium']
lab_service_rows = []
for lab in lab_service.index:
    row   = {'Laboratory': lab}
    total = 0
    for svc in all_services:
        count    = int(lab_service.loc[lab, svc]) if svc in lab_service.columns else 0
        row[svc] = count
        total   += count
    row['Total'] = total
    lab_service_rows.append(row)

lab_service_rows.sort(key=lambda x: x['Total'], reverse=True)

_tbl("Lab Samples by Service Type",
     f"Sample count: Basic / Standard / Premium ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
     lab_service_rows, accent='#3b82f6',
     cols=['Laboratory','Basic','Standard','Premium','Total'])

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════ PARAMETER ANALYSIS ══
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#059669;text-transform:uppercase;letter-spacing:.14em;">🧬 Parameter Analysis</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(5,150,105,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True)

p_cnt = flt_params['Parameter'].value_counts().reset_index()
p_cnt.columns = ['Parameter','Count']
p_cnt['Cost']    = p_cnt['Parameter'].map(price_map).fillna(0)
p_cnt['Revenue'] = p_cnt['Count'] * p_cnt['Cost']
p_cnt = p_cnt.sort_values('Count', ascending=False)

top5_cnt = p_cnt.head(5).sort_values('Count')
top5_rev = p_cnt.sort_values('Revenue', ascending=False).head(5).sort_values('Revenue')

st.markdown(
    '<div style="background:linear-gradient(135deg,#f0fff8 0%,#ecfdf5 100%);'
    'border-radius:28px;padding:24px;margin:20px 0 24px 0;'
    'box-shadow:0 4px 28px rgba(5,150,105,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(5,150,105,.15);">',
    unsafe_allow_html=True
)

c3, c4 = st.columns(2)

with c3:
    fig_cnt = px.bar(
        x=top5_cnt['Count'], y=top5_cnt['Parameter'],
        orientation='h', text=top5_cnt['Count'],
        color_discrete_sequence=['#7c3aed'], labels={'x':'Tests','y':''}
    )
    fig_cnt.update_traces(
        textposition='outside', texttemplate='%{text:,}',
        hovertemplate='<b>%{y}</b><br>%{x:,} tests<extra></extra>',
        marker=dict(line=dict(color='white', width=1))
    )
    lo2 = _lo(260)
    lo2['xaxis_title'] = None; lo2['yaxis_title'] = None
    lo2['bargap'] = 0.28; lo2['margin'] = dict(l=10, r=60, t=16, b=10)
    fig_cnt.update_layout(**lo2)
    _cc("Top 5 Parameters by Count", "Most frequently tested", fig_cnt)

with c4:
    fig_rev = px.bar(
        x=top5_rev['Revenue'], y=top5_rev['Parameter'],
        orientation='h', text=[f"${v:,.0f}" for v in top5_rev['Revenue']],
        color_discrete_sequence=['#059669'], labels={'x':'Revenue','y':''}
    )
    fig_rev.update_traces(
        textposition='outside', texttemplate='%{text}',
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>',
        marker=dict(line=dict(color='white', width=1))
    )
    fig_rev.update_layout(**lo2)
    fig_rev.update_xaxes(tickformat='$,.0f')
    _cc("Top 5 Parameters by Revenue", "Highest earning parameters", fig_rev)

st.markdown('</div>', unsafe_allow_html=True)

# ── Parameters by Laboratory table ──
st.markdown(
    '<div style="background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);'
    'border-radius:28px;padding:20px;margin:20px 0 0 0;'
    'box-shadow:0 4px 28px rgba(245,158,11,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(245,158,11,.15);">',
    unsafe_allow_html=True
)

lab_param  = flt_params.groupby(['Laboratory','Parameter']).size().unstack(fill_value=0)
all_params = p_cnt['Parameter'].tolist()
all_labs   = list(lab_param.index)
lab_rows   = []

for param in all_params:
    unit_cost = price_map.get(param, 0)
    row = {'Parameter': param, 'Unit Cost': f"${unit_cost:,.0f}"}
    total_count = 0
    for lab in all_labs:
        cnt_val = int(lab_param.loc[lab, param]) if param in lab_param.columns else 0
        row[lab]          = f"{cnt_val:,}"
        row[f"{lab} Rev"] = f"${cnt_val * unit_cost:,.0f}"
        total_count      += cnt_val
    row['Total Count']   = f"{total_count:,}"
    row['Total Revenue'] = f"${total_count * unit_cost:,.0f}"
    lab_rows.append(row)

col_order = ['Parameter','Unit Cost']
for lab in all_labs:
    col_order += [lab, f"{lab} Rev"]
col_order += ['Total Count','Total Revenue']

_tbl("Parameters by Laboratory — Count & Revenue",
     "Test count and estimated revenue per parameter per lab",
     lab_rows, accent='#f59e0b', cols=col_order)

st.markdown('</div>', unsafe_allow_html=True)

render_footer()