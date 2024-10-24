import asyncio
from typing import Any

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain_core.callbacks import Callbacks
from langchain_core.prompts import ChatPromptTemplate
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
    # print(prompt.messages) -- to see the prompt

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

"""
async def main():

    chain = get_chain(llm=model)

    async for event in chain.astream_events(
            {"input": "create a cusotmer info tables about www.goldsolarweb.com"},
            version="v1",
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                    event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":
            if (
                    event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
                yield content
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")

#asyncio.run(main())"""

