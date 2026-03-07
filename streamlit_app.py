import streamlit as st
import requests
import os
from fpdf import FPDF
import tempfile

st.set_page_config(page_title="Miss Writer", page_icon="🎙️", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Premium Pink Aesthetic
st.markdown("""
<style>
    /* Main Background & Text with Premium Pattern */
    .stApp {
        background-color: #ffe6f0;
        background-image: linear-gradient(90deg, rgba(255, 204, 221, 0.4) 1px, transparent 1px),
                          linear-gradient(rgba(255, 204, 221, 0.4) 1px, transparent 1px);
        background-size: 40px 40px;
        color: #1a0f14;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #ff66a3 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    
    /* Custom Title Styling (Now much larger) */
    .main-title {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff3385, #ff80b3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 5rem;
        font-weight: 900;
        margin-bottom: 5px;
        padding-bottom: 0px;
        line-height: 1.2;
        text-shadow: 2px 2px 10px rgba(255, 102, 163, 0.1);
    }
    
    /* Subtitle Styling (Now much larger) */
    .sub-title {
        text-align: center;
        color: #5c3547;
        font-size: 2.0rem;
        margin-bottom: 50px;
        font-style: italic;
        font-weight: 600;
    }

    /* Process Output Boxes */
    div.stAlert {
        background-color: #ffffff !important;
        border: 1px solid #ffb3d1 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(255, 102, 163, 0.08);
        padding: 20px !important;
    }
    
    /* Success specific box (Final Story) */
    div.st-emotion-cache-1j02j5g {
        background-color: #fff0f5 !important;
        border-left: 5px solid #ff3385 !important;
        color: #4a2b38 !important;
    }

    /* Info specific box (Transcript) */
    div.st-emotion-cache-12smh5i {
        background-color: #ffffff !important;
        border-left: 5px solid #ff99c2 !important;
        color: #4a2b38 !important;
    }
    
    /* Buttons */
    button[kind="primary"] {
        background-color: #ff4d94 !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(255, 77, 148, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #ff3385 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 51, 133, 0.5) !important;
    }
    
    /* Style the Audio widget and surrounding containers */
    audio {
        border-radius: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        background-color: white !important;
    }
    
    /* Target the text "Record your thoughts" and widget container specifically */
    div.stAudioInput > label > div > p {
        color: #ff3385 !important;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    /* White background behind the recorder UI container itself */
    div.stAudioInput {
        background-color: white !important;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffb3d1;
        box-shadow: 0 4px 15px rgba(255, 102, 163, 0.1);
        margin-bottom: 20px;
    }
    
    /* Top horizontal dividing line */
    hr {
        border-top: 2px dashed #ffccd9;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎙️ Miss Writer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Speak your thoughts naturally. The AI will interpret them and write a beautiful story.</p>", unsafe_allow_html=True)
st.divider()

# Sidebar for Controls and History
with st.sidebar:
    st.header("⚙️ Story Settings")
    selected_genre = st.selectbox(
        "Genre",
        ["Creative Narrative", "Journal Entry", "Fairy Tale", "Sci-Fi", "Mystery", "Romance"]
    )
    selected_tone = st.selectbox(
        "Tone",
        ["Engaging", "Professional", "Melancholy", "Humorous", "Inspirational", "Dark"]
    )
    
    st.divider()
    st.header("🔄 Story History")
    if st.button("Start New Story (Clear History)"):
        st.session_state.story_history = ""
        st.session_state.result = None
        st.rerun()

# Initialize session state for storing result & history
if "result" not in st.session_state:
    st.session_state.result = None
if "story_history" not in st.session_state:
    st.session_state.story_history = ""

# Audio recording widget
audio_value = st.audio_input("Record your thoughts")



# Get backend URL from env, default to localhost for development
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8082")

if audio_value is not None:
    # Adding a separate button to process, giving the user a chance to listen to their audio first
    if st.button("Generate Story", type="primary"):
        with st.spinner("Processing your thoughts... This may take a moment."):
            files = {"audio": ("recording.wav", audio_value, "audio/wav")}
            data = {
                "genre": selected_genre,
                "tone": selected_tone,
                "previous_story": st.session_state.story_history if st.session_state.story_history else ""
            }
            try:
                response = requests.post(f"{API_URL}/process-audio", files=files, data=data, timeout=60)
                
                if response.status_code == 200:
                    st.session_state.result = response.json()
                    st.session_state.story_history = st.session_state.result.get("story", "")
                    st.success("Story successfully generated!")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

# Display Results
if st.session_state.result:
    data = st.session_state.result
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📝 Your Transcript")
        st.info(data.get("transcript", "No transcript found."))
        
        st.subheader("🧠 Thought Interpretation")
        st.write("**Themes:**")
        st.caption(", ".join(data.get("themes", [])))
        
        st.write("**Emotions:**")
        st.caption(", ".join(data.get("emotions", [])))
        
        st.write("**Core Ideas:**")
        for idea in data.get("core_ideas", []):
            st.markdown(f"- {idea}")
            
    with col2:
        st.subheader("✨ Final Story ✨")
        st.markdown("**Human-in-the-loop Editing:** Feel free to correct any spelling or grammar mistakes below before saving.")
        edited_story = st.text_area(
            label="Story Content",
            value=data.get("story", "No story generated."),
            height=400,
            label_visibility="collapsed"
        )
        
        # Helper to generate PDF function
        def create_pdf(text):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Add Logo / Header
            pdf.set_font("Arial", "B", 24)
            pdf.cell(200, 10, txt="Miss Writer", ln=1, align="C")
            pdf.ln(10)
            
            pdf.set_font("Arial", "", 12)
            # FPDF multicell handles the line breaking
            # Deal with unicode characters by encoding to latin-1 and replacing unrepresentable characters.
            clean_text = text.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=clean_text)
            
            # Save to temporary file and read as bytes
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdf.output(tmp.name)
                with open(tmp.name, "rb") as f:
                    pdf_bytes = f.read()
            os.remove(tmp.name)
            return pdf_bytes
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.download_button(
                label="💾 Download as Text",
                data=edited_story,
                file_name="miss_writer_story.txt",
                mime="text/plain"
            )
        with col_btn2:
            st.download_button(
                label="📄 Download as PDF",
                data=create_pdf(edited_story),
                file_name="miss_writer_story.pdf",
                mime="application/pdf"
            )
