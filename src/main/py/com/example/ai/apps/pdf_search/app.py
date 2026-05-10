#
# streamlit run src/main/py/com/example/ai/apps/pdf_search/app.py
#
import streamlit as st
from com.example.ai.apps.pdf_search.basic_crew import create_crew,retrieval_action, generation_action
from com.example.ai.loader.LoadManager import LoadManager
from com.example.ai.vectors.VectorStoreManager import VectorStoreManager
from com.example.ai.LLMManager import LLMManager


st.set_page_config(
    page_title="Research Paper Analyst",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'vstore_mgr' not in st.session_state:
    st.session_state.vstore_mgr = None

if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'paper_summary' not in st.session_state:
    st.session_state.paper_summary = None

def generate_paper_summary(text):
    try:

        llm = LLMManager.get_model(temperature=0.3, max_tokens=4096) #OpenAI(temperature=0.3, max_tokens=1000)  
        summary_prompt = (
            "You are an expert research analyst. Please provide a comprehensive summary of this research paper. "
            "Include the following sections:\n\n"
            "1. **Title and Authors** (if available)\n"
            "2. **Abstract/Summary** - Main research question and objectives\n"
            "3. **Methodology** - How the research was conducted\n"
            "4. **Key Findings** - Main results and discoveries\n"
            "5. **Contributions** - What new knowledge or insights this paper provides\n"
            "6. **Limitations** - Any limitations mentioned by the authors\n"
            "7. **Future Work** - Suggested future research directions\n\n"
            "Please be thorough but concise. Use clear headings and bullet points where appropriate.\n\n"
            f"Research Paper Text:\n{text[:8000]}\n\n"  # Limit text to avoid token limits
            "Summary:"
        )
        summary = llm.invoke(summary_prompt)
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None
    
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
                    _documents = LoadManager.from_upload(uploaded_file)    
                    text = LoadManager.text_from_documents(_documents)
                    if text:
                        summary = generate_paper_summary(text)        
                        if summary:
                            st.session_state.paper_summary = summary
                            vstore_mgr = VectorStoreManager(
                                store_type="faissdb", 
                                collectionOrIndexName="faiss_index"
                            )
                            vstore_mgr.add_documents(_documents)
                        if vstore_mgr:
                            st.session_state.vstore_mgr = vstore_mgr
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
                    crew = create_crew(st.session_state.vstore_mgr, status_callback)
                    status_placeholder.info("Starting AI analysis...")
                    log_step("CrewAI execution started")
                    status_placeholder.info("Retrieving relevant passages...")
                    retrieved_passages = retrieval_action(prompt, st.session_state.vstore_mgr)
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