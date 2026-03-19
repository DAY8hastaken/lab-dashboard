import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    _inject_pie_spin, _cc_pie,
    CSS, load_data, check_login, render_sidebar, render_footer,
    date_range_picker, apply_dr, _skpi, _cc, _page_header, _lo, BLK, MN
)
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="LabCare · Customer",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("Customer")
render_sidebar("Customer")
_inject_pie_spin()

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Customer", "👥 Customer",
             "Organisation activity, engagement and complaints.")

start, end = date_range_picker("cust", df)
flt, _, n  = apply_dr(df, param_rows, start, end)

if n == 0:
    st.info("No records found for the selected date range.")
    render_footer()
    st.stop()

# ── KPI sparklines ──
cust_by_m = df.groupby(df['Service Date'].dt.month)['Organization'].nunique()
comp_by_m = df[df['Complaint'].notna()].groupby(df['Service Date'].dt.month).size()
priv_c_m  = df[df['Customer Type'].isin(['Business Owner','Factory','Clean Water'])].groupby(df['Service Date'].dt.month)['Organization'].nunique()
tot_by_m  = df.groupby(df['Service Date'].dt.month).size()
comp_r_m  = comp_by_m / tot_by_m * 100

to_m = end.month; fr_m = start.month; pr_m = to_m - 1

total_cust   = flt['Organization'].nunique()
total_comp   = int(flt['Complaint'].notna().sum())
total_priv_o = flt[flt['Customer Type'].isin(['Business Owner','Factory','Clean Water'])]['Organization'].nunique()
total_comp_r = flt['Complaint'].notna().mean() * 100 if n else 0

_skpi(None, [
    ('Customers',    f'Total {MN[fr_m]}–{MN[to_m]}', '#ff6b6b','#000', cust_by_m, total_cust,   'num', cust_by_m.get(pr_m,0), cust_by_m.get(to_m,0)),
    ('Complaints',   f'Total {MN[fr_m]}–{MN[to_m]}', '#ffd93d','#000', comp_by_m, total_comp,   'num', comp_by_m.get(pr_m,0), comp_by_m.get(to_m,0)),
    ('Business/Factory', f'Total {MN[fr_m]}–{MN[to_m]}', '#6bcb77','#000', priv_c_m,  total_priv_o, 'num', priv_c_m.get(pr_m,0),  priv_c_m.get(to_m,0)),
    ('Complaint %',  f'Avg {MN[fr_m]}–{MN[to_m]}',   '#4d96ff','#000', comp_r_m,  total_comp_r, 'pct', comp_r_m.get(pr_m,0),  comp_r_m.get(to_m,0)),
], start, end)

# ── Charts ──
org_flt     = org_info[org_info['Organization'].isin(flt['Organization'].unique())].copy()
act_counts  = org_flt['Activity_Status'].value_counts()
ot_by_ctype = flt.groupby(['Customer Type','On time/Late']).size().unstack(fill_value=0)
comp_counts = flt['Complaint'].fillna('No Complaint').value_counts()
top_orgs    = flt['Organization'].value_counts().head(10).sort_values()


def _pie_c(labels, values, title, subtitle, colors=None):
    colors = colors or ['#7c3aed','#3b82f6','#059669','#f59e0b','#ef4444','#ec4899','#06b6d4','#a78bfa']
    fig = px.pie(names=labels, values=values,
                 color_discrete_sequence=colors, hole=0.42)
    fig.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )
    lo = _lo(300)
    lo['showlegend'] = True
    lo['legend'] = dict(orientation='v', x=1.02, y=0.5,
                        font=dict(size=10, color=BLK), bgcolor='rgba(255,255,255,.9)')
    fig.update_layout(**lo)
    _cc_pie(title, subtitle, fig, key=title, h=300)


c1, c2, c3 = st.columns(3)

with c1:
    _pie_c(act_counts.index.tolist(), act_counts.values.tolist(),
           "Customers by Activity", "Organisation engagement status")

with c2:
    _pie_c(comp_counts.index.tolist(), comp_counts.values.tolist(),
           "Complaint Breakdown", "Type and frequency",
           colors=['#e5e7eb','#ef4444','#f97316','#eab308','#3b82f6','#8b5cf6'])

with c3:
    # placeholder so layout stays balanced
    pass

