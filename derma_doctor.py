import streamlit as st
import google.generativeai as genai
from pathlib import Path
from api_key import api_key
import requests
from streamlit_lottie import st_lottie
import base64
 
# --- Animated Medical Background ---
# Lottie animation for medical/doctor background (transparent)
# You can use another Lottie URL if you prefer
medical_bg_lottie_url = "https://lottie.host/3d1e3a8b-1e0f-4f8a-8b7c-5c6b7c7e4e7a/3wJQ8Vw7mK.json"  # Replace with a suitable Lottie animation
 
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
 
medical_bg_lottie = load_lottieurl(medical_bg_lottie_url)
 
# Inject custom CSS for background container and futuristic glassmorphism
st.markdown(
    """
    <style>
    /* Remove Streamlit default header and toolbar */
    header, .st-emotion-cache-1avcm0n, .st-emotion-cache-18ni7ap, .st-emotion-cache-6qob1r {display:none !important;}
    /* Remove extra padding at the top */
    .block-container {padding-top: 0 !important;}
 
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Montserrat:wght@400;700&family=Roboto:wght@400;700&display=swap');
    html, body, [class*='css']  {
        font-family: 'Montserrat', 'Roboto', 'Orbitron', Arial, sans-serif !important;
        background: transparent !important;
    }
    .lottie-bg-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.18;
        filter: blur(0.5px);
    }
    .main > div {
        position: relative;
        z-index: 1;
    }
    /* Glassmorphism card */
    .glass-card {
        background: rgba(30, 40, 60, 0.55);
        border-radius: 22px;
        box-shadow: 0 8px 40px 0 rgba(0,255,255,0.10), 0 2px 8px 0 rgba(0,0,0,0.18);
        backdrop-filter: blur(14px) saturate(140%);
        border: 2px solid rgba(0,255,255,0.25);
        margin: 0 0 18px 0;
        padding: 28px 32px 24px 32px;
    }
    /* Neon title */
    .futuristic-title {
        font-family: 'Orbitron', 'Montserrat', Arial, sans-serif;
        font-size: 2.8rem;
        color: #00fff7;
        text-shadow: 0 0 8px #00fff7, 0 0 32px #00fff780;
        letter-spacing: 2px;
        margin-bottom: 8px;
    }
    /* Neon button */
    .stButton > button {
        background: linear-gradient(90deg, #0fffc1 0%, #00cfff 100%);
        color: #1e283c;
        border-radius: 18px;
        border: none;
        box-shadow: 0 0 16px #00fff7b0;
        font-weight: 700;
        font-size: 1.12rem;
        transition: box-shadow 0.2s;
    }
    .stButton > button:hover {
        box-shadow: 0 0 24px #00fff7, 0 0 64px #00fff7a0;
        background: linear-gradient(90deg, #00cfff 0%, #0fffc1 100%);
    }
    /* Chat input neon border */
    .stTextInput > div > div > input {
        border-radius: 16px !important;
        border: 2px solid #00fff7 !important;
        box-shadow: 0 0 12px #00fff7a0 !important;
        background: rgba(30,40,60,0.75) !important;
        color: #fff !important;
    }
    /* Chat panel glassmorphism */
    .chat-glass {
        background: #fafdffcc;
 
        border-radius: 22px;
        box-shadow: 0 4px 24px 0 #00fff7a0, 0 2px 8px 0 rgba(0,0,0,0.18);
        backdrop-filter: blur(14px) saturate(130%);
        border: 2px solid rgba(0,255,255,0.18);
        padding: 18px 20px 10px 20px;
        margin-bottom: 20px;
    }
    /* Neon glow for images */
    .neon-img {
        box-shadow: 0 0 32px 0 #00fff7a0, 0 0 8px #00fff7c0;
        border-radius: 18px;
        border: 2px solid #00fff7a0;
    }
    /* General neon shadow */
    .main {
        box-shadow: 0 0 120px 0 #00fff7a0 inset;
    }
    </style>
    <div class="lottie-bg-container" id="lottie-bg"></div>
    """,
    unsafe_allow_html=True
)
 
# Render the Lottie animation in the background using streamlit.components.v1.html
import streamlit.components.v1 as components
components.html(
    f"""
    <script src='https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js'></script>
    <lottie-player src='{medical_bg_lottie_url}' background="transparent" speed="1" style="width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; z-index: 0; pointer-events: none; opacity:0.18;" loop autoplay></lottie-player>
    """,
    height=0,
    width=0,
)
 
 
# Lottie animation URL for animated doctor (public domain or free asset)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
 
# Small cartoon doctor image (base64 for chat bubble)
doctor_avatar_url = "https://cdn.pixabay.com/photo/2017/01/31/13/14/avatar-2026510_1280.png"  # Replace with any suitable PNG
 
