import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Dahle Transport", 
    page_icon="🚚", 
    layout="wide",
    initial_sidebar_state="collapsed" # Hij start dicht
)

# --- 2. SESSION STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- 3. CSS STYLING (Met Admin Knop Fix) ---
st.markdown("""
    <style>
    /* IMPORT FONT (Montserrat) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* --- HEADER FIX (Zorgt dat je de sidebar weer kunt openen) --- */
    
    /* We maken de header transparant in plaats van onzichtbaar */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 100000; /* Zorg dat dit BOVEN de witte navbar ligt */
    }
    
    /* Verberg de gekleurde streep en 'running man' icoontjes */
    div[data-testid="stDecoration"] { display: none; }
    div[data-testid="stStatusWidget"] { visibility: hidden; }

    /* Stijl de Sidebar-Toggle knop (pijltje linksboven) */
    button[kind="header"] {
        color: #333 !important; /* Donkergrijs */
        background-color: transparent !important;
        font-weight: bold;
    }
    /* Als je eroverheen muist */
    button[kind="header"]:hover {
        color: #9b59b6 !important; /* Paars */
        background-color: #f0f0f0 !important;
    }

    /* Verberg footer "Made with Streamlit" */
    footer {visibility: hidden;}
    
    /* PUSH CONTENT DOWN (Ruimte voor de navbar) */
    .block-container {
        padding-top: 140px !important;
        padding-bottom: 5rem;
    }
    
    /* --- NAVBAR (Vaste Hoogte) --- */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100px;
        z-index: 9999; /* Net onder de header-knop */
        
        background-color: #ffffff;
        padding: 0px 40px;
        border-bottom: 1px solid #eaeaea;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
    }
    
    /* LOGO */
    .nav-logo img {
        height: 55px;
        margin-top: 0px;
    }
    
    /* LINKS */
    .nav-links {
        font-size: 15px;
        font-weight: 600;
        color: #333;
        display: flex;
        gap: 30px;
        margin-left: 50px; /* Beetje ruimte voor de sidebar knop */
    }
    .nav-links span { cursor: pointer; transition: 0.2s; }
    .nav-links span:hover { color: #9b59b6; }
    
    .nav-btn {
        background-color: #9b59b6;
        color: white;
        padding: 12px 28px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
    }
    
    /* --- CARD STYLING --- */
    .option-card {
        background-color: #262626;
        border: 2px solid #333;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        transition: 0.3s;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .option-card:hover {
        border-color: #9b59b6;
        background-color: #2e2e2e;
        transform: translateY(-5px);
    }
    .card-icon { font-size: 50px; margin-bottom: 20px; margin-top: 10px; }
    .card-title { font-size: 20px; font-weight: 700; color: white; margin-bottom: 15px; }
    .card-desc { font-size: 14px; color: #aaa; line-height: 1.6; }

    /* BUTTONS */
    div.stButton > button {
        background-color: #9b59b6;
        color: white;
        border-radius: 30px;
        padding: 12px 28px;
        font-weight: 700;
        border: none;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        background-color: #af6bca;
        color: white;
    }
    
    /* FORMS */
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; margin-bottom: 5px; }
    
    </style>
    
    <div class="navbar">
        <div class="nav-logo">
            <img src="https://cloud-1de12d.becdn.net/media/original/964295c9ae8e693f8bb4d6b70862c2be/logo-website-top-png-1-.webp" alt="Dahle Transport Logo">
        </div>
        <div class="nav-links">
            <span>Home</span>
            <span>About Us</span>
            <span>Services</span>
            <span>Gallery</span>
            <span>Contact</span>
        </div>
        <div class="nav-btn">CONTACT US</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. CONTROLS (Sidebar - Nu weer bereikbaar!) ---
with st.sidebar:
    st.header("⚙️ Admin / Demo Controls")
    st.info("Gebruik dit menu om te schakelen tussen de Klant-view en de Planner-view.")
    
    mode = st.radio("Kies Scherm:", ["🌐 Customer Website", "🔒 Internal Planner System"])
    
    st.divider()
    if st.button("Reset Demo Data"):
        st.session_state.orders = []
        st.session_state.step = 1
        st.rerun()

# =========================================================
# VIEW 1: CUSTOMER WEBSITE
# =========================================================
if mode == "🌐 Customer Website":
    
    col_spacer_L, col_main, col_spacer_R = st.columns([1, 3, 1])
    
    with col_main:
        
        # --- HEADER ---
        st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>📦 Create new shipment</h2>", unsafe_allow_html=True)
        
        # --- WIZARD STEP 1: SELECT TYPE ---
        if st.session_state.step == 1:
            st.write("Select the type of goods you want to ship:", unsafe_allow_html=False)
            st.write("") 
            
            c_card1, c_card2, c_card3 = st.columns(3)
            
            with c_card1:
                st.markdown("""
                <div class="option-card">
                    <div class="card-icon">📦</div>
                    <div class="card-title">Parcels & Docs</div>
                    <div class="card-desc">Small boxes, envelopes, and urgent documents up to 30kg.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Select Parcels"):
                    st.session_state.selected_type = "Parcels/Docs"
                    st.session_state.step = 2
                    st.rerun()

            with c_card2:
                st.markdown("""
                <div class="option-card">
                    <div class="card-icon">🚛</div>
                    <div class="card-title">Freight / Pallets</div>
                    <div class="card-desc">Euro pallets, industrial goods, and bulk cargo over 30kg.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Select Freight"):
                    st.session_state.selected_type = "Freight/Pallets"
                    st.session_state.step = 2
                    st.rerun()

            with c_card3:
                st.markdown("""
                <div class="option-card">
                    <div class="card-icon">❄️</div>
                    <div class="card-title">Special Transport</div>
                    <div class="card-desc">Refrigerated, hazardous (ADR), or oversized loads.</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Select Special"):
                    st.session_state.selected_type = "Special Transport"
                    st.session_state.step = 2
                    st.rerun()

        # --- WIZARD STEP 2: FORM ---
        elif st.session_state.step == 2:
            st.markdown(f"<h4 style='text-align: center;'>Details for: <span style='color:#9b59b6'>{st.session_state.selected_type}</span></h4>", unsafe_allow_html=True)
            st.write("")
            
            with st.container(border=True):
                with st.form("details_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        company = st.text_input("Company Name")
                        contact = st.text_input("Contact Person")
                        email = st.text_input("Email Address")
                    with c2:
                        pickup = st.text_input("Pickup Address")
                        delivery = st.text_input("Delivery Address")
                        weight = st.number_input("Total Weight (kg)", min_value=1)
                    
                    st.markdown("---")
                    
                    bc1, bc2 = st.columns([1, 4])
                    with bc1:
                        back = st.form_submit_button("← Back")
                    with bc2:
                        next_step = st.form_submit_button("Review Order →")
                    
                if back:
                    st.session_state.step = 1
                    st.rerun()
                
                if next_step:
                    if company and email:
                        st.session_state.temp_order = {
                            "company": company, "contact": contact, "email": email,
                            "route": f"{pickup} ➝ {delivery}", "weight": weight,
                            "type": st.session_state.selected_type
                        }
                        st.session_state.step = 3
                        st.rerun()
                    else:
                        st.error("Please fill in Company Name and Email.")

        # --- WIZARD STEP 3: CONFIRM ---
        elif st.session_state.step == 3:
            st.markdown("<h4 style='text-align: center;'>Review your request</h4>", unsafe_allow_html=True)
            o = st.session_state.temp_order
            
            with st.container(border=True):
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.write(f"**Customer:** {o['company']}")
                    st.write(f"**Email:** {o['email']}")
                    st.write(f"**Type:** {o['type']}")
                with col_s2:
                    st.write(f"**Route:** {o['route']}")
                    st.write(f"**Weight:** {o['weight']} kg")
            
            st.write("")
            c_b1, c_b2 = st.columns([1, 3])
            with c_b1:
                if st.button("← Edit"):
                    st.session_state.step = 2
                    st.rerun()
            with c_b2:
                if st.button("✅ CONFIRM & SEND REQUEST"):
                    final_order = o.copy()
                    final_order['id'] = len(st.session_state.orders) + 1001
                    final_order['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    final_order['status'] = "New"
                    st.session_state.orders.append(final_order)
                    
                    st.balloons()
                    st.success("Your transport request has been sent successfully!")
                    time.sleep(2.5)
                    st.session_state.step = 1
                    st.rerun()

# =========================================================
# VIEW 2: INTERNAL PLANNER
# =========================================================
elif mode == "🔒 Internal Planner System":
    st.title("🔒 Planner Dashboard")
    st.markdown("Internal Use Only | Dahle Transport System v1.0")
    st.markdown("---")

    col_list, col_view = st.columns([1, 2])
    
    with col_list:
        st.subheader("📥 Inbox")
        if not st.session_state.orders:
            st.info("No new orders received.")
        
        for order in reversed(st.session_state.orders):
            status_icon = "🔴" if order['status'] == "New" else "🟢"
            
            with st.container(border=True):
                st.write(f"**{status_icon} {order['company']}**")
                st.caption(f"{order['type']} | {order['date']}")
                if st.button(f"Open #{order['id']}", key=order['id']):
                    st.session_state.selected_order = order

    with col_view:
        st.subheader("📋 Order Processing")
        
        if 'selected_order' in st.session_state:
            sel = st.session_state.selected_order
            
            with st.container(border=True):
                st.markdown(f"### Order #{sel['id']}")
                st.write(f"**Customer:** {sel['company']} ({sel['contact']})")
                st.write(f"**Email:** {sel['email']}")
                st.markdown("---")
                st.write(f"📍 **Route:** {sel['route']}")
                st.write(f"⚖️ **Weight:** {sel['weight']} kg")
                st.write(f"📦 **Type:** {sel['type']}")
            
            st.write("### Planner Actions")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("✅ Approve"):
                    sel['status'] = "Approved"
                    st.success("Order Approved!")
                    st.rerun()
            with c2:
                if st.button("📞 Call Client"):
                    st.info("Marked for callback.")
            with c3:
                if st.button("❌ Reject"):
                    sel['status'] = "Rejected"
                    st.error("Order Rejected.")
                    st.rerun()
        else:
            st.info("Select an order from the list on the left.")
