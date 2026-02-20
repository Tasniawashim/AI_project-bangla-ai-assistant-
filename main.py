import streamlit as st
import os
from gtts import gTTS        
from io import BytesIO        

# --- IMPORTS ---
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Import data
from dataset import get_data 

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="Bangla AI Assistant", 
    page_icon="🇧🇩", 
    layout="centered"  # 'wide' এর বদলে 'centered' দিলে চ্যাট দেখতে সুবিধা হয়
)

# --- SAFE CSS (শুধু হেডারের জন্য, চ্যাটে প্রভাব ফেলবে না) ---
st.markdown("""
<style>
    /* মেইন টাইটেল স্টাইল */
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: #FF4B4B; /* Streamlit Red */
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2em;
        color: gray;
        margin-bottom: 20px;
    }
    /* টপিক ব্যাজ */
    .topic-badge {
        background-color: #262730;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        border: 1px solid #FF4B4B;
        display: inline-block;
        margin-bottom: 8px;
    }
    /* লাইট মোড ফিক্স */
    @media (prefers-color-scheme: light) {
        .topic-badge {
            background-color: #f0f2f6;
            color: black;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- API SETUP ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY missing! Add to `.env` file.")
    st.stop()

@st.cache_resource
def initialize_chatbot():
    docs = get_data()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(docs, embeddings)
    
    llm = ChatGroq(
        groq_api_key=api_key, 
        model_name="llama-3.1-8b-instant", 
        temperature=0
    )
    return vectorstore, llm

try:
    vectorstore, llm = initialize_chatbot()
except Exception as e:
    st.error(f"❌ Setup Error: {e}")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.header("সহায়িকা মেনু 🇧🇩")
    st.markdown("---")
    st.write("📌 **নমুনা প্রশ্ন (Copy-Paste):**")
    st.code("এইচএসসি পরীক্ষা কবে?")
    st.code("ডেঙ্গু লক্ষণ কী?")
    st.code("মেসি কোন দেশের?")
    st.code("RAM এর কাজ কী?")
    st.code("সাজেক কোথায়?")
    
    st.markdown("---")
    if st.button("🗑️ চ্যাট ক্লিয়ার করুন"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN HEADER ---
st.markdown('<div class="main-title">বাংলা এআই 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">আপনার ব্যক্তিগত ভার্চুয়াল অ্যাসিস্ট্যান্ট</div>', unsafe_allow_html=True)

# --- TOPIC LOGIC ---
def detect_topic(query, llm):
    q_lower = query.lower()
    keywords = {
        'shiksha': ['এইচএসসি', 'hsc', 'exam', 'পড়া', 'কলেজ', 'pass', 'gpa'],
        'shastho': ['ডেঙ্গু', 'জ্বর', 'health', 'চিকিৎসা', 'রোগ', 'ঔষধ', 'hospital'],
        'kheladhula': ['মেসি', 'ফুটবল', 'sports', 'খেলা', 'ক্রিকেট', 'goal'],
        'projukti': ['ram', 'র‍্যাম', 'ai', 'python', 'কম্পিউটার', 'mouse', 'keyboard'],
        'vromon': ['সাজেক', 'ভ্রমণ', 'tour', 'ভিসা', 'hotel', 'cox']
    }
    for topic, words in keywords.items():
        if any(word in q_lower for word in words):
            return topic
    
    try:
        response = llm.invoke(f"Classify: shiksha/shastho/kheladhula/projukti/vromon\nQuery: {query}\nReturn ONLY topic:")
        ai_topic = response.content.strip().lower()
        mapping = {"education": "shiksha", "health": "shastho", "sports": "kheladhula", "tech": "projukti", "travel": "vromon"}
        return mapping.get(ai_topic, "unknown")
    except:
        return "unknown"

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='bn')
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        return audio_fp
    except:
        return None

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "আসসালামু আলাইকুম! আপনি কী জানতে চান?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # এখানে কোনো কাস্টম CSS ব্যবহার করা হয়নি, তাই সব সময় পরিষ্কার দেখা যাবে
        if "badge" in message:
             st.markdown(message["badge"], unsafe_allow_html=True)
        st.markdown(message["content"])

# --- USER INPUT & RESPONSE ---
if query := st.chat_input("এখানে প্রশ্ন লিখুন..."):
    
    # 1. User Message Display
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # 2. Assistant Logic
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("ভাবছি..."):
            topic = detect_topic(query, llm)
            display_map = {
                "shiksha": "📚 শিক্ষা", "shastho": "🏥 স্বাস্থ্য", 
                "kheladhula": "⚽ খেলাধুলা", "projukti": "💻 প্রযুক্তি", 
                "vromon": "✈️ ভ্রমণ", "unknown": "❓ সাধারণ"
            }
            topic_name = display_map.get(topic, "❓")
            badge_html = f'<span class="topic-badge">{topic_name}</span>'
            
            voice_text = ""
            final_response = ""

            if topic == "unknown":
                final_response = "দুঃখিত, এই বিষয়টি আমার ডাটাবেজে নেই। দয়া করে শিক্ষা, স্বাস্থ্য, খেলাধুলা, প্রযুক্তি বা ভ্রমণ নিয়ে প্রশ্ন করুন।"
                voice_text = final_response
            else:
                try:
                    retriever = vectorstore.as_retriever(
                        search_kwargs={"filter": {"topic": topic}, "k": 3}
                    )
                    template = """Answer in Bangla based on Context.
                    Context: {context}
                    Question: {question}
                    If no context, say 'তথ্যটি জানা নেই'."""
                    
                    prompt = ChatPromptTemplate.from_template(template)
                    chain = (
                        {"context": retriever, "question": RunnablePassthrough()}
                        | prompt
                        | llm
                        | StrOutputParser()
                    )
                    
                    answer = chain.invoke(query)
                    final_response = answer
                    voice_text = answer
                except Exception as e:
                    final_response = "সমস্যা হয়েছে, আবার চেষ্টা করুন।"
                    st.error(f"Error: {e}")

            # 3. Final Display (Clean Text)
            st.markdown(badge_html, unsafe_allow_html=True) # Badge separate line
            st.markdown(final_response) # Text separate line
            
            # 4. Voice
            if voice_text:
                audio = text_to_speech(voice_text)
                if audio:
                    st.audio(audio, format="audio/mp3")

            # 5. Save to History
            st.session_state.messages.append({
                "role": "assistant", 
                "content": final_response,
                "badge": badge_html
            })