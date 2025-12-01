import streamlit as st 
from src.langgraph_agentic_ai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraph_agentic_ai.llms.azoreopenaillm import AzureLLM
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    loads and runs the langgraph agenticAI application with streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use cases, and displays the output while 
    implementing exception handling for robustness.
    """
    
    #Load UI 
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error('Error: failed to load user input from the UI.')
        return 
    
    user_message = st.chat_input('Enter your message')
    
    if user_message:
        try: 
            llm_config = AzureLLM(user_controls_input=user_input)
            model = llm_config.get_llm_model()
            if not model:
                st.error("Error: LLM model could not be initialized")
                return 
            
            #Initialize and setup the graph based on use case 
            use_case = user_input.get('selected_use_case').strip()
            
            if not use_case:
                st.error('Error: No use case selected')
                return
            
            graph_builder = GraphBuilder(model)
            try:
                graph_workflow = graph_builder.setup_graph(use_case)
                DisplayResultStreamlit(use_case, graph_workflow, user_message).display_result_on_ui()
                
            except Exception as e:
                st.error(f"Error graph setup failed: {e}")
                return
            
            
        except Exception as e: 
            print(user_input)
            st.error(f"Error setup failed: {e}")
            
            return 