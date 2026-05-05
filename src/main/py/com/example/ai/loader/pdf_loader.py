
import streamlit as st
import pypdf
from langchain_openai import OpenAIEmbeddings, OpenAI
from com.example.ai.LLMManager import LLMManager

def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None
    
def generate_paper_summary(text):
    try:

        llm = LLMManager.get_model(temperature=0.3, max_tokens=1000) #OpenAI(temperature=0.3, max_tokens=1000)  
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