import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    fmt_riel,
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _tbl, _cc, _page_header, _lo, BLK, MN
)
import plotly.express as px
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

df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Lab Count & Revenue", "📊 Lab Count & Revenue",
             "Test count and revenue per parameter per laboratory — configure each lab's price rate below.")

start, end         = date_range_picker("labrev", df)
flt, flt_params, n = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

base_price_map = dict(zip(params_df['Parameter Name'], params_df['Cost per Parameter']))
all_labs       = sorted(flt['Laboratory'].unique().tolist())

# ── Helper: get multiplier directly from widget session key ──
def get_mult(lab):
    return float(st.session_state.get(f"mult_{lab}", 1.0))

# ── Initialise widget defaults on first load only ──
for lab in all_labs:
    key = f"mult_{lab}"
    if key not in st.session_state:
        st.session_state[key] = 1.0

# ══════════════════ PER-LAB PRICE MULTIPLIER CONFIG ══
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:8px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#7c3aed;text-transform:uppercase;letter-spacing:.14em;">⚙️ Lab Price Rate Configuration</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(124,58,237,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True
)

st.markdown(
    '<div style="background:#f5f3ff;border-radius:16px;padding:14px 18px;margin-bottom:10px;'
    'border:1.5px solid rgba(124,58,237,.18);font-size:.75rem;color:#4c1d95;">'
    '💡 <b>Set a price multiplier for each lab.</b> Base unit cost comes from the Parameter Price List. '
    'Revenue = count × base cost × lab multiplier. '
    'Adjust until numbers match your actual billing rates — table updates instantly.'
    '</div>', unsafe_allow_html=True
)

with st.expander("🔧 Configure lab multipliers", expanded=True):
    st.markdown(
        '<div style="font-size:.72rem;color:#6b7280;margin-bottom:12px;">'
        '1.0 = base price &nbsp;·&nbsp; 1.2 = 20% higher &nbsp;·&nbsp; 0.8 = 20% lower'
        '</div>', unsafe_allow_html=True
    )

    cols_per_row = 3
    lab_chunks   = [all_labs[i:i+cols_per_row] for i in range(0, len(all_labs), cols_per_row)]
    for chunk in lab_chunks:
        row_cols = st.columns(cols_per_row)
        for ci, lab in enumerate(chunk):
            with row_cols[ci]:
                # Widget writes directly to st.session_state[f"mult_{lab}"]
                st.number_input(
                    label=lab,
                    min_value=0.01, max_value=10.0,
                    step=0.05, format="%.2f",
                    key=f"mult_{lab}",
                    help=f"Price multiplier for {lab} — changes revenue calculations immediately"
                )


# Show active multiplier pills
active_mults = {lab: get_mult(lab) for lab in all_labs if abs(get_mult(lab) - 1.0) > 0.001}
if active_mults:
    pills = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 18px;">'
    for lab, v in active_mults.items():
        color = '#059669' if v > 1.0 else '#ef4444'
        arrow = '▲' if v > 1.0 else '▼'
        pills += (f'<span style="background:{color}18;border:1px solid {color}44;color:{color};'
                  f'border-radius:20px;padding:3px 10px;font-size:.68rem;font-weight:700;">'
                  f'{lab} {arrow} {v:.2f}×</span>')
    pills += '</div>'
    st.markdown(pills, unsafe_allow_html=True)
