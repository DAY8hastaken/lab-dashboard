import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    _inject_pie_spin,
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _cc, _tbl, _page_header, _lo, BLK
)
import plotly.express as px
import pandas as pd
from utils import _cc_pie
st.set_page_config(
    page_title="LabCare · Certificate Errors",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("CertError")
render_sidebar("CertError")
_inject_pie_spin()

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Certificate Errors", "⚠️ Certificate Errors",
             "Track which labs and organisations have certificate errors and how often they occur.")

start, end         = date_range_picker("certerr", df)
flt, flt_params, n = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

# ── Detect errors correctly ──
# A certificate error exists only when the field has a real non-empty value
def _has_error(val):
    if pd.isna(val):
        return False
    s = str(val).strip().lower()
    return s not in ('', 'nan', 'none', 'no', 'no error', '-', 'n/a')

err_mask = flt['Certificate Error'].apply(_has_error)
err_df   = flt[err_mask].copy()

total_errors  = len(err_df)
# Percentage = certificates with errors / total certificates issued (all rows with a cert date)
cert_issued   = flt['Certificate Date'].notna().sum()
# Fallback to total samples if cert dates are mostly empty
denom         = int(cert_issued) if cert_issued > 10 else n
error_rate    = (total_errors / denom * 100) if denom > 0 else 0
labs_affected = err_df['Laboratory'].nunique() if total_errors > 0 else 0
orgs_affected = err_df['Organization'].nunique() if total_errors > 0 else 0

# ── KPI strip ──
st.markdown(
    f'<div style="display:flex;gap:14px;margin:0 0 24px;flex-wrap:wrap;">'

    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #ef4444;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Errors</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#ef4444;margin-top:4px;">{total_errors:,}</div>'
    f'</div>'

    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #f97316;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Error Rate</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#f97316;margin-top:4px;">{error_rate:.2f}%</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">of {denom:,} certificates issued</div>'
    f'</div>'

    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #7c3aed;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Labs Affected</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#7c3aed;margin-top:4px;">{labs_affected}</div>'
    f'</div>'

    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #0ea5e9;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Organisations</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#0ea5e9;margin-top:4px;">{orgs_affected}</div>'
    f'</div>'

    f'</div>',
    unsafe_allow_html=True
)

if total_errors == 0:
    st.markdown(
        '<div style="background:#f0fdf4;border-radius:18px;padding:40px;text-align:center;'
        'border:1.5px solid #bbf7d0;margin-top:12px;">'
        '<div style="font-size:2.5rem;">✅</div>'
        '<div style="font-size:1rem;font-weight:700;color:#166534;margin-top:10px;">No certificate errors in this period</div>'
        '<div style="font-size:.8rem;color:#4ade80;margin-top:4px;">All certificates are clean</div>'
        '</div>',
        unsafe_allow_html=True
    )
    render_footer()
    st.stop()

# ── Charts ──
st.markdown(
    '<div style="background:linear-gradient(135deg,#fff7f7 0%,#fef2f2 100%);'
    'border-radius:28px;padding:24px;margin:4px 0 24px;'
    'box-shadow:0 4px 28px rgba(239,68,68,.09);'
    'border:1.5px solid rgba(239,68,68,.18);">',
    unsafe_allow_html=True
)

ch1, ch2 = st.columns(2)

with ch1:
    by_lab = err_df['Laboratory'].value_counts().reset_index()
    by_lab.columns = ['Laboratory', 'Errors']
    # Add error rate per lab
    lab_total = flt.groupby('Laboratory').size().rename('Total')
    by_lab    = by_lab.merge(lab_total, on='Laboratory', how='left')
    by_lab['Rate'] = (by_lab['Errors'] / by_lab['Total'] * 100).round(2)
    by_lab = by_lab.sort_values('Errors')

    fig_lab = px.bar(
        by_lab, x='Errors', y='Laboratory', orientation='h',
        text='Errors',
        color='Errors',
        color_continuous_scale=[[0,'#fca5a5'],[0.5,'#ef4444'],[1,'#7f1d1d']],
        custom_data=['Total','Rate'],
    )
    fig_lab.update_traces(
        textposition='outside',
        texttemplate='%{text:,}',
        hovertemplate='<b>%{y}</b><br>Errors: %{x:,}<br>Total samples: %{customdata[0]:,}<br>Rate: %{customdata[1]:.2f}%<extra></extra>',
    )
    lo1 = _lo(max(260, len(by_lab) * 52))
    lo1['xaxis_title'] = None; lo1['yaxis_title'] = None
    lo1['bargap'] = 0.3; lo1['margin'] = dict(l=10, r=70, t=16, b=10)
    lo1['coloraxis_showscale'] = False
    fig_lab.update_layout(**lo1)
    _cc("Errors by Laboratory",
        f"Count + hover shows rate per lab · {start.strftime('%d %b')} – {end.strftime('%d %b %Y')}",
        fig_lab, h=max(280, len(by_lab) * 52))

with ch2:
    by_org = err_df['Organization'].value_counts().head(10).reset_index()
    by_org.columns = ['Organization', 'Errors']
    by_org = by_org.sort_values('Errors')

    fig_org = px.bar(
        by_org, x='Errors', y='Organization', orientation='h',
        text='Errors',
        color='Errors',
        color_continuous_scale=[[0,'#fed7aa'],[0.5,'#f97316'],[1,'#7c2d12']],
    )
    fig_org.update_traces(
        textposition='outside',
        texttemplate='%{text:,}',
        hovertemplate='<b>%{y}</b><br>%{x:,} errors<extra></extra>',
    )
    lo2 = _lo(max(260, len(by_org) * 52))
    lo2['xaxis_title'] = None; lo2['yaxis_title'] = None
    lo2['bargap'] = 0.3; lo2['margin'] = dict(l=10, r=70, t=16, b=10)
    lo2['coloraxis_showscale'] = False
    fig_org.update_layout(**lo2)
    _cc("Top Organisations with Errors",
        f"Organisations with most certificate errors · top 10",
        fig_org, h=max(280, len(by_org) * 52))

st.markdown('</div>', unsafe_allow_html=True)

# ── Detail table ──
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#ef4444;text-transform:uppercase;letter-spacing:.14em;">📄 Error Records</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(239,68,68,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True
)

tbl_rows = []
for _, r in err_df.sort_values('Service Date', ascending=False).iterrows():
    tbl_rows.append({
        'Sample ID':         str(r.get('Sample ID', '')),
        'Service Date':      r['Service Date'].strftime('%d %b %Y') if pd.notna(r['Service Date']) else '—',
        'Laboratory':        str(r.get('Laboratory', '')),
        'Organisation':      str(r.get('Organization', '')),
        'Certificate Error': str(r.get('Certificate Error', '')),
    })

st.markdown(
    '<div style="background:linear-gradient(135deg,#fff7f7 0%,#fef2f2 100%);'
    'border-radius:28px;padding:20px;'
    'box-shadow:0 4px 28px rgba(239,68,68,.08);'
    'border:1.5px solid rgba(239,68,68,.15);">',
    unsafe_allow_html=True
)
_tbl(
    f"All Certificate Error Records  ({total_errors:,} total)",
    f"{start.strftime('%d %b')} – {end.strftime('%d %b %Y')} · searchable & sortable",
    tbl_rows,
    accent='#ef4444',
    cols=['Sample ID', 'Service Date', 'Laboratory', 'Organisation', 'Certificate Error'],
    key='cert_err_tbl',
)
st.markdown('</div>', unsafe_allow_html=True)

render_footer()