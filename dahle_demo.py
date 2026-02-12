# --- 3. CSS STYLING (Met Logo Afbeelding) ---
st.markdown(f"""
    <style>
    /* IMPORT FONT (Montserrat) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Montserrat', sans-serif;
    }}

    /* REMOVE DEFAULT ELEMENTS */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stToolbar"] {{ display: none; }}
    
    /* PUSH CONTENT DOWN */
    .block-container {{
        padding-top: 120px !important;
        padding-bottom: 5rem;
    }}
    
    /* --- NAVBAR --- */
    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
        
        background-color: #ffffff;
        padding: 10px 40px; /* Iets minder padding zodat logo past */
        border-bottom: 1px solid #eaeaea;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-sizing: border-box;
    }}
    
    /* LOGO STYLING */
    .nav-logo img {{
        height: 50px; /* Pas dit aan als je logo te groot/klein is */
        margin-top: 5px;
    }}
    
    .nav-links {{
        font-size: 14px;
        font-weight: 600;
        color: #333;
        display: flex;
        gap: 30px;
    }}
    .nav-links span {{ cursor: pointer; transition: 0.2s; }}
    .nav-links span:hover {{ color: #9b59b6; }}
    
    .nav-btn {{
        background-color: #9b59b6;
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        cursor: pointer;
    }}
    
    /* --- CARD STYLING --- */
    .option-card {{
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
    }}
    .option-card:hover {{
        border-color: #9b59b6;
        background-color: #2e2e2e;
        transform: translateY(-5px);
    }}
    .card-icon {{ font-size: 50px; margin-bottom: 20px; margin-top: 10px; }}
    .card-title {{ font-size: 20px; font-weight: 700; color: white; margin-bottom: 15px; }}
    .card-desc {{ font-size: 14px; color: #aaa; line-height: 1.6; }}

    /* BUTTONS */
    div.stButton > button {{
        background-color: #9b59b6;
        color: white;
        border-radius: 30px;
        padding: 12px 28px;
        font-weight: 700;
        border: none;
        width: 100%;
        margin-top: 10px;
    }}
    div.stButton > button:hover {{
        background-color: #af6bca;
        color: white;
    }}
    
    /* FORMS */
    div[data-baseweb="input"] {{ background-color: #333; border-radius: 8px; }}
    div[data-baseweb="input"] input {{ color: white; }}
    label {{ color: #ccc !important; font-weight: 600; margin-bottom: 5px; }}
    
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