# Lottie doctor animation (replace with a suitable Lottie JSON URL)
lottie_doctor = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json")
 
# Gemini model configuration
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)
 
system_prompt = """
You are a medically-informed AI Dermatology Assistant. Your role is to analyze high-resolution images of human skin to identify potential dermatological conditions. You provide structured, clinically relevant insights to assist in early detection and guidance, but you are not a substitute for a licensed medical professional.
give response in bengali language
Core Responsibilities:
1. Detailed Analysis:
- Thoroughly examine each image of human skin.
- Focus on identifying any abnormal findings such as:
  - Lesions, rashes, or discoloration
  - Moles, nevi, or growths
  - Scaling, crusting, or ulceration
  - Inflammation, swelling, or infection
  - Signs of malignancy or chronic skin conditions
2. Findings Report:
- Document all observed anomalies or signs of disease.
- Clearly articulate:
  - Location (if identifiable)
  - Size, shape, color, and texture
  - Pattern, distribution, and symmetry
- Use appropriate dermatological terminology
3. Recommendations and Next Steps:
- Based on your analysis, suggest:
  - Whether the condition appears benign, suspicious, or urgent
  - Whether further evaluation, biopsy, or specialist referral is needed
  - Any monitoring or hygiene practices that may help
4. Treatment Suggestions (if appropriate):
- For common, non-urgent conditions (e.g., acne, eczema, fungal infections), recommend:
  - Over-the-counter treatments
  - Lifestyle or hygiene modifications
  - When to escalate to professional care
Important Notes:
- Scope of Response: Only respond if the image pertains to human dermatological health.
- Clarity of Image: If the image quality impedes clear analysis, note that certain features cannot be reliably assessed and recommend re-uploading a clearer image.
- Medical Disclaimer: Always include the following disclaimer at the end of your response:
  \"Consult with a Doctor before making any medical decisions. This analysis is not a substitute for professional medical advice, diagnosis, or treatment.\"
Output Format Example:
🧪 Analysis Summary:
> Brief summary of the observed condition.
🔍 Findings Report:
- Detailed description of the skin anomaly using clinical terms.
📋 Recommendations and Next Steps:
- Guidance on urgency, next steps, and whether to consult a specialist.
💊 Treatment Suggestions:
- If applicable, suggest basic treatment or care options.
⚠️ Disclaimer:
> \"Consult with a Doctor before making any medical decisions. This analysis is not a substitute for professional medical advice, diagnosis, or treatment.\"
"""
 
st.set_page_config(page_title="Derma Doctor", page_icon=":robot:", layout="wide")
 
# Make sure Lottie player script is loaded at the very top
st.markdown("""
    <script src='https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js'></script>
""", unsafe_allow_html=True)
 
# Layout: Left (doctor) = 0.8, Center (main) = 2.4, Right (chatbot) = 1.8
col1, col2, col3 = st.columns([0.8, 2.4, 1.8])
 
