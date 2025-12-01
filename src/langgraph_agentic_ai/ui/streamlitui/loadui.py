import streamlit as st 
import os
from src.langgraph_agentic_ai.ui.uiconfigfile import Config 


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title='' + self.config.get_page_title(), layout='wide')
        st.header(self.config.get_page_title())
        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False
        
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
            
            if self.user_controls['selected_use_case'] == 'chatbot_with_web':
                os.environ['TAVILY_API_KEY'] = self.user_controls['TAVILY_API_KEY'] = st.session_state['TAVILY_API_KEY'] = st.text_input('TAVILY_API_KEY', type='password')
                
                if self.user_controls['TAVILY_API_KEY'] == '':
                    st.warning('Please enter Tavily API Key')
                    
                    
            if self.user_controls['selected_use_case'] == 'ai_news':
                os.environ['TAVILY_API_KEY'] = self.user_controls['TAVILY_API_KEY'] = st.session_state['TAVILY_API_KEY'] = st.text_input('TAVILY_API_KEY', type='password')
                
                if self.user_controls['TAVILY_API_KEY'] == '':
                    st.warning('Please enter Tavily API Key')
                
                st.subheader('AI News Explorer')
                
                with st.sidebar:
                    timeframe = st.selectbox(
                        "Select Time Frame",
                        ['Daily', 'Weekly', 'Monthly'],
                        index=0
                    )
                   
                if st.button("Fetch Latest AI News", use_container_width=True):
                    st.session_state.timeframe = timeframe
                    st.session_state.IsFetchButtonClicked = True  
                        
                
        return self.user_controls
