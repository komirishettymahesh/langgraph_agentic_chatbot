import yaml

class Config:
    def __init__(self, config_file="./src/langgraph_agentic_ai/ui/uiconfigfile.yaml"):
        self.config = config_file
        with open(self.config) as f:
            self.config_parameters = yaml.safe_load(f)
    
    def get_llm_options(self):
        return self.config_parameters['LLM_OPTIONS']
    
    def get_page_title(self):
        return self.config_parameters['PAGE_TITLE']
    
    def get_model_options(self):
        return self.config_parameters['MODEL_OPTIONS']
    
    def get_usecase_options(self):
        return self.config_parameters['USECASE_OPTIONS']