import os
import time
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="EduGemma AI — Cybernetic Multimodal Tutor Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS + Continuous Background Particle Animation Canvas
st.markdown("""
    <style>
    /* Dark Sci-Fi Theme */
    .stApp {
        background: #030712;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }

    /* Fixed Canvas Background for Continuous Animation */
    #bg-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.35;
        pointer-events: none;
    }

    /* Glowing Cyber Title */
    .glowing-header {
        font-size: 3.2rem !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        letter-spacing: -1px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .sub-tag {
        text-align: center;
        color: #38bdf8;
        font-family: monospace;
        font-size: 0.95rem;
        letter-spacing: 2px;
        margin-bottom: 2rem;
        text-transform: uppercase;
    }

    /* Sci-Fi Glass Cards */
    .cyber-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.1);
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .cyber-card:hover {
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 0 35px rgba(0, 242, 254, 0.25);
    }

    /* Animated Glowing Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #030712;
        font-weight: 800;
        border-radius: 14px;
        border: none;
        padding: 0.85rem 1.8rem;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.8);
        color: #000000;
    }

    /* Glowing Badge */
    .cyber-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        background: rgba(0, 242, 254, 0.1);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }
    </style>

    <!-- Canvas Particle Background Script -->
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
    const particleCount = 60;

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8,
            radius: Math.random() * 2 + 1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00f2fe';
        ctx.strokeStyle = 'rgba(0, 242, 254, 0.15)';

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
                if (dist < 120) {
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

# Header Section
st.markdown('<div style="text-align: center;"><span class="cyber-badge">🤖 GEMMA 4 AGENT SKILL | MULTIMODAL LABS</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="glowing-header">EduGemma Cyber-Tutor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-tag">// Autonomous Multimodal Reasoning & Pedagogical System</p>', unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ System Core")
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🎯 Learning Persona")
    tutor_mode = st.selectbox(
        "Select Tutor Personality:",
        ["Step-by-Step Patient Professor", "Fast Numerical Solver", "Interactive Quiz Master"]
    )
    
    st.markdown("---")
    st.markdown("### ⚡ Fast Preset Demos")
    preset = st.radio("Quick Test Problem:", ["None", "Calculus Integration", "Organic Chemistry Mechanism", "Physics Dynamics"])

# Preset Logic
sample_prompt = ""
if preset == "Calculus Integration":
    sample_prompt = "Solve the definite integral step by step with explanations: $\int_{0}^{\pi} \sin^2(x) dx$"
elif preset == "Organic Chemistry Mechanism":
    sample_prompt = "Explain the SN2 nucleophilic substitution mechanism with transition state energy diagram."
elif preset == "Physics Dynamics":
    sample_prompt = "A 5kg block rests on a 30-degree incline with friction coefficient 0.2. Calculate acceleration down the slope."

# Main Interface Grid
col_in, col_out = st.columns([1, 1.2], gap="large")

with col_in:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Visual & Text Input Matrix")
    
    uploaded_file = st.file_uploader("Upload Problem Picture (Homework, Notes, Diagram)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Target Document Visual Tokenized", use_container_width=True)

    input_text = st.text_area(
        "💬 Specific Query / Command:",
        value=sample_prompt if sample_prompt else "",
        placeholder="Upload image or type equation...",
        height=130
    )
    
    execute_btn = st.button("⚡ EXECUTE NEURAL REASONING")
    st.markdown('</div>', unsafe_allow_html=True)

with col2_out := col_out:
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.markdown("### 🧠 Autonomous Synthesis Output")
    
    if execute_btn:
        if not api_key:
            st.error("❌ API Key Missing! Enter Key in Left Sidebar Control Center.")
        elif not uploaded_file and not input_text.strip():
            st.warning("⚠️ Provide an input image or prompt query to initialize reasoning!")
        else:
            with st.spinner("🌀 Processing Multimodal Embedding Matrix & Gemma 4 Reasoning..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    full_prompt = f"""
                    System Instructions: You are EduGemma, a world-class AI science tutor.
                    Selected Personality: {tutor_mode}
                    
                    Task:
                    1. Solve the query/image with pristine clarity.
                    2. Use LaTeX formatting for mathematical expressions ($...$ or $$...$$).
                    3. Structure response into:
                       - 💡 **Core Scientific Principle**
                       - ✍️ **Step-by-Step Derivation/Solution**
                       - 🎯 **3 Interactive Practice Questions**
                    
                    User Query: {input_text if input_text else 'Solve and break down this problem.'}
                    """
                    
                    if uploaded_file:
                        response = model.generate_content([full_prompt, img])
                    else:
                        response = model.generate_content(full_prompt)
                    
                    # Store result in session state for downloading/TTS
                    st.session_state['solution'] = response.text
                    
                    st.success("✅ Neural Reasoning Matrix Complete!")
                    st.markdown(response.text)
                    
                    # Download Solution Feature
                    st.download_button(
                        label="💾 Download Solution Notes (.txt)",
                        data=response.text,
                        file_name="EduGemma_Solution_Notes.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Processing Error: {str(e)}")
    else:
        if 'solution' in st.session_state:
            st.markdown(st.session_state['solution'])
        else:
            st.info("👈 Upload problem image or select a Quick Preset on the left to initiate AI execution.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #4b5563; font-family: monospace;'>EduGemma v2.0 Open-Source Agent Skill | Built for Gemma 4 Hackathon & Hacktoberfest</p>", unsafe_allow_html=True)
