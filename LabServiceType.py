import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _tbl, _cc, _page_header, _lo, BLK, MN
)
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="LabCare · Lab Service Type",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("LabServiceType")
render_sidebar("LabServiceType")

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Lab Service Type", "🧪 Lab Service Type",
             "Sample distribution across Basic, Standard and Premium service types per laboratory.")

start, end         = date_range_picker("labsvc", df)
flt, flt_params, n = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

# ── Aggregation ──
lab_service  = flt.groupby(['Laboratory','Service Type']).size().unstack(fill_value=0)
all_services = ['Basic','Standard','Premium']
svc_colors   = {'Basic': '#3b82f6', 'Standard': '#7c3aed', 'Premium': '#f59e0b'}

# ── KPI summary strip ──
total_basic    = int(flt[flt['Service Type']=='Basic'].shape[0])
total_standard = int(flt[flt['Service Type']=='Standard'].shape[0])
total_premium  = int(flt[flt['Service Type']=='Premium'].shape[0])
total_all      = total_basic + total_standard + total_premium

st.markdown(
    f'<div style="display:flex;gap:14px;margin:0 0 24px;flex-wrap:wrap;">'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #111827;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">All Samples</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#111827;margin-top:4px;">{total_all:,}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #3b82f6;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Basic</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#3b82f6;margin-top:4px;">{total_basic:,}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">{total_basic/total_all*100:.1f}% of total</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #7c3aed;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Standard</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#7c3aed;margin-top:4px;">{total_standard:,}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">{total_standard/total_all*100:.1f}% of total</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #f59e0b;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Premium</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#f59e0b;margin-top:4px;">{total_premium:,}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">{total_premium/total_all*100:.1f}% of total</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Charts row ──
ch1, ch2 = st.columns(2)

with ch1:
    # Stacked bar by lab
    rows_bar = []
    for lab in lab_service.index:
        for svc in all_services:
            rows_bar.append({
                'Laboratory': lab,
                'Service Type': svc,
                'Count': int(lab_service.loc[lab, svc]) if svc in lab_service.columns else 0
            })
    df_bar = pd.DataFrame(rows_bar)
    fig_bar = px.bar(
        df_bar, x='Count', y='Laboratory', color='Service Type',
        orientation='h', barmode='stack',
        color_discrete_map=svc_colors,
        text='Count',
    )
    fig_bar.update_traces(
        textposition='inside',
        texttemplate='%{text:,}',
        hovertemplate='<b>%{y}</b> · %{data.name}<br>%{x:,} samples<extra></extra>',
    )
    lo = _lo(max(260, len(lab_service.index) * 48))
    lo['xaxis_title'] = None; lo['yaxis_title'] = None
    lo['bargap'] = 0.28; lo['margin'] = dict(l=10, r=20, t=16, b=10)
    lo['legend'] = dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(size=10, color=BLK))
    fig_bar.update_layout(**lo)
    _cc("Samples by Lab — Stacked Service Type",
        f"Stacked count per lab ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})", fig_bar)

with ch2:
    # Pie of service type overall
    svc_dist = flt['Service Type'].value_counts()
    fig_pie  = px.pie(
        names=svc_dist.index.tolist(),
        values=svc_dist.values.tolist(),
        color=svc_dist.index.tolist(),
        color_discrete_map=svc_colors,
        hole=0.42,
    )
    fig_pie.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:,} samples<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2)),
    )
    lo2 = _lo(300)
    lo2['showlegend'] = True
    lo2['legend'] = dict(orientation='v', x=1.02, y=0.5,
                         font=dict(size=10, color=BLK), bgcolor='rgba(255,255,255,.9)')
    fig_pie.update_layout(**lo2)
    _cc("Service Type Distribution",
        f"Overall split across all labs ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
        fig_pie, h=300)

# ── Detailed table ──
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 16px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#3b82f6;text-transform:uppercase;letter-spacing:.14em;">🧪 Detailed Breakdown</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(59,130,246,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True
)

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

st.markdown(
    '<div style="background:linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%);'
    'border-radius:28px;padding:20px;'
    'box-shadow:0 4px 28px rgba(59,130,246,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(59,130,246,.15);">',
    unsafe_allow_html=True
)
_tbl(
    "Lab Samples by Service Type",
    f"Sample count: Basic / Standard / Premium  ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
    lab_service_rows, accent='#3b82f6',
    cols=['Laboratory','Basic','Standard','Premium','Total']
)
st.markdown('</div>', unsafe_allow_html=True)

render_footer()