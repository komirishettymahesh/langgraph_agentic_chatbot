import os 
import streamlit as st 
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()
class AzureLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input
    
    def get_llm_model(self):
        try:
            azure_open_ai_key = self.user_controls_input['azure_openai_api_key']
            AZURE_API_ENDPOINT = os.getenv('AZURE_API_ENDPOINT')
            AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME')
            selected_model_name = self.user_controls_input['selected_llm_model']
            AZURE_API_VERSION = os.getenv('AZURE_API_VERSION')
            
            if azure_open_ai_key == '' or os.environ['azure_open_ai_key'] == '':
                st.error('Please enter the API Key')
                
            llm = AzureChatOpenAI(
                                model=selected_model_name,
                                azure_endpoint=AZURE_API_ENDPOINT,
                                deployment_name=AZURE_DEPLOYMENT_NAME,
                                api_version=AZURE_API_VERSION
                            )
            
        except Exception as e: 
            raise ValueError(f'Error occured with Exception {e}')
        
        return llm
            
