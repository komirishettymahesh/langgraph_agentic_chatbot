from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.langgraph_agentic_ai.nodes.basic_chatbot import BasicChatbotNode
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node

class GraphBuilder:
    def __init__(self, model):
        self.model = model
        self.graph_builder = StateGraph(State)
        
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chabot graph using Langgraph. This method initialized a chatbot node 
        using the 'BasicChatbotNode' class and integrates it into the graph. The chatbot node 
        is set as both the entry and exit point of the graph
        """
        
        self.basic_chatbot_node = BasicChatbotNode(self.model)
        
        self.graph_builder.add_node('chatbot', self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, 'chatbot')
        self.graph_builder.add_edge('chatbot', END)
        
    def chatbot_with_tool_graph(self):
        """
        Builds a advanced chabot graph using Langgraph with tool integration. This method creates a chatbot graph 
        and a tool node. It defines tools, initializes the chatbot with tool capabilities, and sets up conditional
        and direct edges between nodes. The chatbot node is set as the entry point
        """
        ## define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)
        
        #define the chatbot node
        self.chatbot_with_tool_node = ChatbotWithToolNode(self.model)
        chatbot_node = self.chatbot_with_tool_node.create_chatbot(tools)
        self.graph_builder.add_node('chatbot', chatbot_node)
        self.graph_builder.add_node('tools', tool_node)
        
        self.graph_builder.add_edge(START, 'chatbot')
        self.graph_builder.add_conditional_edges('chatbot', tools_condition)
        self.graph_builder.add_edge('tools', 'chatbot')
        self.graph_builder.add_edge('chatbot', END)
    
    
    def ai_news_builder_graph(self):
        
        ai_news_node = AINewsNode(self.model)
        
        self.graph_builder.add_node('fetch_news', ai_news_node.fetch_news)
        self.graph_builder.add_node('summarize_news', ai_news_node.summarize)
        self.graph_builder.add_node('save_results',ai_news_node.save_result)
        
        self.graph_builder.set_entry_point('fetch_news')
        self.graph_builder.add_edge('fetch_news', 'summarize_news')
        self.graph_builder.add_edge('summarize_news','save_results')
        self.graph_builder.add_edge('save_results', END)
        
    
    def setup_graph(self, usecase:str):
        """
        Sets up the graph for the selected use case 
        """
        if usecase.strip() == "chatbot_with_web":
            self.chatbot_with_tool_graph()
            return self.graph_builder.compile()
        
        elif usecase == 'basic_chatbot':
            self.basic_chatbot_build_graph()
            return self.graph_builder.compile()
        
        elif usecase == 'ai_news':
            self.ai_news_builder_graph()
            return self.graph_builder.compile()
    