else:
    st.markdown(
        '<div style="font-size:.7rem;color:#9ca3af;margin:6px 0 18px;">All labs at base rate 1.0×</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════ BUILD DATA ══
lab_param_cnt = flt_params.groupby(['Laboratory', 'Parameter']).size().unstack(fill_value=0)
all_params    = sorted(flt_params['Parameter'].unique().tolist(),
                       key=lambda p: -flt_params[flt_params['Parameter'] == p].shape[0])

def _cnt(lab, param):
    if lab in lab_param_cnt.index and param in lab_param_cnt.columns:
        return int(lab_param_cnt.loc[lab, param])
    return 0

# Build table rows — reads multipliers fresh from session state
lab_rows = []
for param in all_params:
    base  = base_price_map.get(param, 0)
    row   = {'Parameter': param, 'Base Cost': fmt_riel(base)}
    g_cnt = 0; g_rev = 0.0
    for lab in all_labs:
        mult = get_mult(lab)
        eff  = base * mult
        cnt  = _cnt(lab, param)
        rev  = cnt * eff
        row[f"{lab} Count"]   = f"{cnt:,}"
        row[f"{lab} Rate"]    = fmt_riel(eff)
        row[f"{lab} Revenue"] = fmt_riel(rev)
        g_cnt += cnt
        g_rev += rev
    row['Total Count']   = f"{g_cnt:,}"
    row['Total Revenue'] = fmt_riel(g_rev)
    lab_rows.append(row)

col_order = ['Parameter', 'Base Cost']
for lab in all_labs:
    col_order += [f"{lab} Count", f"{lab} Rate", f"{lab} Revenue"]
col_order += ['Total Count', 'Total Revenue']

total_revenue = sum(
    base_price_map.get(p, 0) * get_mult(lab) * _cnt(lab, p)
    for p in all_params for lab in all_labs
)
total_tests = flt_params.shape[0]

# ── KPI strip ──
st.markdown(
    f'<div style="display:flex;gap:14px;margin:0 0 24px;flex-wrap:wrap;">'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;border-top:4px solid #f59e0b;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Revenue</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{total_revenue*4000:,.0f} ៛</div>'
    f'<div style="font-size:.65rem;color:#9ca3af;margin-top:2px;">with lab rate adjustments</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;border-top:4px solid #7c3aed;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Tests</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{total_tests:,}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;border-top:4px solid #3b82f6;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Parameters</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{len(all_params):,}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:140px;background:#fff;border-radius:18px;padding:18px 20px;border-top:4px solid #059669;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Laboratories</div>'
    f'<div style="font-size:1.6rem;font-weight:900;color:#111827;margin-top:4px;">{len(all_labs)}</div>'
    f'</div>'
    f'</div>', unsafe_allow_html=True
)

# ── Revenue by lab chart ──
lab_rev_summary = []
for lab in all_labs:
    mult    = get_mult(lab)
    lab_rev = sum(base_price_map.get(p, 0) * mult * _cnt(lab, p) for p in all_params)
    lab_cnt = int(lab_param_cnt.loc[lab].sum()) if lab in lab_param_cnt.index else 0
    lab_rev_summary.append({
        'Laboratory': lab,
        'Revenue':    lab_rev * 4000,
        'Tests':      lab_cnt,
        'Rate':       f"{mult:.2f}×"
    })

df_chart = pd.DataFrame(lab_rev_summary).sort_values('Revenue', ascending=True)
fig_rev  = px.bar(
    df_chart, x='Revenue', y='Laboratory', orientation='h',
    text='Revenue', color='Revenue',
    color_continuous_scale=[[0,'#ddd6fe'],[0.5,'#7c3aed'],[1,'#2e1065']],
    custom_data=['Tests','Rate'],
)
fig_rev.update_traces(
    textposition='outside', texttemplate='%{text:,.0f}៛',
    hovertemplate='<b>%{y}</b><br>Revenue: %{x:,.0f}៛<br>Tests: %{customdata[0]:,}<br>Multiplier: %{customdata[1]}<extra></extra>',
)
lo_r = _lo(max(260, len(all_labs) * 52))
lo_r['xaxis_title'] = None; lo_r['yaxis_title'] = None
lo_r['bargap'] = 0.3; lo_r['margin'] = dict(l=10, r=90, t=16, b=10)
lo_r['xaxis'] = dict(ticksuffix='៛', tickformat=',.0f')
lo_r['coloraxis_showscale'] = False
fig_rev.update_layout(**lo_r)
_cc("Revenue by Laboratory (adjusted rates)",
    "Hover to see test count and multiplier per lab",
    fig_rev, h=max(280, len(all_labs) * 52))

# ── Detailed table ──
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#f59e0b;text-transform:uppercase;letter-spacing:.14em;">📋 Parameter Breakdown</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(245,158,11,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True
)
st.markdown(
    '<div style="background:linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%);'
    'border-radius:28px;padding:20px;'
    'box-shadow:0 4px 28px rgba(245,158,11,.09);'
    'border:1.5px solid rgba(245,158,11,.15);">',
    unsafe_allow_html=True
)
_tbl(
    "Parameters by Laboratory — Count & Adjusted Revenue",
    f"Base Cost × Lab Multiplier × Count = Revenue  ·  {start.strftime('%d %b')} – {end.strftime('%d %b %Y')}",
    lab_rows, accent='#f59e0b', cols=col_order
)
st.markdown('</div>', unsafe_allow_html=True)

render_footer()