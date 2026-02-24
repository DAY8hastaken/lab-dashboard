import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="LabCare Dashboard", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700;9..40,800;9..40,900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f0f2f8}

/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(175deg,#0a0820 0%,#130e3d 50%,#1c1548 100%)!important;border-right:none!important;box-shadow:6px 0 32px rgba(0,0,0,.45)!important}
[data-testid="stSidebar"] *{color:#b8b0e8!important;font-family:'DM Sans',sans-serif!important}
[data-testid="stSidebar"] .stButton button{background:transparent!important;border:none!important;border-radius:12px!important;padding:11px 14px!important;font-size:.88rem!important;font-weight:500!important;color:#b8b0e8!important;width:100%!important;text-align:left!important;font-family:'DM Sans',sans-serif!important;box-shadow:none!important;transition:all .22s cubic-bezier(.34,1.56,.64,1)!important}
[data-testid="stSidebar"] .stButton button:hover{background:rgba(255,255,255,.08)!important;color:#fff!important;transform:translateX(5px)!important}
[data-testid="stSidebar"] .stButton button:focus{box-shadow:none!important;outline:none!important;border:none!important}
[data-testid="stSidebar"] .nav-active-wrap .stButton button{background:rgba(124,58,237,.22)!important;color:#fff!important;font-weight:700!important;border-left:3px solid #a78bfa!important;border-radius:0 12px 12px 0!important;padding-left:13px!important}
[data-testid="stSidebar"] .nav-active-wrap .stButton button:hover{background:rgba(124,58,237,.30)!important;transform:none!important}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:1px!important}
[data-testid="stSidebar"] .stButton{margin:0 6px!important}
[data-testid="collapsedControl"],button[kind="header"]{display:none!important}
.nav-active-wrap{position:relative}
.nav-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(124,58,237,.32);border:1px solid rgba(167,139,250,.35);border-radius:20px;padding:2px 9px 2px 7px;font-size:.55rem;font-weight:800;color:#c4b5f4!important;letter-spacing:.09em;text-transform:uppercase;margin:0 8px 5px 8px}
.nav-dot{width:6px;height:6px;border-radius:50%;background:#a78bfa;box-shadow:0 0 7px 2px rgba(167,139,250,.75);animation:pulse 1.9s ease-in-out infinite;flex-shrink:0}
.slogo{padding:24px 18px 18px;border-bottom:1px solid rgba(124,58,237,.18);margin-bottom:8px}
.slogo-title{font-size:1.1rem;font-weight:900;color:#fff!important;display:flex;align-items:center;gap:9px}
.slogo-pill{background:rgba(124,58,237,.3);color:#c4b5f4!important;font-size:.55rem!important;font-weight:800!important;padding:2px 8px;border-radius:20px;letter-spacing:.1em}
.slogo-sub{font-size:.6rem;color:rgba(184,176,232,.32)!important;margin-top:5px}

/* Date picker */
.dr-card{background:#fff;border-radius:24px;padding:22px 26px 20px;margin-bottom:32px;box-shadow:0 6px 32px rgba(124,58,237,.10),0 1px 4px rgba(0,0,0,.04);animation:fadeUp .38s cubic-bezier(.22,1,.36,1) both;position:relative;overflow:hidden}
.dr-card::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,#7c3aed 0%,#3b82f6 25%,#06b6d4 50%,#059669 75%,#f59e0b 100%);border-radius:24px 24px 0 0}
.dr-blob1{position:absolute;top:-30px;right:-30px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(124,58,237,.07),transparent 70%);pointer-events:none}
.dr-blob2{position:absolute;bottom:-20px;left:-20px;width:90px;height:90px;border-radius:50%;background:radial-gradient(circle,rgba(5,150,105,.06),transparent 70%);pointer-events:none}
.dr-header{display:flex;align-items:center;margin-bottom:14px}
.dr-title{font-size:.72rem;font-weight:900;color:#111827;text-transform:uppercase;letter-spacing:.14em;display:flex;align-items:center;gap:8px}
.dr-title-pill{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff!important;font-size:.55rem;font-weight:800;padding:2px 9px;border-radius:20px;letter-spacing:.08em;box-shadow:0 2px 8px rgba(124,58,237,.35)}
.dr-pill-btn .stButton button{background:linear-gradient(135deg,#f5f3ff,#ede9fe)!important;border:1.5px solid #ddd6fe!important;border-radius:20px!important;padding:5px 16px!important;font-size:.7rem!important;font-weight:700!important;color:#5b21b6!important;min-width:0!important;width:auto!important;transition:all .2s cubic-bezier(.34,1.56,.64,1)!important;box-shadow:none!important;font-family:'DM Sans',sans-serif!important}
.dr-pill-btn .stButton button:hover{background:linear-gradient(135deg,#7c3aed,#6d28d9)!important;color:#fff!important;border-color:#7c3aed!important;transform:translateY(-2px)!important;box-shadow:0 6px 16px rgba(124,58,237,.3)!important}
.dr-pill-btn .stButton button:focus{outline:none!important;box-shadow:none!important}
.dr-field-label{font-size:.6rem;font-weight:800;text-transform:uppercase;letter-spacing:.13em;margin-bottom:6px;display:flex;align-items:center;gap:6px}
.lbl-from{color:#7c3aed}.lbl-to{color:#059669}
.lbl-dot{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0}
.lbl-dot-from{background:linear-gradient(135deg,#7c3aed,#a78bfa);box-shadow:0 0 6px rgba(124,58,237,.5)}
.lbl-dot-to{background:linear-gradient(135deg,#059669,#34d399);box-shadow:0 0 6px rgba(5,150,105,.5)}
[data-testid="stDateInputField"] input{border-radius:12px!important;border:2px solid #e8e0fc!important;font-family:'DM Sans',sans-serif!important;font-weight:700!important;font-size:.85rem!important;padding:9px 14px!important;color:#111827!important;background:#fafafe!important;transition:all .22s ease!important}
[data-testid="stDateInputField"] input:focus{border-color:#7c3aed!important;background:#fff!important;box-shadow:0 0 0 4px rgba(124,58,237,.13)!important;outline:none!important}
.dr-arrow-wrap{display:flex;align-items:center;justify-content:center;padding-top:26px}
.dr-arrow-icon{font-size:1.4rem;color:#c4b5f4;animation:arrowBounce 2s ease-in-out infinite}
@keyframes arrowBounce{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.dr-summary{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1.5px solid #a7f3d0;border-radius:14px;padding:10px 16px;margin-top:14px}
.dr-sum-from{font-size:.78rem;font-weight:800;color:#065f46}
.dr-sum-arrow{color:#34d399;font-size:1.1rem}
.dr-sum-to{font-size:.78rem;font-weight:800;color:#065f46}
.dr-sum-days{font-size:.68rem;font-weight:600;color:#6b7280}
.dr-sum-badge{margin-left:auto;background:linear-gradient(135deg,#059669,#10b981);color:#fff!important;font-size:.65rem;font-weight:800;padding:4px 12px;border-radius:20px;letter-spacing:.07em;box-shadow:0 3px 10px rgba(5,150,105,.3);white-space:nowrap}

/* KPI cards */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:18px}
.kpi-card{background:#fff;border-radius:20px;padding:20px 20px 16px;box-shadow:0 2px 14px rgba(0,0,0,.07);opacity:0;animation:fadeUp .5s cubic-bezier(.22,1,.36,1) both;transition:transform .3s cubic-bezier(.34,1.56,.64,1),box-shadow .3s;position:relative;overflow:hidden}
.kpi-card:nth-child(1){animation-delay:.04s}.kpi-card:nth-child(2){animation-delay:.10s}.kpi-card:nth-child(3){animation-delay:.16s}.kpi-card:nth-child(4){animation-delay:.22s}
.kpi-card:hover{transform:translateY(-7px);box-shadow:0 18px 40px rgba(61,32,128,.14)}
.kpi-accent{position:absolute;top:0;left:0;right:0;height:3px;border-radius:20px 20px 0 0}
.kpi-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:13px}
.kpi-label{font-size:.62rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.11em}
.kpi-icon{width:44px;height:44px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:20px}
.kpi-value{font-size:1.78rem;font-weight:900;color:#111827;line-height:1.05;margin-bottom:7px;letter-spacing:-.04em}
.kpi-sub{font-size:.7rem;color:#6b7280;font-weight:500}
.pos{color:#059669!important;font-weight:700!important}
.neg{color:#dc2626!important;font-weight:700!important}

/* Chart cards */
.cc{background:#fff;border-radius:20px;padding:20px 18px 12px;box-shadow:0 2px 12px rgba(0,0,0,.06);margin-bottom:14px;opacity:0;animation:fadeUp .55s cubic-bezier(.22,1,.36,1) both;transition:transform .28s,box-shadow .28s;position:relative;overflow:hidden}
.cc-bar{position:absolute;top:0;left:0;right:0;height:3px;border-radius:20px 20px 0 0;background:linear-gradient(90deg,#7c3aed,#3b82f6,#059669);opacity:0;transition:opacity .3s}
.cc:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(61,32,128,.12)}
.cc:hover .cc-bar{opacity:1}
.cc-title{font-size:.92rem;font-weight:800;color:#111827;margin-bottom:2px}
.cc-sub{font-size:.66rem;color:#9ca3af;font-weight:500;margin-bottom:8px}

/* ── Global sparkline card iframe rounding — legacy, kept for safety ── */

/* ═══════════════════════════════════════════
   OVERVIEW — Excel data display
═══════════════════════════════════════════ */
.ov-header{background:#fff;border-radius:24px;padding:28px 32px 24px;margin-bottom:16px;box-shadow:0 4px 24px rgba(0,0,0,.07);position:relative;overflow:hidden;animation:fadeUp .4s cubic-bezier(.22,1,.36,1) both}
.ov-header::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,#7c3aed,#3b82f6,#06b6d4,#059669,#f59e0b);border-radius:24px 24px 0 0}
.ov-head-row{display:flex;align-items:center;gap:16px;margin-bottom:20px}
.ov-head-icon{width:54px;height:54px;border-radius:16px;background:linear-gradient(135deg,#7c3aed,#4f46e5);display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 8px 24px rgba(124,58,237,.38);flex-shrink:0;animation:iconFloat 3s ease-in-out infinite}
@keyframes iconFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.ov-head-title{font-size:1.4rem;font-weight:900;color:#111827;letter-spacing:-.04em}
.ov-head-sub{font-size:.74rem;color:#6b7280;margin-top:3px}
.ov-quick-stats{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.oq{background:#f8f9fc;border-radius:14px;padding:14px 16px;border:1.5px solid #f0eeff;text-align:center;transition:all .25s cubic-bezier(.34,1.56,.64,1);animation:fadeUp .5s cubic-bezier(.22,1,.36,1) both;position:relative;overflow:hidden;cursor:default}
.oq:nth-child(1){animation-delay:.05s}.oq:nth-child(2){animation-delay:.10s}.oq:nth-child(3){animation-delay:.15s}
.oq:nth-child(4){animation-delay:.20s}.oq:nth-child(5){animation-delay:.25s}.oq:nth-child(6){animation-delay:.30s}
.oq:hover{background:#fff;transform:translateY(-4px);box-shadow:0 10px 28px rgba(124,58,237,.12);border-color:#ddd6fe}
.oq::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;border-radius:0 0 14px 14px}
.oq-c1::after{background:linear-gradient(90deg,#7c3aed,#a78bfa)}
.oq-c2::after{background:linear-gradient(90deg,#059669,#34d399)}
.oq-c3::after{background:linear-gradient(90deg,#f59e0b,#fbbf24)}
.oq-c4::after{background:linear-gradient(90deg,#ef4444,#f87171)}
.oq-c5::after{background:linear-gradient(90deg,#3b82f6,#60a5fa)}
.oq-c6::after{background:linear-gradient(90deg,#ec4899,#f9a8d4)}
.oq-icon{font-size:1.3rem;margin-bottom:5px}
.oq-val{font-size:1.25rem;font-weight:900;color:#111827;letter-spacing:-.04em;line-height:1.1}
.oq-lbl{font-size:.58rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;margin-top:3px}

/* data table card */
.tbl-card{background:#fff;border-radius:20px;padding:22px 22px 16px;box-shadow:0 2px 16px rgba(0,0,0,.07);margin-bottom:14px;opacity:0;animation:fadeUp .5s cubic-bezier(.22,1,.36,1) both}
.tbl-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px}
.tbl-title{font-size:1rem;font-weight:800;color:#111827}
.tbl-sub{font-size:.66rem;color:#9ca3af;font-weight:500;margin-top:2px}
.tbl-badge{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff!important;font-size:.64rem;font-weight:800;padding:4px 12px;border-radius:20px;letter-spacing:.07em;box-shadow:0 2px 8px rgba(124,58,237,.3)}

/* filter chips row */
.chip-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.chip{display:inline-flex;align-items:center;gap:5px;background:#f5f3ff;border:1.5px solid #ddd6fe;border-radius:20px;padding:4px 12px;font-size:.68rem;font-weight:700;color:#5b21b6;cursor:default}
.chip-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}

/* Streamlit dataframe */
[data-testid="stDataFrame"]{border-radius:14px!important;overflow:hidden!important}
[data-testid="stDataFrame"] iframe{border-radius:14px!important}
[data-testid="stDataFrame"] *{color:#111827!important}
[data-testid="stDataFrame"] > div{background:#fff!important;border-radius:14px!important}
[data-testid="stDataFrame"] th{background:#f8f9fc!important;color:#111827!important;font-weight:700!important;border-bottom:2px solid #e8ebf2!important}
[data-testid="stDataFrame"] td{background:#fff!important;color:#111827!important;border-bottom:1px solid #f0f2f8!important}
[data-testid="stDataFrame"] tr:hover td{background:#f8f9fc!important}

/* Month comparison card */
.mc-card{background:#fff;border-radius:22px;padding:24px 28px 20px;box-shadow:0 4px 24px rgba(0,0,0,.07);margin-bottom:18px;position:relative;overflow:hidden;animation:fadeUp .45s cubic-bezier(.22,1,.36,1) both}
.mc-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;border-radius:22px 22px 0 0;background:linear-gradient(90deg,#7c3aed,#3b82f6,#059669)}

/* Force st.metric black text */
[data-testid="stMetricLabel"]{color:#111827!important;font-weight:700!important}
[data-testid="stMetricValue"]{color:#111827!important;font-weight:900!important}
[data-testid="stMetricDelta"]{font-weight:700!important}
[data-testid="stMetricDelta"] svg{display:none!important}
[data-testid="metric-container"]{background:#f8f9fc!important;border-radius:14px!important;padding:16px!important;border:1.5px solid #ede9fe!important}

/* Page header */
.ph{margin-bottom:20px;padding-bottom:14px;border-bottom:1.5px solid #e8ebf2;animation:slideIn .38s ease both}
.ph-bc{font-size:.61rem;color:#9ca3af;margin-bottom:3px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.ph h1{font-size:1.55rem!important;font-weight:900!important;color:#111827!important;margin:0 0 4px!important;letter-spacing:-.04em!important}
.ph-sub{font-size:.76rem;color:#6b7280}

#MainMenu,footer,header{visibility:hidden}
.block-container{padding:.7rem 1.3rem 1rem!important}
h1,h2,h3,h4{color:#111827!important}
[data-testid="stTooltipIcon"]{display:none!important}

@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes slideIn{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:translateX(0)}}
@keyframes pulse{0%,100%{box-shadow:0 0 4px 1px rgba(167,139,250,.55)}50%{box-shadow:0 0 11px 4px rgba(167,139,250,.95)}}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════ DATA ══════
@st.cache_data
def load_data():
    df = pd.read_excel("Lab_Service_2025_2000rows_MergedOrg.xlsx", sheet_name="Service Data")
    params = pd.read_excel("Lab_Service_2025_2000rows_MergedOrg.xlsx", sheet_name="Parameter Price List")
    for col in ['Service Date','Sample Received Date','Testing Start Date','Certificate Date','Payment Date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df['Testing Completion Date'] = pd.to_datetime(df['Testing Completion Date'], errors='coerce')
    df['Month']      = df['Service Date'].dt.month
    df['Year']       = df['Service Date'].dt.year
    df['Month_Name'] = df['Service Date'].dt.strftime('%b')
    df['delay_days']       = (df['Certificate Date'] - df['Sample Received Date']).dt.days
    df['receive_to_start'] = (df['Testing Start Date'] - df['Sample Received Date']).dt.days
    df['test_duration']    = (df['Testing Completion Date'] - df['Testing Start Date']).dt.days
    today = pd.Timestamp('2025-12-31')
    oi = df.groupby('Organization').agg(last_visit=('Service Date','max'), total_visits=('Service Date','count')).reset_index()
    def classify(r):
        m = (today - r['last_visit']).days / 30.44
        if m <= 4 and r['total_visits'] >= 2: return 'Active'
        elif m <= 7:  return '>4 months'
        elif m <= 13: return '>7 months'
        elif m <= 24: return '>13 months'
        else:         return '>2 years'
    oi['Activity_Status'] = oi.apply(classify, axis=1)
    df2 = df.merge(oi[['Organization','Activity_Status','total_visits','last_visit']], on='Organization', how='left')
    rows = []
    for _, row in df2.iterrows():
        if pd.notna(row['Parameters Tested']):
            for p in str(row['Parameters Tested']).split(','):
                p = p.strip()
                if p:
                    rows.append({'Laboratory':row['Laboratory'],'Month':row['Month'],'Month_Name':row['Month_Name'],
                                 'Parameter':p,'Customer Type':row['Customer Type'],'Province':row['Province'],
                                 'Year':row['Year'],'Service Date':row['Service Date']})
    return df2, params, pd.DataFrame(rows), oi

df, params_df, param_rows, org_info = load_data()
MIN_DATE = df['Service Date'].min().date()
MAX_DATE = df['Service Date'].max().date()
MONTH_ORD = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'Jun':5,'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11}
C_PURPLE = ['#7c3aed','#9f5ff0','#b87df5','#d4aef9','#5b21b6']
C_GREEN  = ['#064e3b','#059669','#34d399','#6ee7b7']
C_MIXED  = ['#7c3aed','#059669','#f59e0b','#ef4444','#3b82f6','#ec4899']
C_WARM   = ['#ef4444','#f97316','#f59e0b','#22c55e','#14b8a6','#3b82f6','#8b5cf6','#ec4899','#06b6d4','#10b981','#6366f1','#f43f5e']
BLK = "#111827"


# ════════════════════════════════════════════════════════ SIDEBAR ══════
NAV_ITEMS = [("💰","Revenue"),("👥","Customer"),("🔬","Laboratory"),("🧬","Parameter")]
if 'section' not in st.session_state: st.session_state.section = "Revenue"

with st.sidebar:
    st.markdown('<div class="slogo"><div class="slogo-title">🧪 LabCare <span class="slogo-pill">2025</span></div><div class="slogo-sub">Analytics Dashboard · 2,000 records</div></div>', unsafe_allow_html=True)
    for icon, name in NAV_ITEMS:
        is_active = st.session_state.section == name
        if is_active:
            st.markdown('<div class="nav-active-wrap"><span class="nav-badge"><span class="nav-dot"></span>Viewing now</span>', unsafe_allow_html=True)
        if st.button(f"{icon}  {name}", key=f"nav_{name}", use_container_width=True):
            st.session_state.section = name
            st.rerun()
        if is_active:
            st.markdown('</div>', unsafe_allow_html=True)

section = st.session_state.section


# ═══════════════════════════════════════════════════ DATE PICKER ══════
def date_range_picker(key_prefix):
    sk, se = f"dr_{key_prefix}_s", f"dr_{key_prefix}_e"
    if sk not in st.session_state: st.session_state[sk] = MIN_DATE
    if se not in st.session_state: st.session_state[se] = MAX_DATE

    st.markdown('<div class="dr-card"><div class="dr-blob1"></div><div class="dr-blob2"></div><div class="dr-header"><div class="dr-title">📅 Date Range <span class="dr-title-pill">FILTER</span></div></div>', unsafe_allow_html=True)

    c_pill, _ = st.columns([1, 7])
    with c_pill:
        st.markdown('<div class="dr-pill-btn">', unsafe_allow_html=True)
        if st.button("All data", key=f"{key_prefix}_all"):
            st.session_state[sk] = MIN_DATE
            st.session_state[se] = MAX_DATE
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    ca, arrowcol, cb = st.columns([5, .7, 5])
    with ca:
        st.markdown('<div class="dr-field-label lbl-from"><span class="lbl-dot lbl-dot-from"></span>From</div>', unsafe_allow_html=True)
        start = st.date_input("f", value=st.session_state[sk], min_value=MIN_DATE, max_value=MAX_DATE, key=f"{key_prefix}_s2", label_visibility="collapsed")
    with arrowcol:
        st.markdown('<div class="dr-arrow-wrap"><span class="dr-arrow-icon">→</span></div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="dr-field-label lbl-to"><span class="lbl-dot lbl-dot-to"></span>To</div>', unsafe_allow_html=True)
        end = st.date_input("t", value=st.session_state[se], min_value=MIN_DATE, max_value=MAX_DATE, key=f"{key_prefix}_e2", label_visibility="collapsed")

    st.session_state[sk] = start
    st.session_state[se] = end
    if end < start: start, end = end, start

    days = (end - start).days + 1
    cnt  = len(df[(df['Service Date'] >= pd.Timestamp(start)) & (df['Service Date'] <= pd.Timestamp(end))])
    st.markdown(f'<div class="dr-summary"><span class="dr-sum-from">{start.strftime("%d %b %Y")}</span><span class="dr-sum-arrow">→</span><span class="dr-sum-to">{end.strftime("%d %b %Y")}</span><span class="dr-sum-days">· {days} days</span><span class="dr-sum-badge">✦ {cnt:,} samples</span></div></div>', unsafe_allow_html=True)
    return start, end


# ═══════════════════════════════════════════════════ HELPERS ══════
_seq = [0]
def _sm(d, col='Month_Name'):
    d = d.copy(); d['_o'] = d[col].map(MONTH_ORD); return d.sort_values('_o').drop(columns='_o')
def _lo(h=230):
    return dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans',color=BLK,size=11),height=h,margin=dict(l=10,r=10,t=16,b=10),
        xaxis=dict(gridcolor='rgba(0,0,0,.05)',zeroline=False,showline=False,tickfont=dict(size=10,color=BLK),title_font=dict(size=11,color=BLK)),
        yaxis=dict(gridcolor='rgba(0,0,0,.05)',zeroline=False,showline=False,tickfont=dict(size=10,color=BLK),title_font=dict(size=11,color=BLK)),
        legend=dict(font=dict(size=10,color=BLK),bgcolor='rgba(255,255,255,.92)',bordercolor='rgba(0,0,0,.06)',borderwidth=1,orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1),
        transition=dict(duration=400,easing='cubic-in-out'),bargap=0.22,bargroupgap=0.06)
def _cc(title, sub, fig, h=None):
    if h: fig.update_layout(height=h)
    _seq[0] += 1; delay = min(_seq[0]*.07, .65)
    st.markdown(f'<div class="cc" style="animation-delay:{delay:.2f}s"><div class="cc-bar"></div><div class="cc-title">{title}</div><div class="cc-sub">{sub}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
def kcard(icon, bg, accent, value, label, sub=''):
    return f'<div class="kpi-card"><div class="kpi-accent" style="background:{accent}"></div><div class="kpi-top"><div class="kpi-label">{label}</div><div class="kpi-icon" style="background:{bg}">{icon}</div></div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'
def _bar(d,x,y,colors=C_PURPLE,orient='v',h=230,xl=None,yl=None):
    fig = px.bar(d,x=y,y=x,orientation='h',color_discrete_sequence=colors,text_auto='.2s') if orient=='h' else px.bar(d,x=x,y=y,color_discrete_sequence=colors,text_auto=True)
    lo = _lo(h); lo['showlegend'] = False
    if xl: lo['xaxis']['title'] = dict(text=xl,font=dict(size=11,color=BLK))
    if yl: lo['yaxis']['title'] = dict(text=yl,font=dict(size=11,color=BLK))
    fig.update_layout(**lo); fig.update_traces(textposition='outside',textfont=dict(color=BLK,size=9),marker_line_width=0); return fig
def _bargrp(d,x,y,color,cmap=None,barmode='group',h=230,xl=None,yl=None):
    kw = dict(color_discrete_map=cmap) if cmap else dict(color_discrete_sequence=C_MIXED)
    fig = px.bar(d,x=x,y=y,color=color,barmode=barmode,text_auto=True,**kw); lo = _lo(h)
    if xl: lo['xaxis']['title'] = dict(text=xl,font=dict(size=11,color=BLK))
    if yl: lo['yaxis']['title'] = dict(text=yl,font=dict(size=11,color=BLK))
    fig.update_layout(**lo); fig.update_traces(textposition='outside',textfont=dict(color=BLK,size=9),marker_line_width=0); return fig
def _donut(d,names,values,colors=C_PURPLE,h=230):
    fig = px.pie(d,names=names,values=values,color_discrete_sequence=colors,hole=0.54)
    fig.update_layout(**_lo(h)); fig.update_traces(textinfo='percent+label',textfont=dict(color=BLK,size=10),insidetextorientation='radial'); return fig
def _area(d,x,y,color='#7c3aed',h=230,xl=None,yl=None):
    r,g,b = int(color[1:3],16),int(color[3:5],16),int(color[5:7],16)
    fig = go.Figure(go.Scatter(x=d[x],y=d[y],mode='lines+markers',line=dict(color=color,width=2.8),marker=dict(size=7,color=color,line=dict(color='white',width=2)),fill='tozeroy',fillcolor=f'rgba({r},{g},{b},.10)',hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>'))
    lo = _lo(h); lo['showlegend'] = False
    if xl: lo['xaxis']['title'] = dict(text=xl,font=dict(size=11,color=BLK))
    if yl: lo['yaxis']['title'] = dict(text=yl,font=dict(size=11,color=BLK))
    fig.update_layout(**lo); return fig
def _hist(d,x,color='#7c3aed',nbins=12,h=215,xl=None):
    fig = px.histogram(d,x=x,nbins=nbins,color_discrete_sequence=[color])
    lo = _lo(h); lo['showlegend'] = False
    if xl: lo['xaxis']['title'] = dict(text=xl,font=dict(size=11,color=BLK))
    lo['yaxis']['title'] = dict(text='Samples',font=dict(size=11,color=BLK))
    fig.update_layout(**lo); fig.update_traces(marker_line_width=.6,marker_line_color='white'); return fig
def _tbl(title, subtitle, rows, accent='#7c3aed', cols=None):
    RANK_COLORS = ['#7c3aed','#9f5ff0','#c4b5f4','#ddd6fe','#ede9fe']
    parts = []
    parts.append(f'<div style="background:#fff;border-radius:18px;box-shadow:0 2px 16px rgba(0,0,0,.07);overflow:hidden;margin-bottom:16px;border-top:4px solid {accent};">')
    parts.append(f'<div style="padding:14px 14px 10px;border-bottom:1px solid #f3f4f6;">')
    parts.append(f'<span style="font-size:.85rem;font-weight:800;color:#111827;display:block;">{title}</span>')
    parts.append(f'<span style="font-size:.63rem;color:#9ca3af;display:block;margin-top:2px;">{subtitle}</span>')
    parts.append('</div>')

    if cols:
        # header row
        parts.append('<div style="display:flex;padding:8px 14px;border-bottom:2px solid #f3f4f6;background:#f9fafb;">')
        for ci, c in enumerate(cols):
            align = 'left' if ci == 0 else 'right'
            flex  = '2' if ci == 0 else '1'
            parts.append(f'<span style="flex:{flex};text-align:{align};font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.08em;">{c}</span>')
        parts.append('</div>')
        # data rows
        for ri, row in enumerate(rows):
            bg = '#fafafa' if ri % 2 == 0 else '#fff'
            parts.append(f'<div style="display:flex;padding:9px 14px;background:{bg};border-bottom:1px solid #f3f4f6;">')
            for ci, c in enumerate(cols):
                align = 'left' if ci == 0 else 'right'
                flex  = '2' if ci == 0 else '1'
                fw    = '700' if ci == 0 else '600'
                color = '#374151' if ci == 0 else '#111827'
                val   = row.get(c, '—')
                parts.append(f'<span style="flex:{flex};text-align:{align};font-size:.76rem;font-weight:{fw};color:{color};overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{val}</span>')
            parts.append('</div>')
    else:
        for ri, row in enumerate(rows):
            label    = row[0]
            val      = row[1]
            sub      = row[2] if len(row) > 2 else ''
            dot_col  = RANK_COLORS[min(ri, len(RANK_COLORS)-1)]
            bg       = '#fafafa' if ri % 2 == 0 else '#fff'
            parts.append(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:{bg};border-bottom:1px solid #f3f4f6;">')
            parts.append(f'<div style="display:flex;align-items:center;gap:8px;min-width:0;flex:1;">')
            parts.append(f'<span style="width:7px;height:7px;border-radius:50%;background:{dot_col};flex-shrink:0;display:inline-block;"></span>')
            parts.append(f'<span style="min-width:0;">')
            parts.append(f'<span style="display:block;font-size:.78rem;font-weight:600;color:#374151;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{label}</span>')
            if sub:
                parts.append(f'<span style="display:block;font-size:.6rem;color:#9ca3af;margin-top:1px;">{sub}</span>')
            parts.append('</span>')
            parts.append('</div>')
            parts.append(f'<span style="font-size:.92rem;font-weight:800;color:#111827;white-space:nowrap;margin-left:12px;">{val}</span>')
            parts.append('</div>')

    parts.append('</div>')
    st.markdown(''.join(parts), unsafe_allow_html=True)


def apply_dr(s, e):
    ts, te = pd.Timestamp(s), pd.Timestamp(e)
    flt = df[(df['Service Date']>=ts)&(df['Service Date']<=te)].copy()
    fp  = param_rows[(param_rows['Service Date']>=ts)&(param_rows['Service Date']<=te)].copy()
    return flt, fp, len(flt)

MN = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
      7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

def _mom_card(end_date, metrics):
    if end_date.month == 1:
        return
    cur_m  = end_date.month
    prev_m = cur_m - 1
    cur_n  = MN[cur_m]
    prev_n = MN[prev_m]

    def _fmt(v, fmt):
        if fmt == 'dollar': return f'${v:,.0f}'
        if fmt == 'pct':    return f'{v:.1f}%'
        if fmt == 'days':   return f'{v:.1f}d'
        return f'{int(v):,}'

    def _badge(cur, prev, fmt):
        if prev == 0: return '—', '#6b7280', '#f3f4f6'
        d = (cur - prev) / prev * 100
        arrow = '▲' if d >= 0 else '▼'
        bg  = '#dcfce7' if d >= 0 else '#fee2e2'
        col = '#059669' if d >= 0 else '#dc2626'
        suffix = ' pp' if fmt == 'pct' else '%'
        return f'{arrow} {abs(d):.1f}{suffix}', col, bg

    st.markdown(
        f'<div style="background:#fff;border-radius:20px;padding:18px 24px 20px;'
        f'box-shadow:0 3px 18px rgba(0,0,0,.07);margin-bottom:16px;border-top:4px solid #7c3aed;">'
        f'<p style="margin:0 0 14px;font-size:.72rem;font-weight:900;color:#111827;'
        f'text-transform:uppercase;letter-spacing:.12em;">'
        f'📅 Month-on-Month &nbsp;'
        f'<span style="background:#7c3aed;color:#fff;font-size:.6rem;font-weight:800;'
        f'padding:2px 9px;border-radius:20px;">{cur_n} vs {prev_n}</span>'
        f'<span style="float:right;font-size:.62rem;color:#9ca3af;font-weight:500;">'
        f'To date: {end_date.strftime("%d %b %Y")}</span></p>',
        unsafe_allow_html=True
    )
    cols = st.columns(len(metrics))
    for col_st, (icon, label, cur_val, prev_val, fmt) in zip(cols, metrics):
        badge_lbl, badge_tc, badge_bg = _badge(cur_val, prev_val, fmt)
        with col_st:
            st.markdown(
                f'<div style="background:#f8f9fc;border-radius:14px;padding:16px 18px;border:1.5px solid #ede9fe;">'
                f'<div style="font-size:.6rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.12em;margin-bottom:6px;">{icon} {label} — {cur_n}</div>'
                f'<div style="font-size:1.7rem;font-weight:900;color:#111827;letter-spacing:-.04em;line-height:1.1;margin-bottom:8px;">{_fmt(cur_val, fmt)}</div>'
                f'<span style="display:inline-block;padding:3px 10px;border-radius:8px;font-size:.72rem;font-weight:800;background:{badge_bg};color:{badge_tc};">{badge_lbl}</span>'
                f'<div style="margin-top:10px;font-size:.63rem;color:#6b7280;">vs {prev_n}: <b style="color:#111827;">{_fmt(prev_val, fmt)}</b></div>'
                f'</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div><div style="margin-bottom:4px;"></div>', unsafe_allow_html=True)


# ── SPARKLINE KPI CARDS — pure HTML + inline SVG ─────────────────────────
# Renders ALL 4 cards inside a single unified outer container box.
# SVG sparklines are built manually so everything stays inside one st.markdown().

def _make_sparkline_svg(vals, accent, fmt, card_uid, from_m=1, to_m=12, width=300, height=70):
    """
    SVG sparkline with native SVG tooltip (rect+text shown on hover via CSS).
    No JS DOM traversal — works reliably inside Streamlit's iframe.
    """
    import math
    MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    def _fmtv(v, f):
        if f == 'dollar': return f'${v:,.0f}'
        if f == 'pct':    return f'{v:.1f}%'
        if f == 'days':   return f'{v:.1f}d'
        return f'{int(v):,}'

    if not vals or max(vals) == min(vals):
        ys = [height * 0.5] * len(vals)
    else:
        mn, mx = min(vals), max(vals)
        pad = 10
        ys = [pad + (1 - (v - mn) / (mx - mn)) * (height - pad * 2) for v in vals]

    n  = len(vals)
    xs = [i / (n - 1) * width for i in range(n)]

    def ctrl(p0, p1, p2, t=0.28):
        d01 = math.hypot(p1[0]-p0[0], p1[1]-p0[1])
        d12 = math.hypot(p2[0]-p1[0], p2[1]-p1[1])
        fa  = t * d01 / (d01 + d12 + 1e-9)
        fb  = t * d12 / (d01 + d12 + 1e-9)
        c1x = p1[0] - fa*(p2[0]-p0[0]); c1y = p1[1] - fa*(p2[1]-p0[1])
        c2x = p1[0] + fb*(p2[0]-p0[0]); c2y = p1[1] + fb*(p2[1]-p0[1])
        return (c1x,c1y),(c2x,c2y)

    pts = list(zip(xs, ys))
    d   = f'M {pts[0][0]:.1f},{pts[0][1]:.1f}'
    for k in range(1, len(pts)):
        p0 = pts[k-2] if k>=2 else pts[0]
        p1 = pts[k-1]; p2 = pts[k]
        p3 = pts[k+1] if k+1<len(pts) else pts[-1]
        _, c1 = ctrl(p0, p1, p2)
        c2, _ = ctrl(p1, p2, p3)
        d += f' C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'

    area_d  = d + f' L {xs[-1]:.1f},{height} L {xs[0]:.1f},{height} Z'
    grad_id = f'sg_{card_uid}'

    # Build per-point hover groups: invisible wide hit rect + visible dot + tooltip box
    # Uses CSS :hover on a <g> so it's sandboxed-iframe-safe (no JS needed)
    hover_groups = ''
    tip_h = 26   # tooltip box height in SVG units

    # inject CSS for the hover groups inside a <style> in the SVG
    css_rules = f'<style>\n'
    for k in range(n):
        gid = f'hp_{card_uid}_{k}'
        css_rules += (
            f'#{gid} .spk-dot {{ opacity:0; transition:opacity .12s; }}\n'
            f'#{gid} .spk-tip  {{ opacity:0; transition:opacity .12s; }}\n'
            f'#{gid}:hover .spk-dot {{ opacity:1; }}\n'
            f'#{gid}:hover .spk-tip  {{ opacity:1; }}\n'
        )
    css_rules += '</style>\n'

    for k in range(n):
        gid    = f'hp_{card_uid}_{k}'
        mon    = MONTHS[k]
        lbl    = _fmtv(vals[k], fmt)
        tip_txt = f'{mon}: {lbl}'
        tip_w  = max(len(tip_txt) * 7 + 16, 72)

        # position tooltip: flip left if near right edge
        tip_x = xs[k] - tip_w / 2
        if tip_x < 2: tip_x = 2
        if tip_x + tip_w > width - 2: tip_x = width - tip_w - 2
        tip_y = ys[k] - tip_h - 8
        if tip_y < 2: tip_y = ys[k] + 10

        # vertical guideline x position
        hover_groups += f'''
<g id="{gid}" style="cursor:crosshair;">
  <!-- wide invisible hit area -->
  <rect x="{xs[k]-13:.1f}" y="0" width="26" height="{height}" fill="transparent"/>
  <!-- vertical dashed guide line (shown on hover) -->
  <line class="spk-tip" x1="{xs[k]:.1f}" y1="0" x2="{xs[k]:.1f}" y2="{height}"
        stroke="{accent}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
  <!-- dot -->
  <circle class="spk-dot" cx="{xs[k]:.1f}" cy="{ys[k]:.1f}" r="4"
          fill="{accent}" stroke="white" stroke-width="2"/>
  <!-- tooltip bubble -->
  <g class="spk-tip">
    <rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w}" height="{tip_h}"
          rx="6" ry="6" fill="#1e1b4b" opacity="0.92"/>
    <text x="{tip_x + tip_w/2:.1f}" y="{tip_y + 17:.1f}"
          text-anchor="middle" fill="white"
          font-size="11" font-weight="700" font-family="DM Sans,sans-serif">{tip_txt}</text>
  </g>
</g>'''

    svg = f'''<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none"
    style="width:100%;height:{height}px;display:block;overflow:visible;">
  {css_rules}
  <defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{accent}" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <path d="{area_d}" fill="url(#{grad_id})"/>
  <path d="{d}" fill="none" stroke="{accent}" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{xs[from_m-1]:.1f}"  cy="{ys[from_m-1]:.1f}"  r="3.5" fill="{accent}" stroke="white" stroke-width="2"/>
  <circle cx="{xs[to_m-1]:.1f}" cy="{ys[to_m-1]:.1f}" r="3.5" fill="{accent}" stroke="white" stroke-width="2"/>
  {hover_groups}
</svg>'''
    return svg


def _skpi(cols_st, cards, start_date, end_date):
    """
    Combined KPI + MoM card row.
    cards = list of (title, subtitle, _bg, _lc, mseries, cur_val, fmt, prev_val)
    prev_val is the previous month value for MoM badge. Pass 0 if N/A.
    """
    from_m = start_date.month
    to_m   = end_date.month
    ACCENTS = ['#7c3aed','#3b82f6','#059669','#f59e0b']

    def _fmt(v, fmt):
        if fmt == 'dollar': return f'${v:,.0f}'
        if fmt == 'pct':    return f'{v:.1f}%'
        if fmt == 'days':   return f'{v:.1f}d'
        return f'{int(v):,}'

    def _badge(cur, prev, fmt):
        if prev == 0: return '', '', ''
        d = (cur - prev) / prev * 100
        arrow = '▲' if d >= 0 else '▼'
        bg  = '#dcfce7' if d >= 0 else '#fee2e2'
        col = '#059669' if d >= 0 else '#dc2626'
        suffix = ' pp' if fmt == 'pct' else '%'
        return f'{arrow} {abs(d):.1f}{suffix}', col, bg

    period_lbl = MN[to_m] if from_m == to_m else f'{MN[from_m]} » {MN[to_m]}'
    prev_m_lbl = MN[to_m - 1] if to_m > 1 else ''

    inner_cards = []
    for i, card in enumerate(cards):
        # unpack — support 7, 8, or 9-tuple
        if len(card) == 9:
            title, subtitle, _bg, _lc, mseries, total_val, fmt, prev_val, cur_m_val = card
        elif len(card) == 8:
            title, subtitle, _bg, _lc, mseries, total_val, fmt, prev_val = card
            cur_m_val = total_val
        else:
            title, subtitle, _bg, _lc, mseries, total_val, fmt = card
            prev_val = 0; cur_m_val = total_val

        accent   = ACCENTS[i % len(ACCENTS)]
        val_str  = _fmt(total_val, fmt)
        vals     = [float(mseries.get(m, 0)) for m in range(1, 13)]
        card_uid = f'c{i}_{to_m}_{title[:3].replace(" ","")}'
        svg      = _make_sparkline_svg(vals, accent, fmt, card_uid, from_m=from_m, to_m=to_m)
        delay    = 0.06 + i * 0.09

        bdg_lbl, bdg_col, bdg_bg = _badge(cur_m_val, prev_val, fmt)
        prev_str = _fmt(prev_val, fmt) if prev_val else '—'

        # MoM row — only render if we have a prev value and prev month exists
        mom_html = ''
        if bdg_lbl and prev_m_lbl:
            mom_html = f'''
  <div style="display:flex;align-items:center;gap:8px;margin-top:10px;padding-top:10px;
              border-top:1px dashed rgba(0,0,0,.07);">
    <span style="display:inline-flex;align-items:center;gap:4px;
                 background:{bdg_bg};color:{bdg_col};
                 font-size:.7rem;font-weight:800;padding:3px 10px;border-radius:20px;">
      {bdg_lbl}
    </span>
    <span style="font-size:.65rem;color:#9ca3af;font-weight:500;">
      vs {prev_m_lbl}: <b style="color:#6b7280;">{prev_str}</b>
    </span>
  </div>'''

        cur_m_str = _fmt(cur_m_val, fmt)

        card_html = f'''
<div style="
    flex:1; min-width:0;
    background:#fff;
    border-radius:24px;
    overflow:visible;
    box-shadow:0 2px 16px rgba(0,0,0,.07);
    display:flex; flex-direction:column;
    transition:transform .28s cubic-bezier(.34,1.56,.64,1), box-shadow .28s;
    animation:fadeUp .5s cubic-bezier(.22,1,.36,1) {delay:.2f}s both;
    position:relative;
    border-top: 5px solid {accent};
" onmouseenter="this.style.transform='translateY(-6px)';this.style.boxShadow='0 18px 40px rgba(0,0,0,.13)'"
   onmouseleave="this.style.transform='';this.style.boxShadow='0 2px 16px rgba(0,0,0,.07)'">
  <div style="padding:20px 20px 14px;">
    <!-- label + period pill -->
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
      <span style="font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.13em;">{title}</span>
      <span style="font-size:.56rem;font-weight:700;color:#a78bfa;background:#f5f3ff;padding:2px 8px;border-radius:20px;">{period_lbl}</span>
    </div>
    <!-- big value + small end-month pill -->
    <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:3px;">
      <span style="font-size:2rem;font-weight:900;color:#111827;letter-spacing:-.05em;line-height:1.05;">{val_str}</span>
      <span style="font-size:.72rem;font-weight:700;color:{accent};background:rgba({','.join(str(int(accent[j:j+2],16)) for j in (1,3,5))},0.10);
                   padding:2px 9px;border-radius:20px;white-space:nowrap;letter-spacing:-.01em;">
        {MN[to_m]}: {cur_m_str}
      </span>
    </div>
    <!-- subtitle -->
    <div style="font-size:.68rem;color:#9ca3af;font-weight:500;">{subtitle}</div>
    <!-- MoM badge row -->
    {mom_html}
    <!-- sparkline -->
    <div style="margin-top:12px;">{svg}</div>
  </div>
</div>'''
        inner_cards.append(card_html)

    cards_joined = '\n'.join(inner_cards)

    outer = f'''
<div style="
    background:linear-gradient(135deg,#faf9ff 0%,#f4f6ff 50%,#f0fff8 100%);
    border-radius:28px;
    padding:20px;
    margin-top:24px;
    margin-bottom:20px;
    box-shadow:0 4px 28px rgba(124,58,237,.09), 0 1px 4px rgba(0,0,0,.04);
    border:1.5px solid rgba(167,139,250,.15);
    animation:fadeUp .4s cubic-bezier(.22,1,.36,1) both;
">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
    <span style="font-size:.6rem;font-weight:900;color:#7c3aed;text-transform:uppercase;letter-spacing:.14em;">📊 Key Metrics</span>
    <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(124,58,237,.18),transparent);"></div>
    <span style="font-size:.58rem;font-weight:700;color:#9ca3af;">{period_lbl}</span>
  </div>
  <div style="display:flex;gap:14px;">
    {cards_joined}
  </div>
</div>
'''
    st.markdown(outer, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════ PAGES ══

# ── 💰 REVENUE ──────────────────────────────────────────────────────────────
if section == "Revenue":
    _seq[0] = 0
    st.markdown('<div class="ph"><div class="ph-bc">Pages / Revenue</div><h1>💰 Revenue</h1><div class="ph-sub">Financial performance by lab, province and customer type.</div></div>', unsafe_allow_html=True)
    start, end = date_range_picker("rev"); flt, _, n = apply_dr(start, end)
    if n == 0: st.info("No records found for the selected date range.")
    else:
        rev_by_m   = df.groupby(df['Service Date'].dt.month)['Revenue'].sum()
        cnt_by_m   = df.groupby(df['Service Date'].dt.month).size()
        priv_by_m  = df[df['Customer Type']=='Private Company'].groupby(df['Service Date'].dt.month)['Revenue'].sum()
        ot_by_m    = df[df['On time/Late']=='On-Time'].groupby(df['Service Date'].dt.month).size() / cnt_by_m * 100

        to_m = end.month
        fr_m = start.month
        pr_m = to_m - 1

        # ── Big number = TOTAL across the selected date range (from flt)
        total_rev  = flt['Revenue'].sum()
        total_cnt  = len(flt)
        total_priv = flt[flt['Customer Type']=='Private Company']['Revenue'].sum()
        total_ot   = (flt['On time/Late']=='On-Time').mean()*100 if len(flt) else 0

        # ── MoM: compare end month vs previous month (for badge)
        prev_rev  = rev_by_m.get(pr_m, 0)
        prev_cnt  = cnt_by_m.get(pr_m, 0)
        prev_priv = priv_by_m.get(pr_m, 0)
        prev_ot   = ot_by_m.get(pr_m, 0)
        cur_rev   = rev_by_m.get(to_m, 0)
        cur_cnt   = cnt_by_m.get(to_m, 0)
        cur_priv  = priv_by_m.get(to_m, 0)
        cur_ot    = ot_by_m.get(to_m, 0)

        k1, k2, k3, k4 = st.columns(4)
        _skpi([k1,k2,k3,k4], [
            ('Revenue',     f'Total {MN[fr_m]}–{MN[to_m]}',    '#ff6b6b', '#000', rev_by_m,  total_rev,  'dollar', prev_rev,  cur_rev),
            ('Samples',     f'Total {MN[fr_m]}–{MN[to_m]}',    '#ffd93d', '#000', cnt_by_m,  total_cnt,  'num',    prev_cnt,  cur_cnt),
            ('Private Rev', f'Total {MN[fr_m]}–{MN[to_m]}',    '#6bcb77', '#000', priv_by_m, total_priv, 'dollar', prev_priv, cur_priv),
            ('On-Time %',   f'Avg {MN[fr_m]}–{MN[to_m]}',      '#4d96ff', '#000', ot_by_m,   total_ot,   'pct',    prev_ot,   cur_ot),
        ], start, end)

        cur_m  = end.month; cur_y = end.year

        # ── Revenue by Lab ──
        rev_lab = flt.groupby('Laboratory')['Revenue'].sum().sort_values(ascending=False)
        rev_prov = flt.groupby('Province')['Revenue'].sum().sort_values(ascending=False)
        ct = flt.groupby('Customer Type')['Revenue'].sum().sort_values(ascending=False)
        rev_lab_monthly = flt.groupby(['Month_Name','Laboratory'])['Revenue'].sum().unstack(fill_value=0)

        c3,c4=st.columns(2)
        with c3:
            _tbl("Revenue by Lab", "FCL · NFCL · WCL",
                [(lab, f"${v:,.0f}") for lab, v in rev_lab.items()],
                accent='#7c3aed')
        with c4:
            _tbl("Revenue by Province", "Top provinces by total revenue",
                [(prov, f"${v:,.0f}") for prov, v in rev_prov.items()],
                accent='#059669')

        c5,c6=st.columns(2)
        with c5:
            total_r = ct.sum()
            _tbl("By Customer Type", "Private vs Government",
                [(ctype.replace(' Company','').replace(' Department',''),
                  f"${v:,.0f}",
                  f"{v/total_r*100:.1f}% of total" if total_r else '')
                 for ctype, v in ct.items()],
                accent='#7c3aed')
        with c6:
            months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            labs = flt['Laboratory'].unique().tolist()
            rev_m_lab = flt.groupby([flt['Service Date'].dt.month, 'Laboratory'])['Revenue'].sum().unstack(fill_value=0)
            rows = []
            for m_num in sorted(rev_m_lab.index):
                row = {'Month': MN[m_num]}
                for lab in sorted(labs):
                    row[lab] = f"${int(rev_m_lab.loc[m_num, lab]):,}" if lab in rev_m_lab.columns else '$0'
                row['Total'] = f"${int(rev_m_lab.loc[m_num].sum()):,}"
                rows.append(row)
            _tbl("Revenue by Lab — Monthly", "Per lab per month",
                rows, accent='#f59e0b',
                cols=['Month'] + sorted(labs) + ['Total'])


# ── 👥 CUSTOMER ──────────────────────────────────────────────────────────────
elif section == "Customer":
    _seq[0] = 0
    st.markdown('<div class="ph"><div class="ph-bc">Pages / Customer</div><h1>👥 Customer</h1><div class="ph-sub">Organisation activity, engagement and complaints.</div></div>', unsafe_allow_html=True)
    start, end = date_range_picker("cust"); flt, _, n = apply_dr(start, end)
    if n == 0: st.info("No records found for the selected date range.")
    else:
        org_flt=org_info[org_info['Organization'].isin(flt['Organization'].unique())].copy()
        cust_by_m = df.groupby(df['Service Date'].dt.month)['Organization'].nunique()
        comp_by_m = df[df['Complaint'].notna()].groupby(df['Service Date'].dt.month).size()
        priv_c_m  = df[df['Customer Type']=='Private Company'].groupby(df['Service Date'].dt.month)['Organization'].nunique()
        tot_by_m  = df.groupby(df['Service Date'].dt.month).size()
        comp_r_m  = comp_by_m / tot_by_m * 100

        to_m = end.month
        fr_m = start.month
        pr_m = to_m - 1

        # totals across selected range
        total_cust  = flt['Organization'].nunique()
        total_comp  = int(flt['Complaint'].notna().sum())
        total_priv_o= flt[flt['Customer Type']=='Private Company']['Organization'].nunique()
        total_comp_r= flt['Complaint'].notna().mean()*100 if len(flt) else 0

        k1,k2,k3,k4 = st.columns(4)
        _skpi([k1,k2,k3,k4], [
            ('Customers',    f'Total {MN[fr_m]}–{MN[to_m]}', '#ff6b6b', '#000', cust_by_m, total_cust,   'num', cust_by_m.get(pr_m,0), cust_by_m.get(to_m,0)),
            ('Complaints',   f'Total {MN[fr_m]}–{MN[to_m]}', '#ffd93d', '#000', comp_by_m, total_comp,   'num', comp_by_m.get(pr_m,0), comp_by_m.get(to_m,0)),
            ('Private Orgs', f'Total {MN[fr_m]}–{MN[to_m]}', '#6bcb77', '#000', priv_c_m,  total_priv_o, 'num', priv_c_m.get(pr_m,0),  priv_c_m.get(to_m,0)),
            ('Complaint %',  f'Avg {MN[fr_m]}–{MN[to_m]}',   '#4d96ff', '#000', comp_r_m,  total_comp_r, 'pct', comp_r_m.get(pr_m,0),  comp_r_m.get(to_m,0)),
        ], start, end)

        # ── Customer tables ──
        act_counts  = org_flt['Activity_Status'].value_counts()
        prov_counts = flt['Province'].value_counts()
        ot_by_ctype = flt.groupby(['Customer Type','On time/Late']).size().unstack(fill_value=0)
        comp_counts = flt['Complaint'].fillna('No Complaint').value_counts()

        c1,c2,c3=st.columns(3)
        with c1:
            _tbl("Customers by Activity", "Organisation engagement status",
                [(status, f"{int(cnt):,} orgs") for status, cnt in act_counts.items()],
                accent='#059669')
        with c2:
            _tbl("Samples by Province", "Geographic spread",
                [(prov, f"{int(cnt):,}") for prov, cnt in prov_counts.items()],
                accent='#7c3aed')
        with c3:
            rows3 = []
            for ctype, row in ot_by_ctype.iterrows():
                short = ctype.replace(' Company','').replace(' Department','')
                on = int(row.get('On-Time', 0)); late = int(row.get('Late', 0))
                total = on + late
                rows3.append((short, f"{on:,} on-time", f"{late:,} late · {on/total*100:.0f}% rate" if total else ''))
            _tbl("On-Time vs Late by Customer", "Delivery by customer type", rows3, accent='#059669')

        c4,c5=st.columns(2)
        with c4:
            _tbl("Complaint Breakdown", "Type and frequency",
                [(comp, f"{int(cnt):,}") for comp, cnt in comp_counts.items()],
                accent='#ef4444')
        with c5:
            top_orgs = flt['Organization'].value_counts().head(10)
            _tbl("Top 10 Organisations", "By sample volume",
                [(org, f"{int(cnt):,} samples") for org, cnt in top_orgs.items()],
                accent='#3b82f6')


# ── 🔬 LABORATORY ─────────────────────────────────────────────────────────────
elif section == "Laboratory":
    _seq[0] = 0
    st.markdown('<div class="ph"><div class="ph-bc">Pages / Laboratory</div><h1>🔬 Laboratory</h1><div class="ph-sub">Testing volumes, turnaround time and delay analysis.</div></div>', unsafe_allow_html=True)
    start, end = date_range_picker("lab"); flt, _, n = apply_dr(start, end)
    if n == 0: st.info("No records found for the selected date range.")
    else:
        cnt_by_m   = df.groupby(df['Service Date'].dt.month).size()
        ot_cnt_m   = df[df['On time/Late']=='On-Time'].groupby(df['Service Date'].dt.month).size()
        late_cnt_m = df[df['On time/Late']=='Late'].groupby(df['Service Date'].dt.month).size()
        delay_m    = df.groupby(df['Service Date'].dt.month)['delay_days'].mean()
        dur_m      = df.groupby(df['Service Date'].dt.month)['test_duration'].mean()

        to_m = end.month
        fr_m = start.month
        pr_m = to_m - 1

        # totals across selected range
        total_ot   = int((flt['On time/Late']=='On-Time').sum())
        total_late = int((flt['On time/Late']=='Late').sum())
        total_delay= flt['delay_days'].mean()
        total_dur  = flt['test_duration'].mean()

        k1,k2,k3,k4 = st.columns(4)
        _skpi([k1,k2,k3,k4], [
            ('On-Time',      f'Total {MN[fr_m]}–{MN[to_m]}',  '#6bcb77', '#000', ot_cnt_m,   total_ot,    'num',  ot_cnt_m.get(pr_m,0),   ot_cnt_m.get(to_m,0)),
            ('Late',         f'Total {MN[fr_m]}–{MN[to_m]}',  '#ff6b6b', '#000', late_cnt_m, total_late,  'num',  late_cnt_m.get(pr_m,0), late_cnt_m.get(to_m,0)),
            ('Avg Delay',    f'Avg {MN[fr_m]}–{MN[to_m]}',    '#ffd93d', '#000', delay_m,    total_delay, 'days', delay_m.get(pr_m,0),    delay_m.get(to_m,0)),
            ('Test Duration',f'Avg {MN[fr_m]}–{MN[to_m]}',    '#c77dff', '#000', dur_m,      total_dur,   'days', dur_m.get(pr_m,0),      dur_m.get(to_m,0)),
        ], start, end)

        # ── Laboratory tables ──
        lab_counts  = flt.groupby('Laboratory').size().sort_values(ascending=False)
        ot_by_lab   = flt.groupby(['Laboratory','On time/Late']).size().unstack(fill_value=0)
        delay_by_lab= flt.groupby('Laboratory')['delay_days'].agg(['mean','sum']).round(1)
        dur_by_lab  = flt.groupby('Laboratory')['test_duration'].mean().round(1)
        delay_dist  = flt['delay_days'].describe().round(1)

        c1,c2=st.columns(2)
        with c1:
            rows_lab = []
            for lab in lab_counts.index:
                on   = int(ot_by_lab.loc[lab,'On-Time']) if 'On-Time' in ot_by_lab.columns else 0
                late = int(ot_by_lab.loc[lab,'Late'])    if 'Late'    in ot_by_lab.columns else 0
                total = on + late
                rows_lab.append((lab,
                    f"{total:,} samples",
                    f"{on:,} on-time · {late:,} late · {on/total*100:.0f}% rate" if total else ''))
            _tbl("Samples by Lab", "Volume and delivery status per lab", rows_lab, accent='#7c3aed')
        with c2:
            rows_delay = []
            for lab in delay_by_lab.index:
                avg_d = delay_by_lab.loc[lab,'mean']
                sum_d = delay_by_lab.loc[lab,'sum']
                avg_dur = dur_by_lab.get(lab, 0)
                rows_delay.append((lab,
                    f"{avg_d:.1f}d avg delay",
                    f"{sum_d:.0f}d total · {avg_dur:.1f}d test duration"))
            _tbl("Delay & Duration by Lab", "Turnaround performance per lab", rows_delay, accent='#f59e0b')

        c3,c4=st.columns(2)
        with c3:
            # Monthly on-time counts
            ot_m = flt.groupby([flt['Service Date'].dt.month,'On time/Late']).size().unstack(fill_value=0)
            rows_m = []
            for m_num in sorted(ot_m.index):
                on   = int(ot_m.loc[m_num,'On-Time']) if 'On-Time' in ot_m.columns else 0
                late = int(ot_m.loc[m_num,'Late'])    if 'Late'    in ot_m.columns else 0
                total = on + late
                rows_m.append({
                    'Month': MN[m_num],
                    'On-Time': f"{on:,}",
                    'Late': f"{late:,}",
                    'Rate': f"{on/total*100:.0f}%" if total else '—'
                })
            _tbl("Monthly On-Time Summary", "Month-by-month delivery", rows_m,
                accent='#059669', cols=['Month','On-Time','Late','Rate'])
        with c4:
            stats = [
                ('Min delay', f"{delay_dist['min']:.1f}d"),
                ('25th pct',  f"{delay_dist['25%']:.1f}d"),
                ('Median',    f"{delay_dist['50%']:.1f}d"),
                ('Mean',      f"{delay_dist['mean']:.1f}d"),
                ('75th pct',  f"{delay_dist['75%']:.1f}d"),
                ('Max delay', f"{delay_dist['max']:.1f}d"),
            ]
            _tbl("Delay Distribution Stats", "Days: Received → Certificate", stats, accent='#ef4444')


# ── 🧬 PARAMETER ─────────────────────────────────────────────────────────────
elif section == "Parameter":
    _seq[0] = 0
    st.markdown('<div class="ph"><div class="ph-bc">Pages / Parameter</div><h1>🧬 Parameter</h1><div class="ph-sub">Parameter counts, costs, revenue and lab distribution.</div></div>', unsafe_allow_html=True)
    start, end = date_range_picker("param"); flt, flt_params, n = apply_dr(start, end)
    if n == 0: st.info("No records found for the selected date range.")
    else:
        price_map=dict(zip(params_df['Parameter Name'],params_df['Cost per Parameter']))

        param_cnt_m  = param_rows.groupby(param_rows['Service Date'].dt.month).size()
        def _cost_by_m(m):
            pr = param_rows[param_rows['Service Date'].dt.month == m]
            return sum(price_map.get(p,0) for p in pr['Parameter'])
        cost_m = pd.Series({m: _cost_by_m(m) for m in range(1,13)})
        avg_param_m = df.groupby(df['Service Date'].dt.month)['Parameter Count'].mean()
        uniq_param_m = param_rows.groupby(param_rows['Service Date'].dt.month)['Parameter'].nunique()

        to_m = end.month
        fr_m = start.month
        pr_m = to_m - 1

        # totals across selected range
        total_params  = len(flt_params)
        total_cost    = sum(price_map.get(p,0) for p in flt_params['Parameter'])
        total_avg_p   = flt['Parameter Count'].mean() if len(flt) else 0
        total_uniq_p  = flt_params['Parameter'].nunique()

        k1,k2,k3,k4 = st.columns(4)
        _skpi([k1,k2,k3,k4], [
            ('Params Tested', f'Total {MN[fr_m]}–{MN[to_m]}', '#ff6b6b', '#000', param_cnt_m,  total_params,  'num',    param_cnt_m.get(pr_m,0),  param_cnt_m.get(to_m,0)),
            ('Est. Cost',     f'Total {MN[fr_m]}–{MN[to_m]}', '#ffd93d', '#000', cost_m,        total_cost,    'dollar', cost_m.get(pr_m,0),        cost_m.get(to_m,0)),
            ('Avg Params',    f'Avg {MN[fr_m]}–{MN[to_m]}',   '#6bcb77', '#000', avg_param_m,  total_avg_p,   'days',   avg_param_m.get(pr_m,0),  avg_param_m.get(to_m,0)),
            ('Unique Params', f'Total {MN[fr_m]}–{MN[to_m]}', '#4d96ff', '#000', uniq_param_m, total_uniq_p,  'num',    uniq_param_m.get(pr_m,0), uniq_param_m.get(to_m,0)),
        ], start, end)

        p_cnt=flt_params['Parameter'].value_counts().reset_index(); p_cnt.columns=['Parameter','Count']
        p_cnt['Cost']=p_cnt['Parameter'].map(price_map).fillna(0)
        p_cnt['Revenue']=p_cnt['Count']*p_cnt['Cost']
        p_cnt=p_cnt.sort_values('Count',ascending=False)

        c1,c2=st.columns(2)
        with c1:
            _tbl("Parameter Test Count", "Times each parameter was tested",
                [(row['Parameter'], f"{int(row['Count']):,}", f"${row['Revenue']:,.0f} est. revenue")
                 for _, row in p_cnt.iterrows()],
                accent='#7c3aed')
        with c2:
            _tbl("Parameter Revenue", "Count × unit cost per parameter",
                [(row['Parameter'], f"${row['Revenue']:,.0f}", f"{int(row['Count']):,} tests · ${row['Cost']:,.0f}/test")
                 for _, row in p_cnt.sort_values('Revenue', ascending=False).iterrows()],
                accent='#059669')

        # Parameters by Lab — multi-col table
        lab_param = flt_params.groupby(['Laboratory','Parameter']).size().unstack(fill_value=0)
        all_params = p_cnt['Parameter'].tolist()
        lab_rows = []
        for param in all_params:
            row = {'Parameter': param}
            for lab in lab_param.index:
                row[lab] = f"{int(lab_param.loc[lab, param]):,}" if param in lab_param.columns else '0'
            row['Total'] = f"{int(sum(lab_param[param]) if param in lab_param.columns else 0):,}"
            lab_rows.append(row)
        _tbl("Parameters by Laboratory", "Test count per parameter per lab",
            lab_rows, accent='#f59e0b',
            cols=['Parameter'] + list(lab_param.index) + ['Total'])

        c3,c4=st.columns(2)
        with c3:
            pc_dist = flt['Parameter Count'].value_counts().sort_index()
            _tbl("Parameter Count Distribution", "How many params per sample",
                [(f"{int(k)} params", f"{int(v):,} samples", f"{v/len(flt)*100:.1f}% of records")
                 for k, v in pc_dist.items()],
                accent='#7c3aed')
        with c4:
            top5 = p_cnt.head(5)['Parameter'].tolist()
            top5_m = flt_params[flt_params['Parameter'].isin(top5)].groupby(
                [flt_params['Service Date'].dt.month,'Parameter']).size().unstack(fill_value=0)
            t5_rows = []
            for m_num in sorted(top5_m.index):
                row = {'Month': MN[m_num]}
                for p in top5:
                    row[p[:6]] = str(int(top5_m.loc[m_num, p])) if p in top5_m.columns else '0'
                t5_rows.append(row)
            _tbl("Top 5 Parameters — Monthly", "Count per month",
                t5_rows, accent='#3b82f6',
                cols=['Month'] + [p[:6] for p in top5])


st.markdown('<div style="text-align:center;color:#9ca3af;font-size:.64rem;padding:14px 0 6px;border-top:1.5px solid #e2e6f0;margin-top:12px;letter-spacing:.07em;font-family:DM Sans,sans-serif;">LABCARE ANALYTICS · LAB SERVICE 2025 · 2,000 RECORDS</div>', unsafe_allow_html=True)