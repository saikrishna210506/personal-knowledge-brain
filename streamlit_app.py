import streamlit as st

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = {}

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []
    
from utils.pdf_loader import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.vector_store import (
    store_chunks,
    search_chunks,
    clear_collection
)
from utils.rag_engine import generate_answer


st.set_page_config(
    page_title="Personal Knowledge Brain",
    page_icon="🧠"
)
st.title("🧠 Personal Knowledge Brain")

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

if "all_uploaded_files" not in st.session_state:
    st.session_state.all_uploaded_files = []
uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:

        exists = False

        for old_file in st.session_state.all_uploaded_files:

            if old_file.name == file.name:
                exists = True

        if not exists:
            st.session_state.all_uploaded_files.append(file)

uploaded_files = st.session_state.all_uploaded_files

st.sidebar.title("📂 Uploaded Documents")

if uploaded_files:
    for file in uploaded_files:
        st.sidebar.write(f"📄 {file.name}")

if st.sidebar.button("➕ Add More PDFs"):
    st.rerun()

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.memory = {}
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 Agent Memory")

for key, value in st.session_state.memory.items():
    st.sidebar.info(f"{key}: {value}")
if uploaded_files:

    for uploaded_file in uploaded_files:

        if uploaded_file.name not in st.session_state.processed_files:

            save_path = f"uploads/{uploaded_file.name}"

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            text = extract_text_from_pdf(save_path)

            chunks = chunk_text(text)

            store_chunks(chunks)

            st.session_state.processed_files.append(
                uploaded_file.name
            )

    st.success(
        f"✅ {len(uploaded_files)} PDF(s) processed and indexed successfully!"
    )


# Show conversation first

if st.session_state.chat_history:

    st.subheader("Conversation")

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

# ChatGPT-style input

question = st.chat_input(
    "Ask anything about your documents..."
)

if question:

    if not uploaded_files:
        st.warning("Please upload at least one PDF.")

    elif question.strip() == "":
        st.warning("Please enter a question.")

    else:

        results = search_chunks(question)

        all_chunks = results["documents"][0]
        print("\nTOTAL RETRIEVED:", len(all_chunks))

        selected_chunks = []

        for chunk in all_chunks:

           if len(chunk.strip()) > 50:
             selected_chunks.append(chunk)

        context = "\n\n".join(selected_chunks[:5])

        # Build conversation history
        history_text = ""

        for chat in st.session_state.chat_history:
            history_text += (
                f"User: {chat['question']}\n"
                f"Assistant: {chat['answer']}\n\n"
            )

        # Build memory text
        memory_text = ""

        for key, value in st.session_state.memory.items():
            memory_text += f"{key}: {value}\n"
        # Update memory from user's question

        projects = [
         "Personal Knowledge Brain",
         "AI Digital Clone",
         "College Bus Management System",
         "IoT-Based Carbon Emission Monitoring System"
        ]

        for project in projects:

         if project.lower() in question.lower():

          st.session_state.memory["last_project"] = project


        certifications = [
        "AWS Cloud Essentials",
         "Deloitte Data Analytics",
         "Software Engineering Job Simulation",
         "GenAI Powered Data Analytics"
        ]

        for cert in certifications:

         if cert.lower() in question.lower():

          st.session_state.memory["last_certification"] = cert
        with st.spinner("Thinking..."):


            answer = generate_answer(
                question,
                context,
                history_text,
                memory_text
            )
        if answer is None:
          answer = "I couldn't generate an answer."
        companies = ["Codec Technologies"]

        for company in companies:

         if company.lower() in question.lower():

           st.session_state.memory["last_company"] = company

        projects = [
         "Personal Knowledge Brain",
         "AI Digital Clone",
         "College Bus Management System",
         "IoT-Based Carbon Emission Monitoring System"
        ]
        if answer:
         for project in projects:

          if project.lower() in answer.lower():

           st.session_state.memory["last_project"] = project
        if answer:   
         for company in companies:

          if company.lower() in answer.lower():

           st.session_state.memory["last_company"] = company  

        certifications = [
         "AWS Cloud Essentials",
         "Deloitte Data Analytics",
         "Software Engineering Job Simulation",
         "GenAI Powered Data Analytics"
         ]

        found_certs = []
        if answer:
         for cert in certifications:

          if cert.lower() in answer.lower():
           found_certs.append(cert)

        if found_certs:
          st.session_state.memory["certifications"] = found_certs
        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()