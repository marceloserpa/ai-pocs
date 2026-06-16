import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_classic.agents import AgentExecutor, create_react_agent, load_tools, Tool

import langchain.agents
print(dir(langchain.agents))

from dotenv import load_dotenv

load_dotenv()

openai_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

react_template = """Answer the following questions as best you can. You have
    access to the following tools:
    {tools}
    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do

    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought:{agent_scratchpad}"""

prompt = PromptTemplate(
    template=react_template,
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
)

search = DuckDuckGoSearchResults()
search_tool = Tool(
    name="duckduck",
    description="A web search engine. Use this to as a search engine for general queries.",
    func=search.run,
)

tools = load_tools(["llm-math"], llm=openai_llm)
tools.append(search_tool)


agent = create_react_agent(openai_llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

agent_executor.invoke(
    {
    "input": "What is the current price of a MacBook Pro in USD? How much would it cost in EUR if the exchange rate is 0.85 EUR for 1 USD."
    }
)