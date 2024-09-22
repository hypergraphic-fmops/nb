import streamlit as st
from dotenv import load_dotenv
from api_handlers import OllamaHandler, PerplexityHandler, GroqHandler
from utils import generate_response, litellm_config, litellm_instructions
from config_menu import config_menu, display_config
from logger import logger
import os
from handlers.litellm_handler import LiteLLMHandler
import networkx as nx
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

def load_css():
    # Load custom CSS styles
    with open(os.path.join(os.path.dirname(__file__), "..", "static", "styles.css")) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def setup_page():
    # Configure the Streamlit page
    st.set_page_config(page_title="multi1 - Unified AI Reasoning Chains", page_icon="🧠", layout="wide")
    load_css()
    
    # Display the main title
    st.markdown("""
    <h1 class="main-title">
        🧠 multi1 - Unified AI Reasoning Chains
    </h1>
    """, unsafe_allow_html=True)
    
    # Display the app description
    st.markdown("""
    <p class="main-description">
        This app demonstrates AI reasoning chains using different backends: Ollama, Perplexity AI, Groq, and a custom workflow for code analysis and refactoring.
        Choose a backend or workflow and enter your query or code to see the step-by-step process.
    </p>
    """, unsafe_allow_html=True)

def get_api_handler(backend, config):
    if backend == "Ollama":
        return OllamaHandler(config['OLLAMA_URL'], config['OLLAMA_MODEL'])
    elif backend == "Perplexity AI":
        return PerplexityHandler(config['PERPLEXITY_API_KEY'], config['PERPLEXITY_MODEL'])
    elif backend == "Groq":
        return GroqHandler(config['GROQ_API_KEY'], config['GROQ_MODEL'])
    else:  # LiteLLM
        litellm_config = st.session_state.get('litellm_config', {})
        return LiteLLMHandler(
            litellm_config.get('model', ''),
            litellm_config.get('api_base', ''),
            litellm_config.get('api_key', '')
        )

def code_analysis_workflow(code):
    # Placeholder for the code analysis and refactoring workflow
    # This function will be expanded to implement the steps defined in the 'stages' dictionary
    st.write("## Code Analysis and Refactoring Workflow")
    st.write("**Code submitted:**")
    st.code(code, language="python")

    # Placeholder for each stage of the workflow
    for stage, dependencies in stages.items():
        st.write(f"### {stage}")
        # Implement the logic for each stage here (e.g., call LLMs, extract metrics, etc.)
        st.write("**Placeholder for stage implementation**")

def main():
    logger.info("Starting the application")
    setup_page()

    # Set up the sidebar for configuration
    st.sidebar.markdown('<h3 class="sidebar-title">⚙️ Settings</h3>', unsafe_allow_html=True)
    config = config_menu()
    
    # Allow user to select the AI backend or workflow
    option = st.sidebar.selectbox("Choose Option", ["LiteLLM", "Ollama", "Perplexity AI", "Groq", "Code Analysis Workflow"])
    
    if option == "LiteLLM":
        litellm_instructions()
        litellm_config()
    elif option != "Code Analysis Workflow":
        display_config(option, config)
    
    if option == "Code Analysis Workflow":
        # Code input for the workflow
        user_code = st.text_area("Enter your Python code:", placeholder="```python\ndef my_function():\n    # Your code here\n```", language="python")
        if user_code:
            code_analysis_workflow(user_code)
    else:
        api_handler = get_api_handler(option, config)
        logger.info(f"Selected option: {option}")

        # User input field
        user_query = st.text_input("💬 Enter your query:", placeholder="e.g., How many 'R's are in the word strawberry?")

        if user_query:
            logger.info(f"Received user query: {user_query}")
            st.write("🔍 Generating response...")
            response_container = st.empty()
            time_container = st.empty()

            try:
                # Generate and display the response
                for steps, total_thinking_time in generate_response(user_query, api_handler):
                    with response_container.container():
                        for title, content, _ in steps:
                            if title.startswith("Final Answer"):
                                # Display the final answer
                                st.markdown(f'<h3 class="expander-title">🎯 {title}</h3>', unsafe_allow_html=True)
                                st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                                logger.info(f"Final answer generated: {content}")
                            else:
                                # Display intermediate steps
                                with st.expander(f"📝 {title}", expanded=True):
                                    st.markdown(f'<div>{content}</div>', unsafe_allow_html=True)
                                logger.debug(f"Step completed: {title}")

                    # Display total thinking time
                    if total_thinking_time is not None:
                        time_container.markdown(f'<p class="thinking-time">⏱️ Total thinking time: {total_thinking_time:.2f} seconds</p>', unsafe_allow_html=True)
                        logger.info(f"Total thinking time: {total_thinking_time:.2f} seconds")
            except Exception as e:
                # Handle and display any errors
                logger.error(f"Error generating response: {str(e)}", exc_info=True)
                st.error("An error occurred while generating the response. Please try again.")


# Define the stages for the code analysis workflow (same as before)
stages = {
    "Coleta de Dados\n(Códigos Python\nde Graduandos)": [],
    "Pré-processamento\nde Código": ["Coleta de Dados\n(Códigos Python\nde Graduandos)"],
    "Análise de Código com\nLLM (Identificação\nde Erros e Complexidade)": ["Pré-processamento\nde Código"],
    "Extração de Métricas\nde Código (Complexidade\nCiclomática e Acoplamento)": ["Análise de Código com\nLLM (Identificação\nde Erros e Complexidade)"],
    "Identificação de Padrões\nde Erros e Complexidade": ["Extração de Métricas\nde Código (Complexidade\nCiclomática e Acoplamento)"],
    "Desenvolvimento de\nEstratégias de Refatoração\n(com LLMs)": ["Identificação de Padrões\nde Erros e Complexidade"],
    "Aplicação de\nRefatoração\nem Código": ["Desenvolvimento de\nEstratégias de Refatoração\n(com LLMs)"],
    "Avaliação da\nRefatoração (Redução de\nComplexidade e Acoplamento)": ["Aplicação de\nRefatoração\nem Código"],
    "Feedback para\nGraduandos (com LLMs)": ["Avaliação da\nRefatoração (Redução de\nComplexidade e Acoplamento)"],
    "Análise da\nEfetividade da\nAprendizagem": ["Feedback para\nGraduandos (com LLMs)"],
    "Publicação\nAcadêmica": ["Análise da\nEfetividade da\nAprendizagem"],
}

if __name__ == "__main__":
    main()