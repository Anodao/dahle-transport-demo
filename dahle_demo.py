import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dahle Transport Portal", page_icon="🚚", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if 'orders' not in st.session_state:
    st.session_state.orders = []
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'selected_type' not in st.session_state:
    st.session_state.selected_type = None
if 'temp_order' not in st.session_state:
    st.session_state.temp_order = {}

# --- CUSTOM CSS (Dahle Dark Theme + Card Styling) ---
st.markdown("""
    <style>
    /* Dark Background */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Buttons (Dahle Purple) */
    div.stButton > button {
        background-color: #804080;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #9e5a9e;
        color: white;
    }

    /* Card Styling for Step 1 */
    .transport-card {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
        text-align: center;
        height: 250px;
        margin-bottom: 10px;
    }
    .transport-card h3 {
        color: #fff;
    }
    .transport-card p {
        color: #aaa;
        font-size: 0.9em;
    }
    
    /* Progress Bar Style */
    .step-indicator {
        font-size: 1.2em;
        font-weight: bold;
        color: #804080;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚚 Dahle Transport")
with col2:
    if st.button("Reset Demo"):
        st.session_state.step = 1
        st.session_state.orders = []
        st.rerun()

st.markdown("---")

# --- MAIN TABS ---
tab_customer, tab_planner = st.tabs(["1. CUSTOMER PORTAL (Wizard Flow)", "2. PLANNER DASHBOARD"])

# =========================================================
# TAB 1: CUSTOMER (The DHL-style Wizard)
# =========================================================
with tab_customer:
    
    # Progress Indicator
    steps = ["1. Shipment Type", "2. Details", "3. Confirm"]
    st.markdown(f"<div class='step-indicator'>Step {st.session_state.step} of 3: {steps[st.session_state.step-1]}</div>", unsafe_allow_html=True)
    
    # --- STEP 1: SELECT TYPE (Like the DHL Cards) ---
    if st.session_state.step == 1:
        st.subheader("What would you like to ship today?")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            with st.container(border=True):
                st.markdown("### 📦 Parcels & Docs")
                st.markdown("_(Up to 30kg)_")
                st.write("Small boxes, envelopes, and urgent documents.")
                st.write("")
                st.write("")
                if st.button("Select Parcels"):
                    st.session_state.selected_type = "Parcel/Document"
                    st.session_state.step = 2
                    st.rerun()

        with col_b:
            with st.container(border=True):
                st.markdown("### 🚛 Freight / Pallets")
                st.markdown("_(Over 30kg)_")
                st.write("Euro pallets, industrial goods, and bulk cargo.")
                st.write("")
                st.write("")
                if st.button("Select Freight"):
                    st.session_state.selected_type = "Freight/Pallet"
                    st.session_state.step = 2
                    st.rerun()

        with col_c:
            with st.container(border=True):
                st.markdown("### ❄️ Special Transport")
                st.markdown("_(Custom)_")
                st.write("Refrigerated, hazardous, or oversized loads.")
                st.write("")
                st.write("")
                if st.button("Select Special"):
                    st.session_state.selected_type = "Special Transport"
                    st.session_state.step = 2
                    st.rerun()

    # --- STEP 2: FILL DETAILS ---
    elif st.session_state.step == 2:
        st.subheader(f"Enter details for: {st.session_state.selected_type}")
        
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
            
            # Button Row
            bc1, bc2 = st.columns([1, 4])
            with bc1:
                back = st.form_submit_button("← Back")
            with bc2:
                next_step = st.form_submit_button("Review Shipment →")
            
        if back:
            st.session_state.step = 1
            st.rerun()
            
        if next_step:
            if company and email and pickup:
                # Save to temp
                st.session_state.temp_order = {
                    "company": company,
                    "contact": contact,
                    "email": email,
                    "route": f"{pickup} ➝ {delivery}",
                    "weight": weight,
                    "type": st.session_state.selected_type
                }
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please fill in the required fields (Company, Email, Pickup).")

    # --- STEP 3: SUMMARY & CONFIRM ---
    elif st.session_state.step == 3:
        st.subheader("Review your request")
        
        o = st.session_state.temp_order
        
        with st.container(border=True):
            st.info(f"**Type:** {o['type']}")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write(f"**Customer:** {o['company']} ({o['contact']})")
                st.write(f"**Email:** {o['email']}")
            with col_s2:
                st.write(f"**Route:** {o['route']}")
                st.write(f"**Weight:** {o['weight']} kg")

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            if st.button("← Edit"):
                st.session_state.step = 2
                st.rerun()
        with col_b2:
            if st.button("✅ CONFIRM & SEND ORDER"):
                # Save to real database
                final_order = o.copy()
                final_order['id'] = len(st.session_state.orders) + 2024
                final_order['date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                final_order['status'] = "New"
                
                st.session_state.orders.append(final_order)
                
                st.success("Order successfully sent!")
                time.sleep(2)
                st.session_state.step = 1
                st.rerun()

# =========================================================
# TAB 2: PLANNER (The Dashboard)
# =========================================================
with tab_planner:
    st.subheader("Planner Dashboard (Incoming Requests)")
    
    col_list, col_view = st.columns([1, 2])
    
    with col_list:
        st.markdown("#### 📥 Inbox")
        if not st.session_state.orders:
            st.caption("No active orders.")
        
        for order in reversed(st.session_state.orders):
            with st.container(border=True):
                st.write(f"**{order['company']}**")
                st.caption(f"{order['type']} | {order['date']}")
                if st.button(f"Open #{order['id']}", key=order['id']):
                    st.session_state.selected_order = order

    with col_view:
        st.markdown("#### 📋 Order Details")
        
        if 'selected_order' in st.session_state:
            sel = st.session_state.selected_order
            
            with st.container(border=True):
                st.markdown(f"### Order #{sel['id']}")
                st.write(f"**Customer:** {sel['company']}")
                st.write(f"**Type:** {sel['type']}")
                st.markdown("---")
                st.write(f"📍 **Route:** {sel['route']}")
                st.write(f"⚖️ **Weight:** {sel['weight']} kg")
                st.write(f"✉️ **Contact:** {sel['email']}")
            
            st.write("### Actions")
            c_act1, c_act2, c_act3 = st.columns(3)
            with c_act1:
                st.button("✅ Approve")
            with c_act2:
                st.button("📞 Call Client")
            with c_act3:
                st.button("❌ Reject")
        else:
            st.info("Select an order from the list to view details.")
