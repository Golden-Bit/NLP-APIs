import asyncio
from typing import Any

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain_core.callbacks import Callbacks
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

from chains.chain_scripts.utilities.dataloader import DocumentToolKitManager
from chains.chain_scripts.utilities.mongodb import MongoDBToolKitManager

#model = ChatOpenAI(temperature=0, streaming=True, api_key="")

import random


def get_chain(llm: Any = None,
              connection_string: str = "mongodb://localhost:27017",
              default_database: str = None,
              default_collection: str = None):

    if connection_string:
        # Initialize the MongoDB tools
        mongo_tools = MongoDBToolKitManager(
            connection_string=connection_string,
            default_database=default_database,
            default_collection=default_collection,
        ).get_tools()
    else:
        mongo_tools = []

    # Inizializza gli strumenti per i documenti
    doc_tools = DocumentToolKitManager().get_tools()

    tools = mongo_tools + doc_tools

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/openai-tools-agent")
    #print(prompt.messages) #-- to see the prompt
    prompt.messages[0] = ("system", """
    write prompt here...
    """)

    agent = create_openai_tools_agent(
        llm.with_config({"tags": ["agent_llm"]}), tools, prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True).with_config(
        {"run_name": "Agent"}
    )
    return agent_executor
# Note: We use `pprint` to print only to depth 1, it makes it easier to see the output from a high level, before digging in.
#import pprint

#chunks = []
