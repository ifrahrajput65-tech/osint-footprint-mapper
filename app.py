import streamlit as st
import base64
from platforms import PLATFORMS
from core import scan_platforms

# Page configuration
st.set_page_config(
    page_title="OSINT Social Footprint Mapper", 
    page_icon="🛡️", 
    layout="centered"
)

# Function to load and encode background image
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

img_base64 = get_base64_of_bin_file("bg.jpg")

# Custom CSS with visible background and large stylish title
st.markdown(f"""
    <style>
    /* Background Image Styling with lighter overlay so background shows nicely */
    .stApp {{
        background-image: linear-gradient(rgba(10, 10, 15, 0.5), rgba(10, 10, 15, 0.5)), url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f3f4f6;
    }}
    
    /* Big, Stylish, Glowing Neon Title */
    .main-title {{
        font-size: 3rem;
        font-weight: 900;
        color: #fb7185;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 5px;
        text-shadow: 0 0 25px rgba(251, 113, 133, 0.8), 0 0 10px rgba(225, 29, 72, 0.6);
        letter-spacing: 1px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    .sub-title {{
        text-align: center;
        color: #e2e8f0;
        font-size: 1.1rem;
        margin-bottom: 30px;
        font-weight: 500;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }}

    /* Clean Input box styling with dark glass effect */
    .stTextInput > div > div > input {{
        background-color: rgba(15, 15, 25, 0.85);
        color: #ffffff;
        border: 2px solid #e11d48;
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #fb7185;
        box-shadow: 0 0 15px rgba(251, 113, 133, 0.6);
    }}

    /* Prominent glowing button styling */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #e11d48 0%, #9f1239 100%);
        color: white;
        border-radius: 12px;
        font-weight: 800;
        font-size: 16px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(225, 29, 72, 0.6);
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%);
        box-shadow: 0 6px 25px rgba(251, 113, 133, 0.8);
        transform: translateY(-2px);
    }}
    </style>
""", unsafe_allow_html=True)

# Header Section with large stylish title
st.markdown('<p class="main-title">🛡️ OSINT Social Footprint Mapper</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Digital Footprint & Identity Reconnaissance Tool</p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# User Input Form
query = st.text_input("Target Identifier", placeholder="e.g., target_username or target@gmail.com")

if st.button("🚀 Initialize Scan"):
    if not query.strip():
        st.warning("⚠️ Please enter a valid username or email address.")
    else:
        with st.spinner("🔍 Scanning public nodes and analyzing digital footprint..."):
            username, found_accounts = scan_platforms(query, PLATFORMS)
        
        st.success(f"Target Processed: `{username}`")
        st.markdown(f"### 🎯 Found Active Profiles ({len(found_accounts)})")
        
        if found_accounts:
            for acc in found_accounts:
                # Glassmorphism cards with gorgeous pink/rose styling
                st.markdown(f"""
                    <div style="background: rgba(15, 15, 25, 0.85); backdrop-filter: blur(12px); padding: 16px 20px; border-radius: 12px; border-left: 6px solid #fb7185; margin-bottom: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.5);">
                        <span style="color: #fb7185; font-size: 18px; font-weight: 800;">{acc['platform']}</span><br>
                        <a href="{acc['url']}" target="_blank" style="color: #fbcfe8; text-decoration: none; font-size: 15px; word-break: break-all;">{acc['url']}</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No public profiles found matching this identifier on the scanned platforms.")