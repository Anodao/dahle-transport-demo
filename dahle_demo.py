import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIG (Moet altijd als eerste) ---
st.set_page_config(
    page_title="Dahle Transport", 
    page_icon="🚚", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- 3. ADVANCED CSS (Stijl van de website) ---
st.markdown("""
    <style>
    /* IMPORT FONT (Montserrat) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;800&display=swap');

    /* ALGEMEEN FONT */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* VERBERG STREAMLIT ELEMENTEN (Header, Footer, Menu) */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] { display: none; }
    [data-testid="stToolbar"] { display: none; }
    
    /* NAVIGATIEBALK BOVENAAN */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 5rem;
    }
    
    .navbar {
        background-color: #1a1a1a;
        padding: 15px 40px;
        border-bottom: 1px solid #333;
        margin-bottom: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .nav-logo {
        font-size: 24px;
        font-weight: 800;
        color: white;
        text-transform: italic;
    }
    .nav-logo span { color: #9b59b6; }
    
    .nav-links {
        font-size: 14px;
        font-weight: 600;
        color: #ddd;
        display: flex;
        gap: 30px;
    }
    .nav-links span { cursor: pointer; transition: 0.2s; }
    .nav-links span:hover { color: #9b59b6; }
    
    .nav-btn {
        background-color: #9b59b6;
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
    }

    /* HERO TEXT (Slogan) */
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        line-height: 1.1;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    /* KAARTEN STIJL */
    .option-card {
        background-color: #262626;
        border: 2px solid #333;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .option-card:hover {
        border-color: #9b59b6;
        transform: translateY(-5px);
        background-color: #2e2e2e;
    }
    .card-icon { font-size: 40px; margin-bottom: 15px; }
    .card-title { font-size: 18px; font-weight: 700; color: white; margin-bottom: 10px; }
    .card-desc { font-size: 13px; color: #aaa; }

    /* KNOPPEN STIJL */
    div.stButton > button {
        background-color: #9b59b6;
        color: white;
        border-radius: 30px;
        padding: 12px 28px;
        font-weight: 700;
        border: none;
        transition: 0.2s;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #af6bca;
        color: white;
    }
    
    /* INPUT VELDEN DONKER */
    div[data-baseweb="input"] { background-color: #333; border-radius: 8px; }
    div[data-baseweb="input"] input { color: white; }
    label { color: #ccc !important; font-weight: 600; }
    
    </style>
    
    <div class="navbar">
        <div class="nav-logo"><span>dt</span> Dahle Transport</div>
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

# --- 4. VIEW MODE SELECTIE (Verborgen in Sidebar) ---
with st.sidebar:
    st.header("⚙️ Demo Controls")
    mode = st.radio("View Mode:", ["🌐 Customer Website", "🔒 Internal Planner System"])
    st.divider()
    if st.button("Reset Demo Data"):
        st.session_state.orders = []
        st.session_state.step = 1
        st.rerun()

# =========================================================
# VIEW 1: CUSTOMER WEBSITE (Schoon & Strak)
# =========================================================
if mode == "🌐 Customer Website":
    
    # --- HERO SECTION (Zonder openingstijden/extra tekst) ---
    c_hero1, c_hero2 = st.columns([1.2, 1])
    
    with c_hero1:
        # Alleen de grote slogan
        st.markdown('<div class="hero-title">We get it done!</div>', unsafe_allow_html=True)
        # Hier is de "0" en de extra tekst verwijderd

    with c_hero2:
        st.image("https://cdn.pixabay.com/photo/2017/10/04/17/23/truck-2816898_1280.jpg", use_container_width=True)

    st.markdown("---")
    
    # --- WIZARD SECTION ---
    st.markdown("### 📦 Create new shipment")
    
    # STEP 1: KIES TYPE (KAARTEN)
    if st.session_state.step == 1:
        st.write("Select the type of goods you want to ship:")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
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

        with col_b:
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

        with col_c:
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

    # STEP 2: INVUL FORMULIER
    elif st.session_state.step == 2:
        st.markdown(f"#### Details for: **{st.session_state.selected_type}**")
        
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

    # STEP 3: BEVESTIGING
    elif st.session_state.step == 3:
        st.markdown("#### Review your request")
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
        
        c_b1, c_b2 = st.columns([1, 3])
        with c_b1:
            if st.button("← Edit"):
                st.session_state.step = 2
                st.rerun()
        with c_b2:
            if st.button("✅ CONFIRM & SEND REQUEST"):
                # "Database" opslaan
                final_order = o.copy()
                final_order['id'] = len(st.session_state.orders) + 1001
                final_order['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                final_order['status'] = "New"
                st.session_state.orders.append(final_order)
                
                st.balloons()
                st.success("Your transport request has been sent successfully!")
                time.sleep(3)
                st.session_state.step = 1
                st.rerun()

# =========================================================
# VIEW 2: INTERNAL PLANNER (Back-end)
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
                if st.button("✅ Approve & Plan"):
                    sel['status'] = "Approved"
                    st.success("Order Approved!")
                    st.rerun()
            with c2:
                if st.button("📞 Needs Info"):
                    st.info("Marked for callback.")
            with c3:
                if st.button("❌ Reject"):
                    sel['status'] = "Rejected"
                    st.error("Order Rejected.")
                    st.rerun()
        else:
            st.info("Select an order from the list on the left.")
