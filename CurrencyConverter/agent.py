import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import Tool, initialize_agent, AgentType

from tools import (
    get_currency,
    get_exchange_rate,
    get_stock_indices,
    get_maps_pin
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM setup (Groq Llama 3.1)
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0
)

tools = [
    Tool(
        name="Currency",
        func=get_currency,
        description="Get official currency of a country"
    ),
    Tool(
        name="Exchange Rate",
        func=get_exchange_rate,
        description="Get exchange rate vs USD INR GBP EUR"
    ),
    Tool(
        name="Stock Index",
        func=get_stock_indices,
        description="Get major stock indices values"
    ),
    Tool(
        name="Maps Pin",
        func=get_maps_pin,
        description="Returns Google Maps pin of stock exchange HQ"
)

]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    early_stopping_method="generate"
)
