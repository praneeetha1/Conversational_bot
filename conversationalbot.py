import os
import pandas as pd
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain import PromptTemplate
from dotenv import load_dotenv
from langchain_community.llms import LlamaCpp

# html template for chat display
bot_template = "<div style='padding: 10px; border-radius: 5px; background-color: #4a4a4a; margin-bottom: 5px;'><p style='margin: 0; color: #ffffff;'>{{MSG}}</p></div>"
user_template = "<div style='padding: 10px; border-radius: 5px; background-color: #2b2b2b; margin-bottom: 5px; text-align: right;'><p style='margin: 0; color: #ffffff;'>{{MSG}}</p></div>"

load_dotenv()

# define a prompt
llmtemplate = """[INST]
You are a helpful assistant for job seekers. Please provide the information in a friendly manner, including all the details you could find in the documents.
Follow these guidelines for the ouput generation:
- Answer the question based solely on the information in the provided documents.
- Be direct and factual. Begin your responses without using introductory phrases.
- Maintain an ethical and unbiased tone, avoiding harmful or offensive content.
- Do not fabricate any information and say "I cannot provide an answer absed on the provided documetns" if you dont find any information from the documents.
{question}
[/INST]
"""

# directory where csv files are located
DATA_PATH = "data"


# load the csv files into documents - stores them as strings in a list
def load_documents():
    documents = []
    csv_files = []

    try:
        csv_files = [file for file in os.listdir(DATA_PATH) if file.endswith('.csv')]

        for file in csv_files:
            file_path = os.path.join(DATA_PATH, file)
            df = pd.read_csv(file_path)

            expected_columns = ['title', 'company', 'job_description', 'key_skills']
            if not all(col in df.columns for col in expected_columns):
                raise ValueError(f"Columns {expected_columns} not found in {file_path}")

            for _, row in df.iterrows():
                document = f"Title: {row['title']}\n"
                document += f"Company: {row['company']}\n"
                document += f"\n{row['job_description']}\n"
                document += f"Key Skills: {row['key_skills']}\n\n"
                documents.append(document)

    except Exception as e:
        st.error(f"Error processing files: {str(e)}")

    return documents, csv_files


# input the documents into a local faiss vector database by creating embeddings (using minilm model)
def input_into_vectordb(documents):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})
    db = FAISS.from_texts(documents, embeddings)
    db.save_local('vectorstore/db_faiss')
    return db


# set up a conversational chain using LlamaCpp and faiss
# intialize the llm, create a retriver form the faiss db, setup a conversation chain with memory for chat history
def get_conversation_chain(vectordb):
    llama_llm = LlamaCpp(
        model_path="llama-2-7b-chat.Q4_K_M.gguf",
        temperature=0.75,
        max_tokens=200,
        top_p=1,
        n_ctx=3000
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(llmtemplate)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True, output_key='answer'
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llama_llm,
        retriever=retriever,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        memory=memory,
        return_source_documents=True
    )

    return conversation_chain


# handle the user queries, generate responces using conversation chain and display the chat messages
def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


# run the main streamlit app
# allows users to load and process documents, ask questions and chat with the bot
def main():
    st.set_page_config(page_title="Chat with Job Data", page_icon=":briefcase:")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    st.header("Chat with Job Data")
    user_question = st.text_input("Ask a question about job details:")
    
    if user_question:
        if st.session_state.conversation:
            handle_userinput(user_question)
        else:
            st.warning("Please load and process documents first.")

    with st.sidebar:
        st.subheader("Your Job Documents")
        if st.button("Load and Process Documents"):
            with st.spinner("Processing"):
                docs, csv_files = load_documents()
                st.write(f"Loaded {len(csv_files)} files.")
                st.write("Creating embeddings and vector database...")
                vectorstore = input_into_vectordb(docs)
                st.write("Creating conversation chain...")
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success(f"Processed {len(csv_files)} files and created conversation chain.")

if __name__ == "__main__":
    main()