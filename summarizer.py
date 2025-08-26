import google.generativeai as genai
import streamlit as st

def summarize_text(text: str, summary_level: str) -> str:
    """
    Summarizes a given text using Google Gemini.
    
    Args:
        text (str): The text to be summarized.
        summary_level (str): 'brief', 'moderate', or 'deep' to control summary length.

    Returns:
        str: The summarized text.
    """
    
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompts = {
        "brief": "Please provide a brief, concise summary of the following academic notes. Focus on the main points and key takeaways.",
        "moderate": "Please provide a moderate length summary of the following academic notes. Include key concepts, examples, and important details.",
        "deep": "Please provide a very detailed and deep summary of the following academic notes. Cover all major topics, sub-topics, definitions, and complex ideas. Structure it with headings and bullet points for clarity."
    }
    
    prompt_template = prompts.get(summary_level, prompts["moderate"])
    full_prompt = f"{prompt_template}\n\nNotes:\n{text}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error during summarization: {e}")
        return None