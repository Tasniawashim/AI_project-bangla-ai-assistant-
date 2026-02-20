# 🤖 AmarBot: Voice-Enabled Bangla RAG Assistant

**AmarBot** is an intelligent AI Chatbot built on the **Retrieval-Augmented Generation (RAG)** architecture. It is designed to provide highly accurate, hallucination-free answers in Bengali by fetching information from a curated local dataset. Additionally, it features an integrated **Voice Output (TTS)** system to read responses aloud.

---

## ✨ Key Features

* **🎯 Context-Aware RAG:** Answers are grounded strictly in the `dataset.py` knowledge base to ensure reliability.
* **🔊 Bengali Voice Synthesis:** Real-time audio generation using **gTTS** (Google Text-to-Speech).
* **⚡ Ultra-Low Latency:** Inference is powered by **Llama-3.1-8b** via the **Groq LPU** for near-instant responses.
* **🧠 Intelligent Topic Detection:** Automatically classifies queries into Education, Health, Sports, Tech, and Travel.
* **🎨 Interactive UI:** A clean, modern Streamlit dashboard with built-in demo questions.

---

## 🛠 Tech Stack

| Component | Technology |
| --- | --- |
| **Language Model** | Llama-3.1-8b-instant (via Groq) |
| **Vector Store** | ChromaDB |
| **Embeddings** | HuggingFace (`all-MiniLM-L6-v2`) |
| **Frontend** | Streamlit |
| **Speech Engine** | gTTS (Google Text-to-Speech) |

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Bangla_Chatbot.git
cd Bangla_Chatbot

```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Configure API Keys

Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_actual_api_key_here

```

### 5. Run the Application

```bash
streamlit run app.py

```

---

## 📂 Project Structure

```text
Bangla_Chatbot/
├── app.py           # Core application logic & Streamlit UI
├── dataset.py       # Knowledge base (Source of truth)
├── requirements.txt # Project dependencies
├── .env             # Environment variables (API Keys)
└── README.md        # Project documentation

```

---

## 🔍 How it Works

1. **Ingestion:** The chatbot reads text from `dataset.py` and converts it into mathematical vectors using HuggingFace embeddings.
2. **Retrieval:** When you ask a question, ChromaDB finds the most relevant piece of information.
3. **Generation:** Llama 3.1 synthesizes the retrieved data into a natural-sounding Bengali response.
4. **Speech:** The text response is converted to an MP3 file and played automatically.

---

## ⚠️ Troubleshooting

* **API Key Error:** Ensure your `.env` file is named correctly and the key is valid.
* **No Audio:** An active internet connection is required for **gTTS** to generate the voice files.
* **Package Errors:** If `streamlit` is not recognized, ensure your virtual environment is activated before running the app.

---

## 📜 License

This project is licensed under the MIT License.

