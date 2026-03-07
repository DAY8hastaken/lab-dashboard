import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _tbl, _page_header, MN
)
import pandas as pd

st.set_page_config(
    page_title="LabCare · Lab Count & Revenue",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("LabRevenue")
render_sidebar("LabRevenue")

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Lab Count & Revenue", "📊 Lab Count & Revenue",
             "Test count and estimated revenue per parameter per laboratory.")

start, end         = date_range_picker("labrev", df)
flt, flt_params, n = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

price_map = dict(zip(params_df['Parameter Name'], params_df['Cost per Parameter']))

# ── Build table ──
p_cnt = flt_params['Parameter'].value_counts().reset_index()
p_cnt.columns = ['Parameter', 'Count']
p_cnt['Cost']    = p_cnt['Parameter'].map(price_map).fillna(0)
p_cnt['Revenue'] = p_cnt['Count'] * p_cnt['Cost']
p_cnt = p_cnt.sort_values('Count', ascending=False)

lab_param  = flt_params.groupby(['Laboratory', 'Parameter']).size().unstack(fill_value=0)
all_params = p_cnt['Parameter'].tolist()
all_labs   = list(lab_param.index)
lab_rows   = []

for param in all_params:
    unit_cost   = price_map.get(param, 0)
    row         = {'Parameter': param, 'Unit Cost': f"${unit_cost:,.0f}"}
    total_count = 0
    for lab in all_labs:
        cnt_val           = int(lab_param.loc[lab, param]) if param in lab_param.columns else 0
        row[lab]          = f"{cnt_val:,}"
        row[f"{lab} Rev"] = f"${cnt_val * unit_cost:,.0f}"
        total_count      += cnt_val
    row['Total Count']   = f"{total_count:,}"
    row['Total Revenue'] = f"${total_count * unit_cost:,.0f}"
    lab_rows.append(row)

col_order = ['Parameter', 'Unit Cost']
for lab in all_labs:
    col_order += [lab, f"{lab} Rev"]
col_order += ['Total Count', 'Total Revenue']

# ── Summary KPI strip ──
total_revenue = sum(price_map.get(p, 0) * c for p, c in zip(p_cnt['Parameter'], p_cnt['Count']))
total_tests   = p_cnt['Count'].sum()
unique_params = len(p_cnt)
unique_labs   = len(all_labs)

st.markdown(
    f'<div style="display:flex;gap:14px;margin:20px 0 24px;flex-wrap:wrap;">'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #f59e0b;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Revenue</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">${total_revenue:,.0f}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #7c3aed;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Tests</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{total_tests:,}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #3b82f6;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Unique Parameters</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{unique_params:,}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #059669;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Laboratories</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{unique_labs}</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Table ──
st.markdown(
    '<div style="background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);'
    'border-radius:28px;padding:20px;'
    'box-shadow:0 4px 28px rgba(245,158,11,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(245,158,11,.15);">',
    unsafe_allow_html=True
)

_tbl(
    "Parameters by Laboratory — Count & Revenue",
    f"Test count and estimated revenue per parameter per lab  ({start.strftime('%d %b')} – {end.strftime('%d %b %Y')})",
    lab_rows, accent='#f59e0b', cols=col_order
)

st.markdown('</div>', unsafe_allow_html=True)

render_footer()