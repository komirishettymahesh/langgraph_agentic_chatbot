#from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
from typing import List
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages: Annotated[List, add_messages]