import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="EduGemma AI — Multimodal Science & Math Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Animations, Professional Theme & Styling
st.markdown("""
    <style>
    /* Main Theme Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Animated Gradient Title */
    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 3s infinite alternate;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.2);
    }

    /* Custom Styled Buttons with Hover Effects */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        font-weight: 700;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1.05rem;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #4f46e5 0%, #9333ea 100%);
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Status Badge */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="badge">🚀 Gemma 4 Hackathon Entry | Open-Source Agent Skill</div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">EduGemma AI Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Next-Gen Multimodal Science & Mathematics Personal Tutor</p>', unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/brain.png", width=70)
    st.title("Control Center")
    
    api_key = st.text_input("🔑 Gemini API Key", type="password", help="Enter your Gemini API Key from Google AI Studio.")
    
    st.markdown("---")
    st.subheader("💡 Modes")
    mode = st.radio("Select Analysis Depth:", ["Comprehensive Explanation", "Quick Solution & Formulas", "Interactive Quiz Mode"])
    
    st.markdown("---")
    st.markdown("### 🏆 Hackathon Metadata")
    st.caption("**Model Engine:** Gemma 4 / Gemini API")
    st.caption("**License:** MIT Open Source")
    st.caption("**Category:** Best Use of Gemma 4 & DigitalOcean AI")

# Main Dashboard Layout
col1, col2 = st.columns([1, 1.2], gap="medium")

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📷 1. Input Problem or Visual")
    
    uploaded_file = st.file_uploader("Upload Notebook Photo, Diagram, or Equation", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document/Image", use_container_width=True)

    user_query = st.text_area(
        "💬 Additional Prompt / Specific Question:",
        placeholder="e.g., Explain the physics behind this diagram or solve this calculus step by step.",
        height=120
    )
    
    submit_btn = st.button("🚀 Analyze & Solve with EduGemma")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("✨ 2. Intelligent Solution Output")
    
    if submit_btn:
        if not api_key:
            st.error("⚠️ Please enter your Gemini API Key in the sidebar!")
        elif uploaded_file is None and not user_query.strip():
            st.warning("⚠️ Please upload an image or type a question to analyze!")
        else:
            with st.spinner("🤖 EduGemma is processing visual tokens and generating step-by-step solution..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Custom Prompting based on Mode
                    prompt = f"""
                    You are EduGemma, an elite AI Science and Math Tutor built for students.
                    Selected Mode: {mode}
                    
                    Instructions:
                    1. Breakdown the visual/text query with extreme clarity using step-by-step explanations.
                    2. Use LaTeX formatting for all mathematical equations and formulas (e.g., $E = mc^2$).
                    3. Highlight Key Takeaways or Core Concepts clearly.
                    4. Provide 3 practice/quiz questions at the end to reinforce learning.
                    
                    Student Query: {user_query if user_query else 'Solve and explain this step by step.'}
                    """
                    
                    if uploaded_file is not None:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                        
                    st.success("✅ Analysis Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ Error processing request: {str(e)}")
    else:
        st.info("👈 Upload an image or type a query on the left, then click 'Analyze' to see the magic!")
        
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Built with ❤️ for Hacktoberfest 2026 & Gemma 4 Challenge | Open Source Agent Skill</p>", unsafe_allow_html=True)
