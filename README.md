# Job Data Conversational Chatbot
A conversational bot built using LangChain and LLM using a jobs dataset that I extracted from careers pages.

This project is a **Retrieval-Augmented Generation (RAG)** based chatbot that helps job seekers explore and query job listings in a conversational manner. It loads job data from CSVs, creates semantic embeddings, and uses a local Llama 2 model to provide accurate, context-based answers.

The chatbot runs locally, ensuring **privacy** and **offline capability**.

## Project Overview
**Problem:** Job seekers need quick, accurate, searchable access to large datasets of job postings.  
**Solution:** A RAG pipeline that performs semantic search over job data and generates factual answers constrained to your dataset.  
**Why Local:** Offline usage, low cost, enhanced data privacy.

## 🚀 Features
- **Load and validate CSVs** with schema: `title`, `company`, `job_description`, `key_skills`
- **Semantic search** via **FAISS** for fast retrieval
- **Embeddings** from HuggingFace `all-MiniLM-L6-v2`
- **Local language model inference** with LLaMA 2 (via **LlamaCpp**)
- **Conversational memory** for multi‑turn Q&A
- **Custom prompt** to ensure factual, dataset‑grounded responses
- **Streamlit UI** with styled chat bubbles

## 📂 Data Requirement
> **Note:** This repository does **not** include job CSV data.  
> You must add your own CSV files into the `data/` directory before running the chatbot.  
> Each CSV **must** have the following columns:

| Column           | Type   | Description |
|------------------|--------|-------------|
| `title`          | string | Job title/role |
| `company`        | string | Company name |
| `job_description`| text   | Full job description |
| `key_skills`     | text   | Comma/pipe‑separated skills |

**Example CSV:**
title,company,job_description,key_skills
Data Scientist,ABC Corp,"Analyze large datasets and build ML models","Python,SQL,Machine Learning"
Backend Engineer,XYZ Ltd,"Develop backend APIs and maintain databases","Django,PostgreSQL,Docker"

## 📂 Repository Structure
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── conversationalbot.py # Streamlit app entry point
├── data/ # Your CSV job data (user must add)
├── vectorstore/ # Auto-generated FAISS database
├── .env # Environment config (optional)
└── Interface.png # UI screenshot (optional)


## ⚙️ How It Works
1. **Load CSV data** from `data/`
2. **Validate schema** for required columns
3. Convert each job posting into a **text document**
4. **Generate embeddings** (HuggingFace MiniLM-L6-v2)
5. Store vectors in **FAISS**
6. **Retriever** fetches top‑K matches for a query
7. **LLaMA 2** generates an answer using retrieved documents + chat history
8. Display results in the **Streamlit chat interface**


## 🖥️ Quickstart

### 1️⃣ Clone & Install Dependencies
git clone <your-repo-url>
cd <your-repo>
pip install -r requirements.txt

### 2️⃣ Download Model
Download a **LLaMA‑2‑7B‑Chat** `.gguf` file (e.g., `llama-2-7b-chat.Q4_K_M.gguf`).  
Save it in the project root and update the `model_path` in `conversationalbot.py`:
model_path="llama-2-7b-chat.Q4_K_M.gguf"


### 3️⃣ Add Your CSV Data
Place one or more CSV files following the schema into the `data/` folder.

### 4️⃣ Run the App
streamlit run conversationalbot.py

### 5️⃣ Using the Chatbot
- Click **"Load and Process Documents"** in the sidebar.
- Ask natural language questions like:
  - "What skills are required for a Data Analyst position?"
  - "List backend roles that require Django."
  - "Which companies are offering remote work?"

---

## ⚙️ Configuration
- Retriever search depth:  
search_kwargs={"k": 3}
- Model generation params:
- `temperature`
- `max_tokens`
- `n_ctx`
- Prompt defined in `llmtemplate` for style/tone

---

## 🛠 Troubleshooting
- **No CSVs found** → Ensure your files are in the `data/` folder
- **Missing columns** → Match required schema exactly
- **Slow performance** → First run takes longer to embed data
- **Out of memory** → Try smaller `.gguf` model or reduce `n_ctx`

---

## 🔒 Privacy
- Entire pipeline runs locally once model + CSVs are provided  
- No external API calls — your job data never leaves your system

---

## 📚 Tech Stack
- **Python**  
- **Pandas** — CSV parsing & preprocessing  
- **FAISS** — vector similarity search  
- **HuggingFace sentence-transformers** — embeddings  
- **LangChain** — retrieval + LLM orchestration  
- **LlamaCpp** — local LLaMA 2 inference  
- **Streamlit** — web UI  

---

## 📸 Demo
![Chatbot Interface](Interface.png)

