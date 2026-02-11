import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dahle Transport Demo", page_icon="🚚", layout="wide")

# --- CUSTOM CSS STYLING (Dark Mode & Dahle Colors) ---
st.markdown("""
    <style>
    /* Main background color (Dark Theme) */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Styling buttons to match the purple Dahle brand color */
    div.stButton > button {
        background-color: #804080;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #9e5a9e;
        border-color: white;
    }

    /* Styling inputs */
    div[data-baseweb="input"] { background-color: #2d2d2d; }
    div[data-baseweb="select"] { background-color: #2d2d2d; }
    label { color: #d0d0d0 !important; }

    /* Tabs styling */
    button[data-baseweb="tab"] { color: #ffffff; }
    button[data-baseweb="tab"][aria-selected="true"] { background-color: #804080 !important; }
    
    /* Text styling */
    h1, h2, h3 { color: white !important; font-family: sans-serif; }
    .big-slogan { font-size: 3em; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)


# --- SESSION STATE INITIALIZATION ---
if 'orders' not in st.session_state:
    st.session_state.orders = []

# =========================================
# --- HERO SECTION (Clean Version) ---
# =========================================
col_hero_text, col_hero_img = st.columns([3, 2], gap="medium")

with col_hero_text:
    st.markdown("# Dahle Transport")
    st.markdown('<div class="big-slogan">We get it done!</div>', unsafe_allow_html=True)
    st.markdown("### Fast and secure transport.")
    
    st.write("") # Witregel
    st.button("CONTACT US")

with col_hero_img:
    # Hier is de fix: 'use_container_width' in plaats van 'use_column_width'
    st.image("https://cdn.pixabay.com/photo/2017/10/04/17/23/truck-2816898_1280.jpg", use_container_width=True)

st.markdown("---")

# =========================================
# --- THE DEMO TABS ---
# =========================================
tab_customer, tab_system, tab_planner = st.tabs(["1. CUSTOMER (Website)", "2. SYSTEM (Processing)", "3. PLANNER (Dashboard)"])

# --- TAB 1: CUSTOMER ---
with tab_customer:
    st.subheader("1. New Transport Request")
    
    with st.form("order_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email Address")
        with col2:
            pickup_loc = st.text_input("Pickup Address")
            delivery_loc = st.text_input("Delivery Address")
            load_type = st.selectbox("Load Type", ["Pallets (Euro)", "Container", "Single Box", "Special Transport"])
            weight = st.number_input("Weight (kg)", min_value=0)

        submit_button = st.form_submit_button("Send Order Request")

    if submit_button:
        new_order = {
            "id": len(st.session_state.orders) + 1001,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "company": company_name,
            "route": f"{pickup_loc} ➝ {delivery_loc}",
            "load": f"{load_type} ({weight} kg)",
            "email": email,
            "status": "New"
        }
        st.session_state.orders.append(new_order)
        st.success("✅ Order request received.")
        st.info(f"📧 Confirmation email sent to: {email}")

# --- TAB 2: SYSTEM ---
with tab_system:
    st.subheader("2. Automated Processing")
    st.write("Background process simulation:")
    st.markdown("""
    * **Status:** 🟢 Online
    * **Database:** Connected
    * **Email Service:** Active
    """)
    
    st.divider()
    if st.session_state.orders:
        st.dataframe(pd.DataFrame(st.session_state.orders), use_container_width=True)
    else:
        st.warning("No orders in database.")

# --- TAB 3: PLANNER ---
with tab_planner:
    st.subheader("3. Planner Dashboard")

    col_list, col_detail = st.columns([1, 2])

    with col_list:
        st.markdown("#### 📥 Inbox")
        if not st.session_state.orders:
            st.write("No new tasks.")
        
        for order in reversed(st.session_state.orders):
            with st.container(border=True):
                st.write(f"**{order['company']}**")
                st.caption(f"#{order['id']} | {order['date']}")
                if st.button(f"Open #{order['id']}", key=order['id']):
                    st.session_state.selected_order = order

    with col_detail:
        st.markdown("#### 📋 Order Details")
        
        if 'selected_order' in st.session_state:
            o = st.session_state.selected_order
            with st.container(border=True):
                st.info(f"**Request from:** {o['company']}")
                st.write(f"**Route:** {o['route']}")
                st.write(f"**Load:** {o['load']}")
                st.write(f"**Contact:** {o['email']}")
            
            st.write("### Action")
            action = st.radio("Decision:", ["Approve & Schedule", "Contact Client", "Reject"], horizontal=True)
            
            if st.button("Process"):
                with st.spinner("Processing..."):
                    time.sleep(0.5)
                st.success(f"Order #{o['id']} updated: **{action}**")
        else:
            st.info("Select an order to view details.")