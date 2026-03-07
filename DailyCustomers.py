import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils import (
    CSS, load_data, check_login, render_sidebar, render_footer,
    _page_header
)
import pandas as pd

st.set_page_config(
    page_title="LabCare · Daily Customers",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(CSS, unsafe_allow_html=True)
check_login("DailyCustomers")
render_sidebar("DailyCustomers")

# ══════════════════════════════════════════════════════════ PAGE ══════
df, params_df, param_rows, org_info = load_data()

_page_header("Pages / Daily Customers", "👥 Daily Customers — New vs Repeat",
             "See which customers visited on a selected date and whether they are new or returning.")

MIN_DATE = df['Service Date'].min().date()
MAX_DATE = df['Service Date'].max().date()

# ── Date picker ──
st.markdown(
    '<div style="background:#fff;border-radius:20px;padding:20px 24px;margin-bottom:24px;'
    'box-shadow:0 4px 20px rgba(124,58,237,.09);border-top:4px solid #7c3aed;">',
    unsafe_allow_html=True
)
st.markdown('<span style="font-size:.7rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Select Date</span>', unsafe_allow_html=True)
selected_date = st.date_input(
    "", value=MAX_DATE, min_value=MIN_DATE, max_value=MAX_DATE,
    key="dc_date", label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ── Compute ──
daily_data = df[df['Service Date'].dt.date == selected_date].copy()

if len(daily_data) == 0:
    st.info(f"No customer activity on {selected_date.strftime('%d %b %Y')}.")
    render_footer()
    st.stop()

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
        "_sort":         is_repeat,
        "Customer":      customer,
        "Samples Today": today_count,
        "Total Before":  len(before_date) if is_repeat == "Repeat" else 0,
    })

customer_rows = sorted(customer_rows, key=lambda x: (x["_sort"], x["Customer"]))

total_new    = sum(1 for r in customer_rows if r["_sort"] == "New")
total_repeat = sum(1 for r in customer_rows if r["_sort"] == "Repeat")
total_cust   = len(customer_rows)
total_samp   = sum(r["Samples Today"] for r in customer_rows)

# ── KPI strip ──
st.markdown(
    f'<div style="display:flex;gap:14px;margin-bottom:24px;flex-wrap:wrap;">'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #7c3aed;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Customers</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#111827;margin-top:4px;">{total_cust}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">{selected_date.strftime("%d %b %Y")}</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #059669;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">🟢 Repeat</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#059669;margin-top:4px;">{total_repeat}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">returning customers</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #3b82f6;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">🆕 New</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#3b82f6;margin-top:4px;">{total_new}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">first-time customers</div>'
    f'</div>'
    f'<div style="flex:1;min-width:130px;background:#fff;border-radius:18px;padding:18px 20px;'
    f'border-top:4px solid #f59e0b;box-shadow:0 2px 12px rgba(0,0,0,.06);">'
    f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;">Total Samples</div>'
    f'<div style="font-size:1.7rem;font-weight:900;color:#111827;margin-top:4px;">{total_samp}</div>'
    f'<div style="font-size:.65rem;color:#6b7280;margin-top:2px;">submitted today</div>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# ── Table ──
st.markdown(
    '<div style="background:linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%);'
    'border-radius:28px;padding:20px;'
    'box-shadow:0 4px 28px rgba(124,58,237,.09),0 1px 4px rgba(0,0,0,.04);'
    'border:1.5px solid rgba(124,58,237,.15);">',
    unsafe_allow_html=True
)

table_html = (
    '<div style="background:#fff;border-radius:18px;box-shadow:0 4px 16px rgba(0,0,0,.07);overflow:hidden;margin-bottom:0;">'
    '<div style="padding:14px 16px 10px;background:#fff;border-bottom:1px solid #f3f4f6;">'
    f'<span style="font-size:.85rem;font-weight:800;color:#111827;">Customer Activity</span>'
    f'<span style="font-size:.63rem;color:#9ca3af;display:block;margin-top:2px;">{selected_date.strftime("%A, %d %B %Y")} · {total_cust} customers · {total_samp} samples</span>'
    '</div>'
    '<div style="display:flex;padding:10px 16px;background:#f9fafb;border-bottom:2px solid #e5e7eb;">'
    '<span style="flex:1;font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;">Status</span>'
    '<span style="flex:3;font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;">Customer</span>'
    '<span style="flex:1;text-align:right;font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;">Samples Today</span>'
    '<span style="flex:1;text-align:right;font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.07em;">Total Before</span>'
    '</div>'
)

for ri, row in enumerate(customer_rows):
    bg        = '#fafafa' if ri % 2 == 0 else '#fff'
    is_new    = row["_sort"] == "New"
    val_color = '#6b7280' if row["Total Before"] == 0 else '#111827'
    val_str   = '—' if row["Total Before"] == 0 else f'{row["Total Before"]:,}'
    table_html += (
        f'<div style="display:flex;padding:12px 16px;background:{bg};border-bottom:1px solid #f3f4f6;align-items:center;">'
        f'<span style="flex:1;">'
        f'<span style="display:inline-flex;align-items:center;gap:5px;background:{"#dcfce7" if not is_new else "#dbeafe"};'
        f'color:{"#065f46" if not is_new else "#1e40af"};font-size:.72rem;font-weight:800;'
        f'padding:3px 10px;border-radius:20px;">{row["Status"]}</span>'
        f'</span>'
        f'<span style="flex:3;font-size:.82rem;font-weight:600;color:#374151;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:12px;">{row["Customer"]}</span>'
        f'<span style="flex:1;text-align:right;font-size:.82rem;font-weight:800;color:#111827;">{row["Samples Today"]}</span>'
        f'<span style="flex:1;text-align:right;font-size:.82rem;font-weight:600;color:{val_color};">{val_str}</span>'
        f'</div>'
    )

table_html += '</div>'
st.markdown(table_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

render_footer()