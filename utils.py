import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import date, timedelta
import calendar
import os

# Absolute path to the Excel file — always relative to this utils.py file
_BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
_EXCEL_PATH = os.path.join(_BASE_DIR, "Lab_Service_2025_2000rows_MergedOrg.xlsx")

# ══════════════════════════════════════════════════════ CONSTANTS ══════
BLK = "#111827"
MN  = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
       7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
MONTH_ORD = {'Jan':0,'Feb':1,'Mar':2,'Apr':3,'May':4,'Jun':5,
             'Jul':6,'Aug':7,'Sep':8,'Oct':9,'Nov':10,'Dec':11}

# ══════════════════════════════════════════════════════════ CSS ══════
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700;9..40,800;9..40,900&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#f0f2f8}

[data-testid="stSidebar"]{background:linear-gradient(175deg,#0a0820 0%,#130e3d 50%,#1c1548 100%)!important;border-right:none!important;box-shadow:6px 0 32px rgba(0,0,0,.45)!important}
[data-testid="stSidebar"] *{color:#b8b0e8!important;font-family:'DM Sans',sans-serif!important}

[data-testid="stSidebar"] .stButton button{background:transparent!important;border:none!important;border-radius:12px!important;padding:11px 14px!important;font-size:.88rem!important;font-weight:500!important;color:#b8b0e8!important;width:100%!important;text-align:left!important;font-family:'DM Sans',sans-serif!important;box-shadow:none!important;transition:all .22s cubic-bezier(.34,1.56,.64,1)!important;cursor:pointer!important;pointer-events:auto!important}
[data-testid="stSidebar"] .stButton button:hover{background:rgba(255,255,255,.08)!important;color:#fff!important;transform:translateX(5px)!important}
[data-testid="stSidebar"] .stButton button:focus{box-shadow:none!important;outline:none!important;border:none!important}

section[data-testid="stSidebar"]{min-width:280px!important;max-width:280px!important;transform:none!important}
button[data-testid="baseButton-header"]{display:none!important}
[data-testid="stSidebarCollapseButton"]{display:none!important}
[data-testid="collapsedControl"]{display:none!important;visibility:hidden!important;width:0!important;height:0!important;margin:0!important;padding:0!important;border:none!important;pointer-events:none!important;overflow:hidden!important}
[data-testid="collapsedControl"] *{display:none!important;visibility:hidden!important;pointer-events:none!important}
button[kind="header"]{display:none!important;visibility:hidden!important;pointer-events:none!important}
[data-testid="stSidebar"]{display:block!important;visibility:visible!important}
#MainMenu{visibility:hidden!important}

.nav-active-wrap{position:relative}
.nav-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(124,58,237,.32);border:1px solid rgba(167,139,250,.35);border-radius:20px;padding:2px 9px 2px 7px;font-size:.55rem;font-weight:800;color:#c4b5f4!important;letter-spacing:.09em;text-transform:uppercase;margin:0 8px 5px 8px}
.nav-dot{width:6px;height:6px;border-radius:50%;background:#a78bfa;box-shadow:0 0 7px 2px rgba(167,139,250,.75);animation:pulse 1.9s ease-in-out infinite;flex-shrink:0}
.slogo{padding:24px 18px 18px;border-bottom:1px solid rgba(124,58,237,.18);margin-bottom:8px}
.slogo-title{font-size:1.1rem;font-weight:900;color:#fff!important;display:flex;align-items:center;gap:9px}
.slogo-pill{background:rgba(124,58,237,.3);color:#c4b5f4!important;font-size:.55rem!important;font-weight:800!important;padding:2px 8px;border-radius:20px;letter-spacing:.1em}
.slogo-sub{font-size:.6rem;color:rgba(184,176,232,.32)!important;margin-top:5px}
.slogo-user{font-size:.65rem;color:rgba(167,139,250,.8)!important;margin-top:4px;font-weight:600}

.stTextInput > div > div,.stTextInput > div > div > input,[data-testid="stTextInputRootElement"],[data-testid="stTextInputRootElement"] input{background:#fff!important;color:#111827!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important;font-size:.82rem!important;font-weight:500!important;}
[data-testid="stTextInputRootElement"] input:focus{border-color:#7c3aed!important;box-shadow:0 0 0 3px rgba(124,58,237,.12)!important;outline:none!important;background:#fff!important;color:#111827!important;}
[data-testid="stTextInputRootElement"] input::placeholder{color:#9ca3af!important;font-weight:400!important;}

.stSelectbox > div > div,[data-testid="stSelectbox"] > div,[data-testid="stSelectbox"] > div > div{background:#fff!important;color:#111827!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important;font-size:.82rem!important;font-weight:500!important;}
[data-testid="stSelectbox"] span,[data-testid="stSelectbox"] p,[data-testid="stSelectbox"] div{color:#111827!important;background:#fff!important;}
[data-testid="stSelectbox"] ul,[data-baseweb="popover"],[data-baseweb="popover"] *,[data-baseweb="menu"],[data-baseweb="menu"] *,[data-baseweb="select"] *{background:#fff!important;color:#111827!important;font-family:'DM Sans',sans-serif!important;}
[data-baseweb="option"]:hover,[role="option"]:hover{background:#f5f3ff!important;color:#7c3aed!important;}
[aria-selected="true"][role="option"]{background:#ede9fe!important;color:#5b21b6!important;font-weight:700!important;}
[data-testid="stSelectbox"] svg{fill:#6b7280!important;}

.stCheckbox,.stCheckbox label,.stCheckbox span,.stCheckbox p{color:#111827!important;font-family:'DM Sans',sans-serif!important;font-size:.82rem!important;font-weight:500!important;background:transparent!important;}
[data-baseweb="checkbox"] > div{background:#fff!important;border:2px solid #d1d5db!important;border-radius:5px!important;}
[data-baseweb="checkbox"][aria-checked="true"] > div{background:#7c3aed!important;border-color:#7c3aed!important;}

[data-testid="stDateInputField"],[data-testid="stDateInputField"] input,[data-testid="stDateInput"] input,[data-testid="stDateInput"] > div > div{background:#fff!important;color:#111827!important;border:2px solid #e5e7eb!important;border-radius:12px!important;font-family:'DM Sans',sans-serif!important;font-weight:600!important;font-size:.85rem!important;padding:9px 14px!important;}
[data-testid="stDateInputField"] input:focus{border-color:#7c3aed!important;box-shadow:0 0 0 4px rgba(124,58,237,.13)!important;outline:none!important;}

[data-baseweb="calendar"]{background:#fff!important;border-radius:18px!important;box-shadow:0 8px 36px rgba(0,0,0,.13)!important;border:1px solid #e5e7eb!important;padding:10px!important;overflow:hidden!important;}
[data-baseweb="calendar"] div,[data-baseweb="calendar"] span,[data-baseweb="calendar"] p,[data-baseweb="calendar"] abbr,[data-baseweb="calendar"] td,[data-baseweb="calendar"] th,[data-baseweb="calendar"] tr,[data-baseweb="calendar"] table,[data-baseweb="calendar"] thead,[data-baseweb="calendar"] tbody{background:#fff!important;color:#111827!important;font-family:'DM Sans',sans-serif!important;border-color:transparent!important;}
[data-baseweb="calendar"] [role="columnheader"],[data-baseweb="calendar"] [role="columnheader"] *{color:#9ca3af!important;font-size:.66rem!important;font-weight:800!important;text-transform:uppercase!important;letter-spacing:.09em!important;background:#fff!important;}
[data-baseweb="calendar"] [role="gridcell"] button{background:#fff!important;color:#374151!important;border:none!important;outline:none!important;box-shadow:none!important;border-radius:50%!important;font-weight:500!important;font-family:'DM Sans',sans-serif!important;transition:background .15s,color .15s,box-shadow .15s!important;cursor:pointer!important;}
[data-baseweb="calendar"] [role="gridcell"] button:hover{background:#fee2e2!important;color:#ef4444!important;box-shadow:0 0 0 3px rgba(239,68,68,.15)!important;}
[data-baseweb="calendar"] [aria-current="date"] button{background:#ef4444!important;color:#fff!important;font-weight:800!important;border-radius:50%!important;box-shadow:0 2px 10px rgba(239,68,68,.45)!important;}
[data-baseweb="calendar"] [aria-selected="true"] button{background:#7c3aed!important;color:#fff!important;border-radius:50%!important;font-weight:800!important;box-shadow:0 2px 12px rgba(124,58,237,.4)!important;}

.stButton button{background:#fff!important;color:#111827!important;border:1.5px solid #d1d5db!important;border-radius:10px!important;padding:10px 14px!important;font-size:.95rem!important;font-weight:700!important;font-family:'DM Sans',sans-serif!important;transition:all .2s ease!important;box-shadow:0 2px 6px rgba(0,0,0,.08)!important}
.stButton button:hover{background:#f9fafb!important;color:#111827!important;box-shadow:0 4px 10px rgba(0,0,0,.12)!important;border-color:#9ca3af!important}
.stButton button:focus{box-shadow:0 0 0 3px rgba(124,58,237,.1),0 2px 6px rgba(0,0,0,.08)!important;border-color:#7c3aed!important}

[data-testid="stSidebar"] .stButton button{background:transparent!important;border:none!important;border-radius:12px!important;padding:11px 14px!important;font-size:.88rem!important;font-weight:500!important;color:#b8b0e8!important;width:100%!important;text-align:left!important;box-shadow:none!important;}
[data-testid="stSidebar"] .stButton button:hover{background:rgba(255,255,255,.08)!important;color:#fff!important;transform:translateX(5px)!important}
[data-testid="stSidebar"] .nav-active-wrap .stButton button{background:rgba(124,58,237,.22)!important;color:#fff!important;font-weight:700!important;border-left:3px solid #a78bfa!important;border-radius:0 12px 12px 0!important;padding-left:13px!important}

.dr-mode-buttons{display:flex;gap:12px!important;width:100%!important;margin:12px 0!important;padding:0!important}
.dr-mode-buttons > div{flex:1!important;min-width:0!important}

[data-testid="stNumberInput"] input{background:#fff!important;color:#111827!important;border:1.5px solid #e5e7eb!important;border-radius:10px!important;font-family:'DM Sans',sans-serif!important;font-size:1rem!important;font-weight:600!important;padding:12px 14px!important;}
[data-testid="stNumberInput"] button{background:#ffffff!important;color:#111827!important;border:1.5px solid #e5e7eb!important;border-radius:6px!important;cursor:pointer!important;font-weight:700!important;}
[data-testid="stNumberInput"] svg{fill:#111827!important;stroke:#111827!important;width:20px!important;height:20px!important;}

.dr-card{background:#fff;border-radius:24px;padding:22px 26px 20px;margin-bottom:32px;box-shadow:0 6px 32px rgba(124,58,237,.10),0 1px 4px rgba(0,0,0,.04);animation:fadeUp .38s cubic-bezier(.22,1,.36,1) both;position:relative;overflow:hidden}
.dr-card::before{content:'';position:absolute;top:0;left:0;right:0;height:5px;background:linear-gradient(90deg,#7c3aed 0%,#3b82f6 25%,#06b6d4 50%,#059669 75%,#f59e0b 100%);border-radius:24px 24px 0 0}
.dr-blob1{position:absolute;top:-30px;right:-30px;width:120px;height:120px;border-radius:50%;background:radial-gradient(circle,rgba(124,58,237,.07),transparent 70%);pointer-events:none}
.dr-blob2{position:absolute;bottom:-20px;left:-20px;width:90px;height:90px;border-radius:50%;background:radial-gradient(circle,rgba(5,150,105,.06),transparent 70%);pointer-events:none}
.dr-header{display:flex;align-items:center;margin-bottom:16px}
.dr-title{font-size:.85rem;font-weight:900;color:#111827;text-transform:uppercase;letter-spacing:.14em;display:flex;align-items:center;gap:8px}
.dr-title-pill{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:#fff!important;font-size:.65rem;font-weight:800;padding:4px 12px;border-radius:20px;letter-spacing:.08em;box-shadow:0 2px 8px rgba(124,58,237,.35)}
.dr-pill-btn .stButton button{background:linear-gradient(135deg,#f5f3ff,#ede9fe)!important;border:1.5px solid #ddd6fe!important;border-radius:20px!important;padding:8px 18px!important;font-size:.8rem!important;font-weight:700!important;color:#5b21b6!important;min-width:0!important;width:auto!important;transition:all .2s cubic-bezier(.34,1.56,.64,1)!important;box-shadow:none!important;}
.dr-pill-btn .stButton button:hover{background:linear-gradient(135deg,#7c3aed,#6d28d9)!important;color:#fff!important;border-color:#7c3aed!important;transform:translateY(-2px)!important;box-shadow:0 6px 16px rgba(124,58,237,.3)!important}
.dr-field-label{font-size:.75rem!important;font-weight:800!important;text-transform:uppercase;letter-spacing:.13em;margin-bottom:8px!important;display:flex;align-items:center;gap:6px;color:#111827!important}
.lbl-from{color:#7c3aed}.lbl-to{color:#059669}
.lbl-dot{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0}
.lbl-dot-from{background:linear-gradient(135deg,#7c3aed,#a78bfa);box-shadow:0 0 6px rgba(124,58,237,.5)}
.lbl-dot-to{background:linear-gradient(135deg,#059669,#34d399);box-shadow:0 0 6px rgba(5,150,105,.5)}
.dr-arrow-wrap{display:flex;align-items:center;justify-content:center;padding-top:26px}
.dr-arrow-icon{font-size:1.4rem;color:#c4b5f4;animation:arrowBounce 2s ease-in-out infinite}
@keyframes arrowBounce{0%,100%{transform:translateX(0)}50%{transform:translateX(5px)}}
.dr-summary{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1.5px solid #a7f3d0;border-radius:14px;padding:12px 18px;margin-top:16px}
.dr-sum-from{font-size:.9rem;font-weight:800;color:#065f46}
.dr-sum-arrow{color:#34d399;font-size:1.2rem}
.dr-sum-to{font-size:.9rem;font-weight:800;color:#065f46}
.dr-sum-days{font-size:.8rem;font-weight:600;color:#6b7280}
.dr-sum-badge{margin-left:auto;background:linear-gradient(135deg,#059669,#10b981);color:#fff!important;font-size:.8rem;font-weight:800;padding:6px 14px;border-radius:20px;letter-spacing:.07em;box-shadow:0 3px 10px rgba(5,150,105,.3);white-space:nowrap}

.cc{background:#fff;border-radius:20px;padding:20px 18px 12px;box-shadow:0 2px 12px rgba(0,0,0,.06);margin-bottom:14px;opacity:0;animation:fadeUp .55s cubic-bezier(.22,1,.36,1) both;transition:transform .28s,box-shadow .28s;position:relative;overflow:hidden}
.cc-bar{position:absolute;top:0;left:0;right:0;height:3px;border-radius:20px 20px 0 0;background:linear-gradient(90deg,#7c3aed,#3b82f6,#059669);opacity:0;transition:opacity .3s}
.cc:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(61,32,128,.12)}
.cc:hover .cc-bar{opacity:1}
.cc-title{font-size:.92rem;font-weight:800;color:#111827;margin-bottom:2px}
.cc-sub{font-size:.66rem;color:#9ca3af;font-weight:500;margin-bottom:8px}

[data-testid="stDataFrame"]{border-radius:14px!important;overflow:hidden!important}
[data-testid="stDataFrame"] th{background:#f8f9fc!important;color:#111827!important;font-weight:700!important}
[data-testid="stDataFrame"] td{background:#fff!important;color:#111827!important}

[data-testid="stMetricLabel"]{color:#111827!important;font-weight:700!important}
[data-testid="stMetricValue"]{color:#111827!important;font-weight:900!important}
[data-testid="metric-container"]{background:#f8f9fc!important;border-radius:14px!important;padding:16px!important;border:1.5px solid #ede9fe!important}

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
"""

# ═══════════════════════════════════════════════════════════ DATA ══════
@st.cache_data
def load_data():
    df = pd.read_excel(_EXCEL_PATH, sheet_name="Service Data")
    params = pd.read_excel(_EXCEL_PATH, sheet_name="Parameter Price List")
    for col in ['Service Date','Sample Received Date','Testing Start Date','Certificate Date','Payment Date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    df['Testing Completion Date'] = pd.to_datetime(df['Testing Completion Date'], errors='coerce')
    df['Month']      = df['Service Date'].dt.month
    df['Year']       = df['Service Date'].dt.year
    df['Month_Name'] = df['Service Date'].dt.strftime('%b')
    df['delay_days']       = (df['Certificate Date'] - df['Sample Received Date']).dt.days
    df['receive_to_start'] = (df['Testing Start Date'] - df['Sample Received Date']).dt.days
    df['test_duration']    = (df['Testing Completion Date'] - df['Testing Start Date']).dt.days
    df['cert_late_days']   = df['delay_days'].clip(lower=0)

    if 'Service Type' not in df.columns:
        import numpy as np
        np.random.seed(42)
        df['Service Type'] = np.random.choice(
            ['Basic', 'Standard', 'Premium'], size=len(df), p=[0.35, 0.45, 0.20]
        )

    today = pd.Timestamp('2025-12-31')
    oi = df.groupby('Organization').agg(
        last_visit=('Service Date','max'),
        total_visits=('Service Date','count')
    ).reset_index()

    def classify(r):
        m = (today - r['last_visit']).days / 30.44
        if m <= 4 and r['total_visits'] >= 2: return 'Active'
        elif m <= 7:  return '>4 months'
        elif m <= 13: return '>7 months'
        elif m <= 24: return '>13 months'
        else:         return '>2 years'
    oi['Activity_Status'] = oi.apply(classify, axis=1)

    df2 = df.merge(
        oi[['Organization','Activity_Status','total_visits','last_visit']],
        on='Organization', how='left'
    )

    rows = []
    for _, row in df2.iterrows():
        if pd.notna(row['Parameters Tested']):
            for p in str(row['Parameters Tested']).split(','):
                p = p.strip()
                if p:
                    rows.append({
                        'Laboratory':     row['Laboratory'],
                        'Month':          row['Month'],
                        'Month_Name':     row['Month_Name'],
                        'Parameter':      p,
                        'Customer Type':  row['Customer Type'],
                        'Province':       row['Province'],
                        'Year':           row['Year'],
                        'Service Date':   row['Service Date']
                    })
    return df2, params, pd.DataFrame(rows), oi


# ══════════════════════════════════════════════════ AUTH HELPERS ══════

# Users — role controls which page they can access
USERS = {
    "finance":   {"password": "finance123",   "role": "Finance",   "display": "Finance Team",       "page": "Financial"},
    "customer":  {"password": "customer123",  "role": "Customer",  "display": "Customer Service",   "page": "Customer"},
    "technique": {"password": "technique123", "role": "Technique", "display": "Technique Team",     "page": "Analysis"},
}

# Maps role → the single page they are allowed to visit
ROLE_PAGE = {
    "Finance":   "Financial",
    "Customer":  "Customer",
    "Technique": "Analysis",
}

# Full nav config (icon, sidebar label, page key)
ALL_NAV = [
    ("💰", "Financial",        "Financial"),
    ("👥", "Customer",         "Customer"),
    ("🔬", "NISTI Performance","Analysis"),
]


def check_login(current_page: str = ""):
    """
    Verify the user is logged in AND is allowed to view current_page.
    Redirects to login or their home page if not authorised.
    """
    if not st.session_state.get("logged_in"):
        st.switch_page("main.py")
        st.stop()

    if current_page:
        role      = st.session_state["user"]["role"]
        allowed   = ROLE_PAGE.get(role, "")
        if allowed and current_page != allowed:
            st.switch_page(f"pages/{allowed}.py")
            st.stop()


def render_sidebar(active_page: str):
    """Render sidebar — only shows the nav item the user's role can access."""
    # ── hide Streamlit's default page list ──
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"]{display:none!important}
    </style>""", unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    role = user.get("role", "")

    # Which nav items this role can see
    allowed_page = ROLE_PAGE.get(role, "")
    visible_nav  = [(icon, label, key) for icon, label, key in ALL_NAV
                    if key == allowed_page]

    with st.sidebar:
        st.markdown(
            f'<div class="slogo">'
            f'<div class="slogo-title">🧪 LabCare <span class="slogo-pill">2025</span></div>'
            f'<div class="slogo-sub">Analytics Dashboard · 2,000 records</div>'
            f'<div class="slogo-user">👤 {user.get("display","User")} · {role}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        for icon, label, page_key in visible_nav:
            is_active = active_page == page_key
            if is_active:
                st.markdown(
                    '<div class="nav-active-wrap">'
                    '<span class="nav-badge"><span class="nav-dot"></span>Viewing now</span>',
                    unsafe_allow_html=True
                )
            if st.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True):
                st.switch_page(f"pages/{page_key}.py")
            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr style="border-color:rgba(124,58,237,.18);margin:16px 0">', unsafe_allow_html=True)
        if st.button("🚪  Logout", key="nav_logout", use_container_width=True):
            st.session_state.clear()
            st.switch_page("main.py")


# ══════════════════════════════════════════════════════ LAYOUT ══════
def _lo(h=230):
    return dict(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans', color=BLK, size=11),
        height=h, margin=dict(l=10, r=10, t=16, b=10),
        xaxis=dict(gridcolor='rgba(0,0,0,.05)', zeroline=False, showline=False,
                   tickfont=dict(size=10, color=BLK), title_font=dict(size=11, color=BLK)),
        yaxis=dict(gridcolor='rgba(0,0,0,.05)', zeroline=False, showline=False,
                   tickfont=dict(size=10, color=BLK), title_font=dict(size=11, color=BLK)),
        legend=dict(font=dict(size=10, color=BLK), bgcolor='rgba(255,255,255,.92)',
                    bordercolor='rgba(0,0,0,.06)', borderwidth=1,
                    orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        transition=dict(duration=400, easing='cubic-in-out'), bargap=0.22, bargroupgap=0.06
    )


def _tbl(title, subtitle, rows, accent='#7c3aed', cols=None, key=None):
    RANK_COLORS = ['#7c3aed','#9f5ff0','#c4b5f4','#ddd6fe','#ede9fe']
    import hashlib
    raw  = (title + subtitle + (key or '')).encode()
    tkey = 'tbl_' + hashlib.md5(raw).hexdigest()[:10]

    st.markdown(
        f'<div style="background:#fff;border-radius:18px 18px 0 0;'
        f'box-shadow:0 -2px 10px rgba(0,0,0,.05);border-top:4px solid {accent};'
        f'padding:14px 14px 10px;border-bottom:1px solid #f3f4f6;">'
        f'<span style="font-size:.85rem;font-weight:800;color:#111827;display:block;">{title}</span>'
        f'<span style="font-size:.63rem;color:#9ca3af;display:block;margin-top:2px;">{subtitle}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    if cols:
        fc1, fc2, fc3 = st.columns([3, 2, 1])
        with fc1:
            search   = st.text_input('Search', key=f'{tkey}_s', placeholder=f'Filter {cols[0]}…', label_visibility='collapsed')
        with fc2:
            sort_col = st.selectbox('Sort by', cols, key=f'{tkey}_sc', label_visibility='collapsed')
        with fc3:
            asc      = st.checkbox('↑', value=False, key=f'{tkey}_asc')

        filtered = [r for r in rows if search.lower() in str(r.get(cols[0], '')).lower()] if search else list(rows)

        def _skey(r):
            v = str(r.get(sort_col, ''))
            c = v.replace('$','').replace(',','').replace('%','').replace('d','').strip()
            try: return float(c)
            except: return v

        filtered = sorted(filtered, key=_skey, reverse=not asc)
        p = [
            f'<div style="background:#fff;border-radius:0 0 18px 18px;box-shadow:0 4px 16px rgba(0,0,0,.07);overflow:hidden;margin-bottom:16px;">',
            f'<div style="padding:3px 14px 5px;background:#f9f9f9;border-bottom:1px solid #eee;"><span style="font-size:.58rem;color:#9ca3af;">{len(filtered):,} rows{f" of {len(rows):,}" if search else ""}</span></div>',
            '<div style="display:flex;padding:8px 14px;border-bottom:2px solid #f0f0f0;background:#f9fafb;">',
        ]
        for ci, c in enumerate(cols):
            align = 'left' if ci == 0 else 'right'
            flex  = '2' if ci == 0 else '1'
            arrow = (' ↑' if asc else ' ↓') if c == sort_col else ''
            col_c = accent if c == sort_col else '#9ca3af'
            p.append(f'<span style="flex:{flex};text-align:{align};font-size:.59rem;font-weight:800;color:{col_c};text-transform:uppercase;letter-spacing:.07em;">{c}{arrow}</span>')
        p.append('</div>')
        for ri, row in enumerate(filtered):
            bg = '#fafafa' if ri % 2 == 0 else '#fff'
            p.append(f'<div style="display:flex;padding:9px 14px;background:{bg};border-bottom:1px solid #f3f4f6;">')
            for ci, c in enumerate(cols):
                align = 'left' if ci == 0 else 'right'
                flex  = '2' if ci == 0 else '1'
                fw    = '700' if ci == 0 else '600'
                color = '#374151' if ci == 0 else '#111827'
                p.append(f'<span style="flex:{flex};text-align:{align};font-size:.76rem;font-weight:{fw};color:{color};overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{row.get(c, "—")}</span>')
            p.append('</div>')
        p.append('</div>')
        st.markdown(''.join(p), unsafe_allow_html=True)
    else:
        fc1, fc2 = st.columns([3, 2])
        with fc1:
            search   = st.text_input('Search', key=f'{tkey}_s', placeholder='Filter by name…', label_visibility='collapsed')
        with fc2:
            sort_opt = st.selectbox('Sort', ['Default','Value ↑','Value ↓'], key=f'{tkey}_so', label_visibility='collapsed')

        filtered = [r for r in rows if search.lower() in str(r[0]).lower()] if search else list(rows)

        def _vnum(r):
            c = str(r[1]).replace('$','').replace(',','').replace('%','').replace('d','').strip().split()[0]
            try: return float(c)
            except: return 0

        if sort_opt == 'Value ↑':   filtered = sorted(filtered, key=_vnum)
        elif sort_opt == 'Value ↓': filtered = sorted(filtered, key=_vnum, reverse=True)

        p = [
            f'<div style="background:#fff;border-radius:0 0 18px 18px;box-shadow:0 4px 16px rgba(0,0,0,.07);overflow:hidden;margin-bottom:16px;">',
            f'<div style="padding:3px 14px 5px;background:#f9f9f9;border-bottom:1px solid #eee;"><span style="font-size:.58rem;color:#9ca3af;">{len(filtered):,} items{f" of {len(rows):,}" if search else ""}</span></div>',
        ]
        for ri, row in enumerate(filtered):
            label   = row[0]; val = row[1]
            sub     = row[2] if len(row) > 2 else ''
            dot_col = RANK_COLORS[min(ri, len(RANK_COLORS)-1)]
            bg      = '#fafafa' if ri % 2 == 0 else '#fff'
            p.append(
                f'<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:{bg};border-bottom:1px solid #f3f4f6;">'
                f'<div style="display:flex;align-items:center;gap:8px;min-width:0;flex:1;">'
                f'<span style="width:7px;height:7px;border-radius:50%;background:{dot_col};flex-shrink:0;display:inline-block;"></span>'
                f'<span style="min-width:0;">'
                f'<span style="display:block;font-size:.78rem;font-weight:600;color:#374151;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{label}</span>'
            )
            if sub:
                p.append(f'<span style="display:block;font-size:.6rem;color:#9ca3af;margin-top:1px;">{sub}</span>')
            p.append(
                f'</span></div>'
                f'<span style="font-size:.92rem;font-weight:800;color:#111827;white-space:nowrap;margin-left:12px;">{val}</span>'
                f'</div>'
            )
        p.append('</div>')
        st.markdown(''.join(p), unsafe_allow_html=True)


def _make_sparkline_svg(vals, accent, fmt, card_uid, from_m=1, to_m=12, width=300, height=70):
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
        return (c1x, c1y), (c2x, c2y)

    pts = list(zip(xs, ys))
    d   = f'M {pts[0][0]:.1f},{pts[0][1]:.1f}'
    for k in range(1, len(pts)):
        p0 = pts[k-2] if k >= 2 else pts[0]
        p1 = pts[k-1]; p2 = pts[k]
        p3 = pts[k+1] if k+1 < len(pts) else pts[-1]
        _, c1 = ctrl(p0, p1, p2)
        c2, _ = ctrl(p1, p2, p3)
        d += f' C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'

    area_d  = d + f' L {xs[-1]:.1f},{height} L {xs[0]:.1f},{height} Z'
    grad_id = f'sg_{card_uid}'
    tip_h   = 26

    css_rules = '<style>\n'
    for k in range(n):
        gid = f'hp_{card_uid}_{k}'
        css_rules += (
            f'#{gid} .spk-dot{{opacity:0;transition:opacity .12s;}}\n'
            f'#{gid} .spk-tip{{opacity:0;transition:opacity .12s;}}\n'
            f'#{gid}:hover .spk-dot{{opacity:1;}}\n'
            f'#{gid}:hover .spk-tip{{opacity:1;}}\n'
        )
    css_rules += '</style>'

    hover_groups = ''
    for k in range(n):
        gid     = f'hp_{card_uid}_{k}'
        mon     = MONTHS[k]
        lbl     = _fmtv(vals[k], fmt)
        tip_txt = f'{mon}: {lbl}'
        tip_w   = max(len(tip_txt) * 7 + 16, 72)
        tip_x   = xs[k] - tip_w / 2
        if tip_x < 2: tip_x = 2
        if tip_x + tip_w > width - 2: tip_x = width - tip_w - 2
        tip_y = ys[k] - tip_h - 8
        if tip_y < 2: tip_y = ys[k] + 10

        hover_groups += (
            f'<g id="{gid}" style="cursor:crosshair;">'
            f'<rect x="{xs[k]-13:.1f}" y="0" width="26" height="{height}" fill="transparent"/>'
            f'<line class="spk-tip" x1="{xs[k]:.1f}" y1="0" x2="{xs[k]:.1f}" y2="{height}"'
            f' stroke="{accent}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>'
            f'<circle class="spk-dot" cx="{xs[k]:.1f}" cy="{ys[k]:.1f}" r="4"'
            f' fill="{accent}" stroke="white" stroke-width="2"/>'
            f'<g class="spk-tip">'
            f'<rect x="{tip_x:.1f}" y="{tip_y:.1f}" width="{tip_w}" height="{tip_h}"'
            f' rx="6" ry="6" fill="#1e1b4b" opacity="0.92"/>'
            f'<text x="{tip_x + tip_w/2:.1f}" y="{tip_y + 17:.1f}"'
            f' text-anchor="middle" fill="white" font-size="11" font-weight="700"'
            f' font-family="DM Sans,sans-serif">{tip_txt}</text>'
            f'</g></g>'
        )

    svg = (
        f'<svg viewBox="0 0 {width} {height}" preserveAspectRatio="none"'
        f' style="width:100%;height:{height}px;display:block;overflow:visible;">'
        f'{css_rules}'
        f'<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{accent}" stop-opacity="0.20"/>'
        f'<stop offset="100%" stop-color="{accent}" stop-opacity="0.02"/>'
        f'</linearGradient></defs>'
        f'<path d="{area_d}" fill="url(#{grad_id})"/>'
        f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="2"'
        f' stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{xs[from_m-1]:.1f}" cy="{ys[from_m-1]:.1f}" r="3.5"'
        f' fill="{accent}" stroke="white" stroke-width="2"/>'
        f'<circle cx="{xs[to_m-1]:.1f}" cy="{ys[to_m-1]:.1f}" r="3.5"'
        f' fill="{accent}" stroke="white" stroke-width="2"/>'
        f'{hover_groups}'
        f'</svg>'
    )
    return svg


def _skpi(_, cards, start_date, end_date):
    from_m = start_date.month
    to_m   = end_date.month
    ACCENTS = ['#7c3aed','#3b82f6','#059669','#f59e0b']

    def _fmt(v, fmt):
        if fmt == 'dollar': return f'${v:,.0f}'
        if fmt == 'pct':    return f'{v:.1f}%'
        if fmt == 'days':   return f'{v:.1f}d'
        return f'{int(v):,}'

    def _badge(cur, prev, fmt):
        if not prev: return '', '', ''
        d = (cur - prev) / prev * 100
        arrow = '▲' if d >= 0 else '▼'
        bg  = '#dcfce7' if d >= 0 else '#fee2e2'
        col = '#059669' if d >= 0 else '#dc2626'
        suffix = ' pp' if fmt == 'pct' else '%'
        return f'{arrow} {abs(d):.1f}{suffix}', col, bg

    period_lbl = MN[to_m] if from_m == to_m else f'{MN[from_m]} \u00bb {MN[to_m]}'
    prev_m_lbl = MN[to_m - 1] if to_m > 1 else ''

    inner_cards = []
    for i, card in enumerate(cards):
        if len(card) == 9:
            title, subtitle, _bg, _lc, mseries, total_val, fmt, prev_val, cur_m_val = card
        elif len(card) == 8:
            title, subtitle, _bg, _lc, mseries, total_val, fmt, prev_val = card
            cur_m_val = total_val
        else:
            title, subtitle, _bg, _lc, mseries, total_val, fmt = card
            prev_val = 0; cur_m_val = total_val

        accent    = ACCENTS[i % len(ACCENTS)]
        val_str   = _fmt(total_val, fmt)
        vals      = [float(mseries.get(m, 0)) for m in range(1, 13)]
        card_uid  = f'c{i}_{to_m}_{title[:3].replace(" ","")}'
        svg       = _make_sparkline_svg(vals, accent, fmt, card_uid, from_m=from_m, to_m=to_m)
        delay     = 0.06 + i * 0.09
        bdg_lbl, bdg_col, bdg_bg = _badge(cur_m_val, prev_val, fmt)
        prev_str  = _fmt(prev_val, fmt) if prev_val else '\u2014'
        cur_m_str = _fmt(cur_m_val, fmt)
        r, g, b   = int(accent[1:3], 16), int(accent[3:5], 16), int(accent[5:7], 16)

        mom_html = ''
        if bdg_lbl and prev_m_lbl:
            mom_html = (
                f'<div style="display:flex;align-items:center;gap:8px;margin-top:10px;'
                f'padding-top:10px;border-top:1px dashed rgba(0,0,0,.07);">'
                f'<span style="display:inline-flex;align-items:center;gap:4px;'
                f'background:{bdg_bg};color:{bdg_col};font-size:.7rem;font-weight:800;'
                f'padding:3px 10px;border-radius:20px;">{bdg_lbl}</span>'
                f'<span style="font-size:.65rem;font-weight:500;">'
                f'vs {prev_m_lbl}: <b style="color:#6b7280;">{prev_str}</b></span>'
                f'</div>'
            )

        card_html = (
            f'<div style="flex:1;min-width:0;background:#fff;border-radius:24px;overflow:visible;'
            f'box-shadow:0 2px 16px rgba(0,0,0,.07);display:flex;flex-direction:column;'
            f'transition:transform .28s cubic-bezier(.34,1.56,.64,1),box-shadow .28s;'
            f'animation:fadeUp .5s cubic-bezier(.22,1,.36,1) {delay:.2f}s both;'
            f'position:relative;border-top:5px solid {accent};"'
            f' onmouseenter="this.style.transform=\'translateY(-6px)\';this.style.boxShadow=\'0 18px 40px rgba(0,0,0,.13)\'"'
            f' onmouseleave="this.style.transform=\'\';this.style.boxShadow=\'0 2px 16px rgba(0,0,0,.07)\'">'
            f'<div style="padding:20px 20px 14px;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">'
            f'<span style="font-size:.59rem;font-weight:800;color:#9ca3af;text-transform:uppercase;letter-spacing:.13em;">{title}</span>'
            f'<span style="font-size:.56rem;font-weight:700;color:#a78bfa;background:#f5f3ff;padding:2px 8px;border-radius:20px;">{period_lbl}</span>'
            f'</div>'
            f'<div style="display:flex;align-items:baseline;gap:10px;margin-bottom:3px;">'
            f'<span style="font-size:2rem;font-weight:900;color:#111827;letter-spacing:-.05em;line-height:1.05;">{val_str}</span>'
            f'<span style="font-size:.72rem;font-weight:700;color:{accent};background:rgba({r},{g},{b},0.10);padding:2px 9px;border-radius:20px;white-space:nowrap;">{MN[to_m]}: {cur_m_str}</span>'
            f'</div>'
            f'<div style="font-size:.68rem;color:#9ca3af;font-weight:500;">{subtitle}</div>'
            f'{mom_html}'
            f'<div style="margin-top:12px;">{svg}</div>'
            f'</div></div>'
        )
        inner_cards.append(card_html)

    outer = (
        f'<div style="background:linear-gradient(135deg,#faf9ff 0%,#f4f6ff 50%,#f0fff8 100%);'
        f'border-radius:28px;padding:20px;margin-top:24px;margin-bottom:20px;'
        f'box-shadow:0 4px 28px rgba(124,58,237,.09),0 1px 4px rgba(0,0,0,.04);'
        f'border:1.5px solid rgba(167,139,250,.15);animation:fadeUp .4s cubic-bezier(.22,1,.36,1) both;">'
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">'
        f'<span style="font-size:.6rem;font-weight:900;color:#7c3aed;text-transform:uppercase;letter-spacing:.14em;">\U0001f4ca Key Metrics</span>'
        f'<div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(124,58,237,.18),transparent);"></div>'
        f'<span style="font-size:.58rem;font-weight:700;color:#9ca3af;">{period_lbl}</span>'
        f'</div>'
        f'<div style="display:flex;gap:14px;">{"".join(inner_cards)}</div>'
        f'</div>'
    )
    st.markdown(outer, unsafe_allow_html=True)


def _cc(title, subtitle, fig, h=None):
    st.markdown('<div class="cc"><div class="cc-bar"></div>', unsafe_allow_html=True)
    st.markdown(f'<h3 class="cc-title">{title}</h3>', unsafe_allow_html=True)
    st.markdown(f'<p class="cc-sub">{subtitle}</p>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)


def _page_header(breadcrumb, title, subtitle):
    st.markdown(
        f'<div class="ph"><div class="ph-bc">{breadcrumb}</div>'
        f'<h1>{title}</h1>'
        f'<div class="ph-sub">{subtitle}</div></div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════ DATE RANGE PICKER ══════
def date_range_picker(key_prefix, df):
    MIN_DATE = df['Service Date'].min().date()
    MAX_DATE = df['Service Date'].max().date()

    sk, se = f"dr_{key_prefix}_s", f"dr_{key_prefix}_e"
    smode  = f"dr_{key_prefix}_mode"

    if sk    not in st.session_state: st.session_state[sk]    = MIN_DATE
    if se    not in st.session_state: st.session_state[se]    = MAX_DATE
    if smode not in st.session_state: st.session_state[smode] = "Date Range"

    st.markdown(
        '<div class="dr-card"><div class="dr-blob1"></div><div class="dr-blob2"></div>'
        '<div class="dr-header"><div class="dr-title">📅 Date Filter '
        '<span class="dr-title-pill">SELECT MODE</span></div></div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="dr-mode-buttons">', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("📆 Daily",      use_container_width=True, key=f"{key_prefix}_mode_daily"):
            st.session_state[smode] = "Daily"; st.rerun()
    with m2:
        if st.button("📊 Monthly",    use_container_width=True, key=f"{key_prefix}_mode_monthly"):
            st.session_state[smode] = "Monthly"; st.rerun()
    with m3:
        if st.button("📈 Yearly",     use_container_width=True, key=f"{key_prefix}_mode_yearly"):
            st.session_state[smode] = "Yearly"; st.rerun()
    with m4:
        if st.button("📅 Date Range", use_container_width=True, key=f"{key_prefix}_mode_range"):
            st.session_state[smode] = "Date Range"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    mode = st.session_state[smode]

    if mode == "Daily":
        st.markdown('<div style="margin:16px 0;padding:16px;background:#f0f9ff;border-radius:12px;border-left:4px solid #3b82f6;">', unsafe_allow_html=True)
        selected_date = st.date_input("", value=st.session_state[sk], min_value=MIN_DATE, max_value=MAX_DATE, key=f"{key_prefix}_daily_date", label_visibility="collapsed")
        st.session_state[sk] = selected_date
        st.session_state[se] = selected_date
        start = end = selected_date
        cnt = len(df[(df['Service Date'] >= pd.Timestamp(start)) & (df['Service Date'] <= pd.Timestamp(end))])
        st.markdown(f'<div style="margin-top:12px;padding:14px 16px;background:white;border-radius:8px;border:1px solid #bfdbfe;"><span style="font-size:.9rem;font-weight:700;color:#1e40af;">✦ {cnt:,} samples on {start.strftime("%d %b %Y")}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif mode == "Monthly":
        st.markdown('<div style="margin:16px 0;padding:16px;background:#f0fdf4;border-radius:12px;border-left:4px solid #059669;">', unsafe_allow_html=True)
        mc1, mc2 = st.columns(2)
        with mc1:
            selected_month = st.selectbox("", list(MN.values()), key=f"{key_prefix}_month", label_visibility="collapsed")
            month_num = list(MN.values()).index(selected_month) + 1
        with mc2:
            selected_year = st.number_input("", value=MAX_DATE.year, min_value=MIN_DATE.year, max_value=MAX_DATE.year, key=f"{key_prefix}_year", label_visibility="collapsed")
        _, last_day = calendar.monthrange(selected_year, month_num)
        start = pd.Timestamp(year=selected_year, month=month_num, day=1).date()
        end   = pd.Timestamp(year=selected_year, month=month_num, day=last_day).date()
        st.session_state[sk] = start; st.session_state[se] = end
        cnt = len(df[(df['Service Date'] >= pd.Timestamp(start)) & (df['Service Date'] <= pd.Timestamp(end))])
        st.markdown(f'<div style="margin-top:12px;padding:14px 16px;background:white;border-radius:8px;border:1px solid #a7f3d0;"><span style="font-size:.9rem;font-weight:700;color:#065f46;">✦ {cnt:,} samples in {selected_month} {selected_year}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif mode == "Yearly":
        st.markdown('<div style="margin:16px 0;padding:16px;background:#fffbeb;border-radius:12px;border-left:4px solid #f59e0b;">', unsafe_allow_html=True)
        selected_year = st.number_input("", value=MAX_DATE.year, min_value=MIN_DATE.year, max_value=MAX_DATE.year, key=f"{key_prefix}_yearly", label_visibility="collapsed")
        start = pd.Timestamp(year=selected_year, month=1, day=1).date()
        end   = pd.Timestamp(year=selected_year, month=12, day=31).date()
        st.session_state[sk] = start; st.session_state[se] = end
        cnt = len(df[(df['Service Date'] >= pd.Timestamp(start)) & (df['Service Date'] <= pd.Timestamp(end))])
        st.markdown(f'<div style="margin-top:12px;padding:14px 16px;background:white;border-radius:8px;border:1px solid #fde68a;"><span style="font-size:.9rem;font-weight:700;color:#78350f;">✦ {cnt:,} samples in {selected_year}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        c_pill, _ = st.columns([1, 7])
        with c_pill:
            st.markdown('<div class="dr-pill-btn">', unsafe_allow_html=True)
            if st.button("All data", key=f"{key_prefix}_all"):
                st.session_state[sk] = MIN_DATE; st.session_state[se] = MAX_DATE; st.rerun()
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
        st.session_state[sk] = start; st.session_state[se] = end
        if end < start: start, end = end, start
        days = (end - start).days + 1
        cnt  = len(df[(df['Service Date'] >= pd.Timestamp(start)) & (df['Service Date'] <= pd.Timestamp(end))])
        st.markdown(
            f'<div class="dr-summary">'
            f'<span class="dr-sum-from">{start.strftime("%d %b %Y")}</span>'
            f'<span class="dr-sum-arrow">→</span>'
            f'<span class="dr-sum-to">{end.strftime("%d %b %Y")}</span>'
            f'<span class="dr-sum-days">· {days} days</span>'
            f'<span class="dr-sum-badge">✦ {cnt:,} samples</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)
    return start, end


def apply_dr(df, param_rows, s, e):
    ts, te = pd.Timestamp(s), pd.Timestamp(e)
    flt    = df[(df['Service Date'] >= ts) & (df['Service Date'] <= te)].copy()
    fp     = param_rows[(param_rows['Service Date'] >= ts) & (param_rows['Service Date'] <= te)].copy()
    return flt, fp, len(flt)


# ══════════════════════════════════════════════════════ FOOTER ══════
def render_footer():
    st.markdown(
        '<div style="text-align:center;color:#9ca3af;font-size:.64rem;padding:14px 0 6px;'
        'border-top:1.5px solid #e2e6f0;margin-top:12px;letter-spacing:.07em;'
        'font-family:DM Sans,sans-serif;">LABCARE ANALYTICS · LAB SERVICE 2025 · 2,000 RECORDS</div>',
        unsafe_allow_html=True
    )