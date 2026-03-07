import streamlit as st

st.set_page_config(
    page_title="LabCare · Login",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Redirect if already logged in ──
if st.session_state.get("logged_in"):
    st.switch_page("pages/Financial.py")

# ── Users ──
USERS = {
    "finance":    {"password": "finance123",    "role": "Finance",    "display": "Finance Team",     "page": "Financial"},
    "customer":   {"password": "customer123",   "role": "Customer",   "display": "Customer Service", "page": "Customer"},
    "technique":  {"password": "technique123",  "role": "Technique",  "display": "Technique Team",   "page": "Analysis"},
    "superadmin": {"password": "superadmin123", "role": "SuperAdmin", "display": "Super Admin",      "page": "Financial"},
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,600;9..40,700;9..40,900&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:linear-gradient(135deg,#0a0820 0%,#130e3d 50%,#1c1548 100%);min-height:100vh}
#MainMenu,footer,header,[data-testid="stSidebarCollapseButton"],[data-testid="collapsedControl"]{display:none!important;visibility:hidden!important}
.block-container{padding:0!important;max-width:100%!important}

/* ── Login card ── */
.login-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:24px}
.login-card{background:rgba(255,255,255,.04);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,.10);border-radius:32px;padding:48px 44px 40px;width:100%;max-width:420px;box-shadow:0 32px 80px rgba(0,0,0,.45),0 0 0 1px rgba(124,58,237,.15) inset;animation:fadeUp .55s cubic-bezier(.22,1,.36,1) both}
.login-logo{text-align:center;margin-bottom:32px}
.login-logo-icon{font-size:3rem;margin-bottom:10px;display:block}
.login-logo-title{font-size:1.6rem;font-weight:900;color:#fff;letter-spacing:-.05em}
.login-logo-pill{display:inline-block;background:rgba(124,58,237,.35);color:#c4b5f4;font-size:.6rem;font-weight:800;padding:3px 10px;border-radius:20px;letter-spacing:.1em;margin-left:8px;vertical-align:middle}
.login-logo-sub{font-size:.72rem;color:rgba(184,176,232,.5);margin-top:6px;font-weight:500}
.login-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,.25),transparent);margin:24px 0}
.login-field-label{font-size:.7rem;font-weight:800;color:rgba(196,181,244,.7);text-transform:uppercase;letter-spacing:.12em;margin-bottom:6px;display:block}
.login-hint{font-size:.65rem;color:rgba(167,139,250,.45);margin-top:16px;text-align:center;line-height:1.6}
.login-hint b{color:rgba(167,139,250,.7)}

/* Input overrides for dark bg */
[data-testid="stTextInputRootElement"] input{background:rgba(255,255,255,.08)!important;color:#fff!important;border:1.5px solid rgba(255,255,255,.12)!important;border-radius:12px!important;font-family:'DM Sans',sans-serif!important;font-size:.92rem!important;font-weight:500!important;padding:12px 16px!important}
[data-testid="stTextInputRootElement"] input:focus{border-color:#a78bfa!important;box-shadow:0 0 0 4px rgba(124,58,237,.22)!important;background:rgba(255,255,255,.11)!important}
[data-testid="stTextInputRootElement"] input::placeholder{color:rgba(196,181,244,.35)!important}

/* Login button */
.login-btn .stButton button{background:linear-gradient(135deg,#7c3aed,#5b21b6)!important;color:#fff!important;border:none!important;border-radius:14px!important;padding:14px!important;font-size:1rem!important;font-weight:800!important;width:100%!important;letter-spacing:.03em!important;box-shadow:0 8px 24px rgba(124,58,237,.45)!important;transition:all .2s cubic-bezier(.34,1.56,.64,1)!important;margin-top:8px!important}
.login-btn .stButton button:hover{background:linear-gradient(135deg,#6d28d9,#4c1d95)!important;transform:translateY(-2px)!important;box-shadow:0 14px 32px rgba(124,58,237,.55)!important}

/* Error message */
.login-error{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.3);border-radius:12px;padding:12px 16px;color:#fca5a5;font-size:.82rem;font-weight:600;margin-top:10px;text-align:center}

/* Demo badge strip */
.demo-strip{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:18px}
.demo-badge{background:rgba(124,58,237,.18);border:1px solid rgba(167,139,250,.2);border-radius:8px;padding:5px 12px;font-size:.62rem;font-weight:700;color:rgba(196,181,244,.7);letter-spacing:.06em}

@keyframes fadeUp{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
</style>
""", unsafe_allow_html=True)

# ── Login card markup ──
st.markdown("""
<div class="login-wrap">
  <div class="login-card">
    <div class="login-logo">
      <span class="login-logo-icon">🧪</span>
      <div>
        <span class="login-logo-title">LabCare</span>
        <span class="login-logo-pill">2025</span>
      </div>
      <div class="login-logo-sub">Analytics Dashboard · 2,000 records</div>
    </div>
    <div class="login-divider"></div>
""", unsafe_allow_html=True)

st.markdown('<span class="login-field-label">Username</span>', unsafe_allow_html=True)
username = st.text_input("", placeholder="Enter username", key="login_user", label_visibility="collapsed")

st.markdown('<span class="login-field-label" style="margin-top:14px;display:block;">Password</span>', unsafe_allow_html=True)
password = st.text_input("", placeholder="Enter password", type="password", key="login_pass", label_visibility="collapsed")

# ── Login button ──
st.markdown('<div class="login-btn" style="margin-top:20px;">', unsafe_allow_html=True)
login_clicked = st.button("Sign In →", use_container_width=True, key="login_btn")
st.markdown('</div>', unsafe_allow_html=True)

# ── Auth logic ──
if login_clicked:
    user_data = USERS.get(username.strip().lower())
    if user_data and user_data["password"] == password:
        st.session_state["logged_in"] = True
        st.session_state["username"]  = username.strip().lower()
        st.session_state["user"]      = user_data
        st.switch_page(f"pages/{user_data['page']}.py")
    else:
        st.markdown('<div class="login-error">❌ Invalid username or password. Please try again.</div>', unsafe_allow_html=True)

# ── Demo hints ──
st.markdown("""
    <div class="login-hint">Demo accounts</div>
    <div class="demo-strip">
      <span class="demo-badge">finance / finance123</span>
      <span class="demo-badge">customer / customer123</span>
      <span class="demo-badge">technique / technique123</span>
      <span class="demo-badge">superadmin / superadmin123</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)