# --- Futuristic Neon CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Montserrat:wght@400;700&family=Roboto:wght@400;700&display=swap');
    html, body, [class*='css']  {
        font-family: 'Montserrat', 'Roboto', 'Orbitron', Arial, sans-serif !important;
        background: linear-gradient(120deg, #e0f7fa 0%, #fafdff 100%) !important;
    }
    /* Neon-glow border animation */
    @keyframes borderGlow {
      0% { box-shadow: 0 0 10px 2px #00fff7, 0 0 40px 8px #8fd3ff80; }
      50% { box-shadow: 0 0 24px 6px #7cfcff, 0 0 64px 16px #b388ff80; }
      100% { box-shadow: 0 0 10px 2px #00fff7, 0 0 40px 8px #8fd3ff80; }
    }
    /* Neon-glass cards */
    .glass-card, .chat-glass {
        background: linear-gradient(120deg, #fafdffcc 60%, #e0f7faee 100%);
        border-radius: 24px;
        border: 2.5px solid #00fff7a0;
        animation: borderGlow 2.8s infinite;
        backdrop-filter: blur(16px) saturate(144%);
        margin: 0 0 22px 0;
        padding: 28px 32px 24px 32px;
    }
    .glass-card {
        box-shadow: 0 8px 40px 0 #00fff7a0, 0 2px 8px 0 #b388ff40;
    }
    .chat-glass {
        box-shadow: 0 4px 24px 0 #b388ff80, 0 2px 8px 0 #00fff7a0;
    }
    /* Neon-glow for doctor Lottie */
    .doctor-neon {
        box-shadow: 0 0 32px 0 #00fff7a0, 0 0 24px #b388ff80, 0 0 8px #7cfcffb0;
        border-radius: 32px;
        background: rgba(240,255,255,0.08);
        padding: 8px;
        margin-top: 10px;
    }
    /* Neon vertical bar background */
    .neon-bar {
        position: absolute;
        left: 50%;
        top: 0;
        transform: translateX(-50%);
        width: 16px;
        height: 100vh;
        background: linear-gradient(180deg, #00fff7 0%, #b388ff 100%);
        opacity: 0.18;
        border-radius: 12px;
        z-index: 0;
        filter: blur(2.5px);
    }
    .doctor-label {
        color: #0a2cff;
        font-family: Orbitron,Montserrat,sans-serif;
        font-size: 1.12rem;
        margin-top: 10px;
        text-shadow: 0 0 8px #b7d0ff, 0 0 16px #00fff7a0;
        letter-spacing: 1.5px;
    }
    </style>
""", unsafe_allow_html=True)
 
 
# Main content and chat fade-in animation CSS (fix for SyntaxError)
st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: none; }
    }
    .glass-card, .chat-glass {
        animation: fadeInUp 1.1s cubic-bezier(.23,1.07,.32,1) 0s both;
    }
    .ai-bubble-anim {
        animation: fadeInUp 0.85s cubic-bezier(.23,1.07,.32,1) 0s both;
    }
    .futuristic-title {
        font-family: 'Orbitron', 'Montserrat', Arial, sans-serif;
        font-size: 2.8rem;
        color: #0a2cff;
        text-shadow: 0 0 12px #0a2cff, 0 0 32px #0a2cff80;
        letter-spacing: 2px;
        margin-bottom: 8px;
        margin-top: 0px;
        animation: fadeInUp 1s cubic-bezier(.23,1.07,.32,1) 0s both;
    }
    .chat-glass h3 {
        color: #0a2cff !important;
        text-shadow: 0 0 12px #0a2cff, 0 0 32px #0a2cff80;
        font-family: 'Orbitron', 'Montserrat', Arial, sans-serif;
        font-size: 1.6rem;
        margin-top: 0px;
        margin-bottom: 12px;
        animation: fadeInUp 1s cubic-bezier(.23,1.07,.32,1) 0s both;
    }
    </style>
""", unsafe_allow_html=True)
 
 
 
# ---- Modern Wide Header ----
st.markdown("""
    <div style='width:100%;max-width:900px;margin:0 auto 1.5rem auto;padding:2.5rem 1rem 1rem 1rem;background:linear-gradient(90deg,#e3f6fc 0%,#fafdff 100%);border-radius:32px;box-shadow:0 4px 32px #00fff733;text-align:center;'>
        <h1 style='font-family:Orbitron,Montserrat,sans-serif;font-size:2.8rem;letter-spacing:2px;color:#0a2cff;margin-bottom:0.5rem;'>Derma Doctor AI</h1>
        <div style='font-size:1.25rem;color:#1a1c2c;font-family:Montserrat,Roboto,sans-serif;'>Instant AI-powered skin analysis. Upload or capture a photo to begin.</div>
    </div>
""", unsafe_allow_html=True)
 
# --- Main Two-Column Layout ---
main_col, chat_col = st.columns([2, 1], gap="large")
 
with main_col:
    st.markdown("""
        <div style='width:100%;max-width:600px;margin:0 auto 2rem auto;padding:2rem 1.5rem 1.5rem 1.5rem;background:#fff;border-radius:22px;box-shadow:0 4px 24px #0a2cff22;'>
            <h2 style='font-family:Montserrat,sans-serif;font-size:1.6rem;color:#0a2cff;margin-bottom:1.2rem;'>AI Skin Analyzer</h2>
            <div style='margin-bottom:1.4rem;'>
                <b>Upload</b> or <b>Capture</b> a clear photo of your skin area for instant AI analysis.
            </div>
    """, unsafe_allow_html=True)
 
    col_upload, col_capture = st.columns(2)
    with col_upload:
        st.markdown("<div style='padding:0.5rem 0;font-size:1.1rem;color:#888;'>Upload Image</div>", unsafe_allow_html=True)
        st.markdown("<div style='border:2px dashed #0a2cff33;border-radius:12px;padding:0.7rem 0.5rem;background:#fafdff;'>🖼️<div style='font-size:0.95rem;color:#888;'>Drag & drop or click to upload</div></div>", unsafe_allow_html=True)
        upload_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key="main_upload")
    with col_capture:
        st.markdown("<div style='padding:0.5rem 0;font-size:1.1rem;color:#888;'>Capture Photo</div>", unsafe_allow_html=True)
        st.markdown("<div style='border:2px dashed #0a2cff33;border-radius:12px;padding:0.7rem 0.5rem;background:#fafdff;'>📷<div style='font-size:0.95rem;color:#888;'>Use your device camera</div></div>", unsafe_allow_html=True)
        capture_image = st.camera_input("", key="main_capture")
 
    image_data = None
    image_source = None
    if upload_file is not None:
        image_data = upload_file.getvalue()
        image_source = "upload"
    elif capture_image is not None:
        image_data = capture_image.getvalue()
        image_source = "capture"
 
    if image_data is not None:
        st.markdown("<div style='margin:1rem 0;text-align:center;'>", unsafe_allow_html=True)
        st.image(image_data, width=340, caption="Preview", use_container_width=False, clamp=False, channels="RGB")
        st.markdown("</div>", unsafe_allow_html=True)
 
    analyze_btn = st.button("Analyze", key="analyze_btn", use_container_width=True)
    if analyze_btn:
        if image_data is not None:
            image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
            promt_parts = [image_parts[0], system_prompt]
            st.session_state["last_uploaded_image"] = image_data
            progress_bar = st.progress(0, text="Analyzing image...")
            import time
            for percent in range(1, 91, 10):
                time.sleep(0.05)
                progress_bar.progress(percent, text=f"Analyzing image... {percent}%")
            response = model.generate_content(promt_parts)
            progress_bar.progress(100, text="Analysis complete!")
            time.sleep(0.2)
            progress_bar.empty()
            st.markdown(f"""
                <div style='margin:1.5rem auto 0 auto;max-width:520px;background:#fafdff;border-radius:18px;box-shadow:0 2px 12px #0a2cff22;padding:1.5rem 1.2rem 1.2rem 1.2rem;'>
                    <div style='display:flex;align-items:center;margin-bottom:0.6rem;'>
                        <span style='font-size:2rem;margin-right:0.6rem;'>🩺</span>
                        <span style='font-size:1.15rem;font-weight:600;color:#0a2cff;'>AI Analysis Result</span>
                    </div>
                    <div style='font-size:1.08rem;color:#222;line-height:1.6;'>{response.text.replace('</div>', '').replace('</DIV>', '')}</div>
                </div>
            """, unsafe_allow_html=True)
            st.session_state["last_diagnosis"] = response.text
        else:
            st.warning("Please upload or capture an image before analyzing.")
    st.markdown("</div>", unsafe_allow_html=True)
 
 
with chat_col:
    # --- Modern Chatbot Panel ---
    st.markdown("""
        <div style='width:100%;max-width:520px;margin:2.5rem auto 0 auto;background:#fff;border-radius:22px;box-shadow:0 4px 24px #0a2cff22;padding:1.5rem 1.5rem 1rem 1.5rem;'>
            <h3 style='text-align:center;font-family:Montserrat,sans-serif;font-size:1.3rem;color:#0a2cff;margin-bottom:1.2rem;'>Ask Dr. AI</h3>
            <div style='max-height:260px;overflow-y:auto;margin-bottom:1rem;'>
    """, unsafe_allow_html=True)
 
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
 
    # Display chat bubbles
    for q, a in st.session_state["chat_history"]:
        st.markdown(f"""
            <div style='display:flex;justify-content:flex-end;margin-bottom:0.3rem;'>
                <div style='background:#e3f6fc;color:#0a2cff;padding:0.6rem 1rem;border-radius:18px 18px 4px 18px;max-width:70%;font-size:1.05rem;box-shadow:0 2px 8px #0a2cff11;'>
                    <b>You:</b> {q}
                </div>
            </div>
            <div style='display:flex;justify-content:flex-start;margin-bottom:0.7rem;'>
                <div style='background:#fafdff;color:#222;padding:0.7rem 1.1rem 0.7rem 0.9rem;border-radius:18px 18px 18px 4px;max-width:80%;font-size:1.06rem;box-shadow:0 2px 8px #00fff711;'>
                    <span style='font-size:1.3rem;vertical-align:middle;margin-right:8px;'>🩺</span> <b style='color:#0a2cff;'>Dr. AI:</b> {a.replace('</div>', '').replace('</DIV>', '')}
                </div>
            </div>
        """, unsafe_allow_html=True)
 
    st.markdown("</div>", unsafe_allow_html=True)
 
    # --- Chat Input ---
    # --- Chat Input ---
    user_input = st.text_input("Ask a question about your skin or the diagnosis above:", key="chat_input")
    send_clicked = st.button("Send", key="send_btn", use_container_width=True)
    if send_clicked and user_input:
        chat_prompt = """You are Dr. AI, a friendly cartoon dermatologist. Answer user questions about dermatology or their diagnosis. If a diagnosis is available, use it as context. Always be concise, medically responsible, and supportive. Add a doctor cartoon emoji at the start of each response."""
        if "last_diagnosis" in st.session_state:
            chat_prompt += f"\n\nDiagnosis Context: {st.session_state['last_diagnosis']}"
        chat_prompt += f"\n\nUser: {user_input}"
        chat_response = model.generate_content([chat_prompt])
        st.session_state["chat_history"].append((user_input, chat_response.text))
 
    # --- End of Chatbot Card ---
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)

 
