#
# streamlit run src/pdf_search_crew/app.py
#
import streamlit as st
from com.example.ai.loader.pdf_loader import extract_text_from_pdf, generate_paper_summary
from com.example.ai.vectors.vector_store import process_document
from com.example.ai.apps.pdf_search.basic_crew import create_crew,retrieval_action, generation_action

st.set_page_config(
    page_title="Research Paper Analyst",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'paper_summary' not in st.session_state:
    st.session_state.paper_summary = None

def main():

    st.title("Research Paper Analyst")
    st.markdown("Upload a research paper and ask questions about it using AI-powered analysis.")    
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type="pdf",
            help="Upload a research paper in PDF format"
        )        

        if uploaded_file is not None:
            st.info(f"File uploaded: {uploaded_file.name}")        
            if st.button("Process Document", type="primary"):
                with st.spinner("Processing document and generating summary..."):
                    text = extract_text_from_pdf(uploaded_file)    
                    if text:
                        summary = generate_paper_summary(text)        
                        if summary:
                            st.session_state.paper_summary = summary
                            vectorstore = process_document(text)        
                        if vectorstore:
                            st.session_state.vectorstore = vectorstore
                            st.session_state.document_processed = True
                            st.info("Document processed successfully! Summary generated and ready for questions.")
                        else:
                            st.error("Failed to process document.")
                    else:
                        st.error("Failed to extract text from PDF.")

    if not st.session_state.document_processed:
        st.info("Please upload and process a PDF document using the sidebar to get started.")   

    else:
        with st.expander("Paper Summary", expanded=False):
            if st.session_state.paper_summary:
                st.markdown(st.session_state.paper_summary)
            else:
                st.warning("Summary not available.")

        st.subheader("Ask Questions About Your Research Paper")        

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"]) 

        if prompt := st.chat_input("Ask a question about the research paper..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})  

            with st.chat_message("user"):
                st.write(prompt)        

            with st.chat_message("assistant"):
                progress_container = st.container()
                execution_trace_container = st.expander("Execution Details", expanded=False)     

                with progress_container:
                    st.info("Initializing AI agents...")

                try:
                    status_placeholder = st.empty()
                    trace_placeholder = execution_trace_container.empty()
                    execution_steps = []

                    def log_step(step):
                        execution_steps.append(step)
                        with trace_placeholder:
                            for i, s in enumerate(execution_steps, 1):
                                st.write(f"{i}. {s}")

                    def status_callback(message):
                        status_placeholder.info(message)
                        log_step(message)                    

                    status_placeholder.info("Initializing AI agents...")
                    log_step("CrewAI agents initialized")
                    crew = create_crew(st.session_state.vectorstore, status_callback)
                    status_placeholder.info("Starting AI analysis...")
                    log_step("CrewAI execution started")
                    status_placeholder.info("Retrieving relevant passages...")
                    retrieved_passages = retrieval_action(prompt, st.session_state.vectorstore)
                    log_step("Retrieved relevant passages from the research paper")
                    status_placeholder.info("Generating comprehensive answer...")

                    inputs = {
                        "user": prompt,
                        "Retriever": retrieved_passages
                    }

                    response = generation_action(inputs)
                    log_step("Generated detailed answer with citations")
                    status_placeholder.info("Analysis complete!")
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.markdown("### AI Analysis Result:")
                    st.write(response)
                    with execution_trace_container:
                        st.markdown("### Execution Summary:")
                        st.info("**Retriever Agent**: Found relevant passages from the research paper")
                        st.info("**Generator Agent**: Created comprehensive answer with citations")
                        st.info(f"**Total Steps**: {len(execution_steps)}")
                        st.markdown("### Detailed Execution Trace:")

                        for i, step in enumerate(execution_steps, 1):
                            st.write(f"{i}. {step}")            

                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

        

        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


if __name__ == "__main__":
    main()