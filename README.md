# Job Data Conversational Chatbot
A conversational bot built using LangChain and LLM using a jobs dataset that I extracted from careers pages.

This project is a **Retrieval-Augmented Generation (RAG)** based chatbot that helps job seekers explore and query job listings in a conversational manner. It loads job data from CSVs, creates semantic embeddings, and uses a local Llama 2 model to provide accurate, context-based answers.

The chatbot runs locally, ensuring **privacy** and **offline capability**.

## Project Overview

## 🚀 Features
- **Load job postings from CSVs** with validation for required columns.
- **Semantic Search** powered by [FAISS](https://github.com/facebookresearch/faiss).
- **Dense Embeddings** via HuggingFace `all-MiniLM-L6-v2`.
- **Local LLM Inference** with Llama 2 (via [LlamaCpp](https://github.com/ggerganov/llama.cpp)).
- **Conversational Memory** to keep chat context.
- **Custom Prompting** to ensure factual, ethical, and concise responses.
- **Interactive Frontend** built with Streamlit.


## ⚙️ How It Works
1. **Load CSV Data**  
   CSVs in `data/` must contain: `title`, `company`, `job_description`, `key_skills`.

2. **Generate Embeddings**  
   Each job posting is converted into a vector using HuggingFace `all-MiniLM-L6-v2`.

3. **Build Vector Store**  
   Vectors stored in FAISS for fast semantic search.

4. **Set Up RAG Chain**  
   - Retriever queries FAISS for relevant postings.
   - Local Llama 2 model generates answer conditioned on retrieved docs + chat history.

5. **Conversational UI**  
   Streamlit app displays question/answer bubbles in real time.

---

## 🖥️ Running Locally
### 1. Clone and Install

git clone <repo-url>
cd project
pip install -r requirements.txt

### 2. Download Model  
Place your Llama 2 `.gguf` file in the root folder and update the path in `app.py`.

### 3. Add CSV Data  
Put your job postings CSV files into the `data/` directory.

### 4. Run Streamlit App  


## 📌 Notes
- The system only answers based on the provided documents. If no info is found, it explicitly states so.
- Works fully offline once CSVs and model file are available.
- Ideal for **private data querying** without exposing data to API calls.

---

## 🛠️ Tech Stack
- **LangChain** → Orchestrating RAG pipeline.
- **FAISS** → Vector similarity search.
- **HuggingFace Transformers** → Text embeddings.
- **LlamaCpp** → Running Llama 2 locally.
- **Streamlit** → User interface.
- **Pandas** → CSV processing.

---

## 📷 Demo Screenshot
*(Insert screenshot here)*