# ── On-Time vs Late split into 2 big pies ──
st.markdown(
    '<div style="display:flex;align-items:center;gap:10px;margin:28px 0 14px;">'
    '<span style="font-size:.65rem;font-weight:900;color:#059669;text-transform:uppercase;letter-spacing:.14em;">⏱️ On-Time & Late by Customer Type</span>'
    '<div style="flex:1;height:1.5px;background:linear-gradient(90deg,rgba(5,150,105,.25),transparent);"></div>'
    '</div>', unsafe_allow_html=True
)

OT_COLORS  = ['#059669','#34d399','#10b981','#6ee7b7','#a7f3d0','#d1fae5',
              '#0d9488','#14b8a6','#2dd4bf','#5eead4','#99f6e4','#ccfbf1']
LATE_COLORS= ['#ef4444','#f87171','#fca5a5','#fecaca','#f97316','#fb923c',
              '#fdba74','#fed7aa','#dc2626','#b91c1c','#991b1b','#7f1d1d']

def _big_pie(title, subtitle, labels, values, colors, key, h=460):
    fig = px.pie(names=labels, values=values,
                 color_discrete_sequence=colors, hole=0.35)
    fig.update_traces(
        textposition='outside', textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>',
        marker=dict(line=dict(color='white', width=2)),
    )
    lo = _lo(h)
    lo['showlegend'] = True
    lo['legend'] = dict(
        orientation='v', yanchor='middle', y=0.5, xanchor='left', x=1.05,
        font=dict(size=11, color=BLK), bgcolor='rgba(255,255,255,.9)',
        bordercolor='rgba(0,0,0,.06)', borderwidth=1,
    )
    lo['margin'] = dict(l=40, r=220, t=40, b=40)
    fig.update_layout(**lo)
    uid = 'pie_' + key
    st.markdown('<div class="cc"><div class="cc-bar"></div>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="cc-title">{title}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="cc-sub">{subtitle}</p>', unsafe_allow_html=True)
    rot = st.slider('↻ Rotate', 0, 359, 0, step=3, key=uid, label_visibility='collapsed')
    for trace in fig.data:
        if hasattr(trace, 'rotation'):
            trace.rotation = rot
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':'hover','scrollZoom':False,'displaylogo':False})
    st.markdown('</div>', unsafe_allow_html=True)

ot_labels = ot_by_ctype.index.tolist()
ot_vals   = [int(ot_by_ctype.loc[c, 'On-Time']) if 'On-Time' in ot_by_ctype.columns else 0
             for c in ot_labels]
ot_labels_f = [l for l, v in zip(ot_labels, ot_vals) if v > 0]
ot_vals_f   = [v for v in ot_vals if v > 0]
_big_pie("✅ On-Time by Customer Type",
         "Samples delivered on time per customer type",
         ot_labels_f, ot_vals_f, OT_COLORS, key='ontime_ctype')

late_labels = ot_by_ctype.index.tolist()
late_vals   = [int(ot_by_ctype.loc[c, 'Late']) if 'Late' in ot_by_ctype.columns else 0
               for c in late_labels]
late_labels_f = [l for l, v in zip(late_labels, late_vals) if v > 0]
late_vals_f   = [v for v in late_vals if v > 0]
_big_pie("⚠️ Late by Customer Type",
         "Samples delivered late per customer type",
         late_labels_f, late_vals_f, LATE_COLORS, key='late_ctype')

# ── Top 10 Organisations bar ──
fig_orgs = px.bar(
    x=top_orgs.values, y=top_orgs.index,
    orientation='h', text=top_orgs.values,
    color_discrete_sequence=['#7c3aed'],
    labels={'x': 'Samples', 'y': ''}
)
fig_orgs.update_traces(
    textposition='outside', texttemplate='%{text:,}',
    hovertemplate='<b>%{y}</b><br>%{x:,} samples<extra></extra>',
    marker=dict(line=dict(color='white', width=1))
)
lo = _lo(max(280, len(top_orgs) * 34))
lo['xaxis_title'] = None; lo['yaxis_title'] = None
lo['bargap'] = 0.28; lo['margin'] = dict(l=10, r=60, t=16, b=10)
fig_orgs.update_layout(**lo)
_cc("Top 10 Organisations", "By sample volume", fig_orgs)

render_footer()