from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os 

class AINewsNode:
    def __init__(self, model):
        """
        Initialize the AINews node with the API keys for Tavily and Azure
        """
        self.tavily = TavilyClient()
        self.llm = model
        self.state = {}
        
    def fetch_news(self, state:dict) -> dict:
        """
        Fetch AI news based on the specified frequency
        
        Args:
            state: The state containing the frequency
            
        Returns:
            dict: Updated state with 'news_data' key containing the fetched news
        """
        
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d', 'weekly': 'w', 'monthly': 'm'}
        days_map = {'daily':1, 'weekly':7, 'monthly': 30, 'year': 366}
        
        response = self.tavily.search(
            query = 'Top Artificial Intelligence technology news India and globally',
            topic='news',
            time_range=time_range_map[frequency],
            include_answer='advanced',
            max_results=15,
            days=days_map[frequency]
        )
        
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return self.state
    
    def summarize(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        
        Args:
        state(dict) -> the state dictionary containing news data
        
        Returns: 
        dict: updated state with summary key containing the summarized news        
        """
        
        news_items = self.state['news_data']
        
        prompt_template = ChatPromptTemplate(
            [('system', """Summarize AI news articles into the markdown format. For each item include
             - Date in **YYYY-MM-DD** format in IST timezone
             - Concise sentences summary from latest news
             - Sort news by date wise (latest first)
             - Source URL as link
             Use format:
             #### [Date]
             - [Summary](URL)
             """),
            ('user', "Articles:\n{articles}")
        ])
        
        articles_str = '\n\n'.join([
            f"Content: {item.get('content','')}\nURL:{item.get('url','')}\nDate: {item.get('published_date','')}" for item in news_items
        ])
        
        try:
            formatted_prompt = prompt_template.format(articles=articles_str)
            response = self.llm.invoke(input=formatted_prompt)
        except Exception as e:
            print(e)
        
        state['summary'] = response.content
        self.state['summary'] = state['summary']
    
        return self.state 
    
    
    def save_result(self, state:dict):        
        frequency = self.state['frequency']
        summary = self.state['summary']
        
        try: 
            directory = "./AINews"
            os.makedirs(directory, exist_ok=True)
            filename = os.path.join(directory, f"{frequency}_summary.md")
            with open(filename,'w') as f:
                f.write(f'# {frequency.capitalize()} AI News Summary\n\n')
                f.write(summary)
        except Exception as e:
            print(e)
        self.state['filename'] = filename
        return self.state 