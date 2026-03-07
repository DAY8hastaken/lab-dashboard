import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
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
check_login()
render_sidebar("Customer")

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
priv_c_m  = df[df['Customer Type']=='Private Company'].groupby(df['Service Date'].dt.month)['Organization'].nunique()
tot_by_m  = df.groupby(df['Service Date'].dt.month).size()
comp_r_m  = comp_by_m / tot_by_m * 100

to_m = end.month; fr_m = start.month; pr_m = to_m - 1

total_cust   = flt['Organization'].nunique()
total_comp   = int(flt['Complaint'].notna().sum())
total_priv_o = flt[flt['Customer Type']=='Private Company']['Organization'].nunique()
total_comp_r = flt['Complaint'].notna().mean() * 100 if n else 0

_skpi(None, [
    ('Customers',    f'Total {MN[fr_m]}–{MN[to_m]}', '#ff6b6b','#000', cust_by_m, total_cust,   'num', cust_by_m.get(pr_m,0), cust_by_m.get(to_m,0)),
    ('Complaints',   f'Total {MN[fr_m]}–{MN[to_m]}', '#ffd93d','#000', comp_by_m, total_comp,   'num', comp_by_m.get(pr_m,0), comp_by_m.get(to_m,0)),
    ('Private Orgs', f'Total {MN[fr_m]}–{MN[to_m]}', '#6bcb77','#000', priv_c_m,  total_priv_o, 'num', priv_c_m.get(pr_m,0),  priv_c_m.get(to_m,0)),
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
    _cc(title, subtitle, fig, h=300)


c1, c2, c3 = st.columns(3)

with c1:
    _pie_c(act_counts.index.tolist(), act_counts.values.tolist(),
           "Customers by Activity", "Organisation engagement status")

with c2:
    ot_labels, ot_vals = [], []
    for ctype in ot_by_ctype.index:
        short = ctype.replace(' Company','').replace(' Department','')
        for status in ['On-Time','Late']:
            if status in ot_by_ctype.columns:
                ot_labels.append(f"{short} {status}")
                ot_vals.append(int(ot_by_ctype.loc[ctype, status]))
    _pie_c(ot_labels, ot_vals,
           "On-Time vs Late", "By customer type",
           colors=['#059669','#ef4444','#34d399','#f87171','#a7f3d0','#fca5a5'])

with c3:
    _pie_c(comp_counts.index.tolist(), comp_counts.values.tolist(),
           "Complaint Breakdown", "Type and frequency",
           colors=['#e5e7eb','#ef4444','#f97316','#eab308','#3b82f6','#8b5cf6'])

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

# ── Daily Customers: New vs Repeat ──
st.markdown("### 👥 Daily Customers — New vs Repeat")

selected_date = end
daily_data    = df[df['Service Date'].dt.date == selected_date].copy()

if len(daily_data) > 0:
    customer_rows = []
    for customer in daily_data['Organization'].unique():
        today_count = len(daily_data[daily_data['Organization'] == customer])
        before_date = df[
            (df['Organization'] == customer) &
            (df['Service Date'].dt.date < selected_date)
        ]
        is_repeat = "Repeat" if len(before_date) > 0 else "New"
        badge     = "🟢" if is_repeat == "Repeat" else "🆕"
        customer_rows.append({
            "Status":        f"{badge} {is_repeat}",
            "Customer":      customer,
            "Samples Today": today_count,
            "Total Before":  len(before_date) if is_repeat == "Repeat" else "—"
        })

    customer_rows = sorted(customer_rows, key=lambda x: (x["Status"], x["Customer"]))

    table_html = (
        '<div style="background:#fff;border-radius:18px;box-shadow:0 4px 16px rgba(0,0,0,.07);overflow:hidden;margin-bottom:16px;">'
        '<div style="display:flex;padding:12px 16px;background:#f9fafb;border-bottom:2px solid #e5e7eb;">'
        '<span style="flex:1;font-size:.59rem;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:.07em;">Status</span>'
        '<span style="flex:2;font-size:.59rem;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:.07em;">Customer</span>'
        '<span style="flex:1;text-align:right;font-size:.59rem;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:.07em;">Today</span>'
        '<span style="flex:1;text-align:right;font-size:.59rem;font-weight:800;color:#111827;text-transform:uppercase;letter-spacing:.07em;">Before</span>'
        '</div>'
    )
    for ri, row in enumerate(customer_rows):
        bg = '#fafafa' if ri % 2 == 0 else '#fff'
        table_html += (
            f'<div style="display:flex;padding:11px 16px;background:{bg};border-bottom:1px solid #f3f4f6;align-items:center;">'
            f'<span style="flex:1;font-size:.82rem;font-weight:600;color:#111827;">{row["Status"]}</span>'
            f'<span style="flex:2;font-size:.82rem;font-weight:600;color:#374151;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{row["Customer"]}</span>'
            f'<span style="flex:1;text-align:right;font-size:.82rem;font-weight:700;color:#111827;">{row["Samples Today"]}</span>'
            f'<span style="flex:1;text-align:right;font-size:.82rem;font-weight:600;color:#6b7280;">{row["Total Before"]}</span>'
            f'</div>'
        )
    table_html += '</div>'
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("No customer activity on selected end date.")

render_footer()