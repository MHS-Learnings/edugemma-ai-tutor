import os
import time
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="EduGemma AI — Holographic Autonomous Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS + Continuous Background Particle Animation + Cyber Intro Screen
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');

    /* Global Dark Sci-Fi Theme */
    .stApp {
        background: #020617;
        color: #f8fafc;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Fixed Fullscreen Background Particle Canvas */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.45;
        pointer-events: none;
    }

    /* Intro Screen Overlay Styling */
    #intro-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #020617;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeOut 0.8s ease-in-out 3.2s forwards;
        pointer-events: none;
    }

    /* Cyber Core Arc Reactor Spinner */
    .cyber-core {
        width: 120px;
        height: 120px;
        border: 4px solid transparent;
        border-top: 4px solid #00f2fe;
        border-right: 4px solid #4facfe;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.6);
        margin-bottom: 20px;
    }

    .intro-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f2fe, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-transform: uppercase;
    }

    .intro-sub {
        color: #38bdf8;
        font-family: monospace;
        letter-spacing: 2px;
        margin-top: 10px;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes fadeOut {
        0% { opacity: 1; visibility: visible; }
        100% { opacity: 0; visibility: hidden; }
    }

    /* Glowing Main Title */
    .glowing-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 3.5rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #38bdf8, #c084fc, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        letter-spacing: -1px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Cyber Glassmorphism Card Container */
    .cyber-card {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 254, 0.25);
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.15);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .cyber-card:hover {
        border-color: rgba(0, 242, 254, 0.6);
        box-shadow: 0 0 45px rgba(0, 242, 254, 0.35);
    }

    /* Glowing Animated Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00f2fe 0%, #3b82f6 100%);
        color: #020617;
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        border-radius: 14px;
        border: none;
        padding: 0.95rem 1.8rem;
        font-size: 1.15rem;
        letter-spacing: 1px;
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.5);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 40px rgba(0, 242, 254, 0.9);
        color: #000000;
    }

    /* Status Badge */
    .cyber-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        background: rgba(0, 242, 254, 0.12);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.4);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        margin-bottom: 12px;
    }
    </style>

    <!-- Holographic Intro Sequence Screen -->
    <div id="intro-overlay">
        <div class="cyber-core"></div>
        <div class="intro-title">EduGemma AI</div>
        <div class="intro-sub">[ INITIALIZING NEURAL CORE & GEMMA 4 ENGINE... ]</div>
    </div>

    <!-- Background Particle Canvas Engine Script -->
    <canvas id="bg-canvas"></canvas>
    <script>
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    const particles = [];
    const particleCount = 75;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.9,
            vy: (Math.random() - 0.5) * 0.9,
            radius: Math.random() * 2.5 + 1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00f2fe';
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.18)';

        for (let i = 0; i < particleCount; i++) {
            let p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();

            for (let j = i + 1; j < particleCount; j++) {
                let p2 = particles[j];
                let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
    </script>
""", unsafe_allow_html=True)

# Main UI Header
st.markdown('<div style="text-align: center;"><span class="cyber-badge">⚡ AUTONOMOUS MULTIMODAL AGENT SKILL</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="glowing-header">EDUGEMMA CYBER TUTOR</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #38bdf8; font-family: monospace; letter-spacing: 3px;">// GEMMA 4 MULTIMODAL REASONING MATRIX</p>', unsafe_allow_html=True)

# Sidebar Control Center
with st.sidebar:
    st.markdown("### ⚙️ SYSTEM CONFIG")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🎯 AGENT PERSONA")
    tutor_mode = st.radio(
        "Select Learning Mode:",
        ["🔬 Step-by-Step Concept Breakdown", "⚡ Instant Solution & Formulas", "🎯 Interactive Quiz Generator"]
    )
    
    st.markdown("---")
    st.markdown("### 🚀 DEMO PRESETS")
    preset = st.radio("Quick Load Test Problem:", ["None", "Calculus Integral", "Organic Reaction", "Physics Vector Dynamics"])

# Preset Logic
sample_prompt = ""
if preset == "Calculus Integral":
    sample_prompt = "Solve the definite integral step by step with clear explanations: $\int_{0}^{\pi} \sin^2(x) dx$"
elif preset == "Organic Reaction":
    sample_prompt = "Explain the SN2 nucleophilic substitution reaction mechanism with energy transition curve."
elif preset == "Physics Vector Dynamics":
    sample_prompt = "A 10kg block slides down a 30-degree inclined plane with kinetic friction coefficient 0.15. Calculate net acceleration."

# Main Interface Grid
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("### 📥 VISUAL TOKEN INPUT")
    
    uploaded_file = st.file_uploader("Upload Image (Diagram, Equation, Handwritten Notes)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Tokenized Input Image", use_container_width=True)

    input_text = st.text_area(
        "💬 Specific Prompt / Command:",
        value=sample_prompt if sample_prompt else "",
        placeholder="Type math formula or question...",
        height=130
    )
    
    execute_btn = st.button("🚀 INITIALIZE NEURAL REASONING")
    st.markdown('</div>', unsafe_allow_html=True)

with col_out:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI SYNTHESIS OUTPUT")
    
    if execute_btn:
        if not api_key:
            st.error("❌ API Key Required! Enter Key in Left Control Center.")
        elif not uploaded_file and not input_text.strip():
            st.warning("⚠️ Upload an image or select a Quick Demo Preset on the left!")
        else:
            with st.spinner("🌀 Processing Neural Matrix & Gemma 4 Multimodal Embeddings..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    full_prompt = f"""
                    System Prompt: You are EduGemma, an advanced Cybernetic Science & Math AI Tutor.
                    Selected Mode: {tutor_mode}
                    
                    Instructions:
                    1. Solve with pristine step-by-step clarity.
                    2. Use LaTeX formatting ($...$ or $$...$$) for equations.
                    3. Format response into:
                       - 💡 **Core Scientific Principle**
                       - ✍️ **Complete Step-by-Step Derivation**
                       - 🎯 **3 Follow-up Quiz Questions for Practice**
                    
                    User Query: {input_text if input_text else 'Analyze and explain this step by step.'}
                    """
                    
                    if uploaded_file:
                        response = model.generate_content([full_prompt, img])
                    else:
                        response = model.generate_content(full_prompt)
                    
                    st.session_state['solution'] = response.text
                    
                    st.success("✅ Neural Reasoning Complete!")
                    st.markdown(response.text)
                    
                    # Download Solution Feature
                    st.download_button(
                        label="💾 Download Cyber Notes (.txt)",
                        data=response.text,
                        file_name="EduGemma_Cyber_Notes.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Execution Error: {str(e)}")
    else:
        if 'solution' in st.session_state:
            st.markdown(st.session_state['solution'])
        else:
            st.info("👈 Upload an image or select a Quick Demo Preset on the left, then click Execute.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #475569; font-family: monospace;'>EduGemma Cybernetic Agent v3.0 | Built for Gemma 4 Challenge & Open-Source Agent Skill</p>", unsafe_allow_html=True)
