# Conversational_bot
A conversational bot built using LangChain and LLM using a jobs dataset that I extracted from careers pages

Welcome to the Job Chatbot project!! This repository contains the code for a chatbot that helps job seekers by providing detailed information about job listings. The chatbot uses LangChain for conversational retrieval, FAISS for vector search, and LlamaCpp for generating responses.
I've built this after taking inspiration from several videos and articles.


## Project Overview

This project involves the following steps:
1. **Loading Job Documents**: Extracting job details from CSV files.
2. **Creating Embeddings**: Generating embeddings for job documents using HuggingFace.
3. **Building Vector Database**: Storing embeddings in a FAISS vector database.
4. **Setting up Conversational Chain**: Using LangChain to create a conversational retrieval chain.
5. **Integrating with LlamaCpp**: Generating responses based on retrieved documents.
6. **Streamlit Interface**: Building a user-friendly interface for interacting with the chatbot.



Please refer to the notebook page for a detailed step-by-step process and the accompanying code.
