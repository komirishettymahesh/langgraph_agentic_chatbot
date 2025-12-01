import streamlit as st 
import os 
#import sys 
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from src.langgraph_agentic_ai.ui.uiconfigfile import Config 


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title='' + self.config.get_page_title(), layout='wide')
        st.header(self.config.get_page_title())
        
        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            #LLM selection
            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)
            if self.user_controls['selected_llm'] == 'azure_openai':
                model_options = self.config.get_model_options()
                self.user_controls['selected_llm_model'] = st.selectbox('Select Model', model_options)
                self.user_controls['azure_openai_api_key'] = st.session_state['azure_openai_api_key'] = st.text_input('API Key', type='password')
                
                #validate API key
                if not self.user_controls['azure_openai_api_key']:
                    st.warning('Please enter your API ket to proceed')
            
            
            #use case selection 
            self.user_controls['selected_use_case'] = st.selectbox("select use case", usecase_options)
        return self.user_controls    
