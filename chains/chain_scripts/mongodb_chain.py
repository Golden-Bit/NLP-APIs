from typing import Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from chains.chain_scripts.utilities.mongodb import MongoDBToolKitManager


# Function to get a modified chain without memory or chat history
def get_chain(llm: Any = None,
              connection_string: str = "mongodb://localhost:27017",
              default_database: str = None,
              default_collection: str = None):

    # Initialize the MongoDB tools
    mongo_tools = MongoDBToolKitManager(
        connection_string=connection_string,
        default_database=default_database,
        default_collection=default_collection,
    ).get_tools()

    # Define the prompt with a placeholder for the agent_scratchpad (required by tools)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant capable of performing various tasks using tools."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),  # Required placeholder for intermediate steps
        ]
    )

    # Create the agent with the prompt and structured tools (MongoDB tools in this case)
    agent = create_openai_tools_agent(llm, mongo_tools, prompt)

    # Create the agent executor without memory or chat history
    agent_executor = AgentExecutor(agent=agent, tools=mongo_tools, verbose=True)

    return agent_executor


# Example of agent execution
if __name__ == "__main__":
    # Configure the OpenAI chat model
    llm = ChatOpenAI(model="gpt-4o",
                     temperature=0,
                     api_key="your_api_key")

    # Get the chain (without chat history)
    chain = get_chain(llm=llm)

    # Example query for inserting a document into MongoDB
    response = chain.invoke(
        {
            "input": "Insert a new document into MongoDB in the 'users' collection with a random name and age. subito "
                     "dopo l'inserimento usa struemnto e leggi subito il dato dal db. infine elimina il docuemnto e "
                     "duqnue prova a rivere tutti i docuemnti. quando devi richiamarti i docuemti per le query non "
                     "usare il campo _id, invece crea un campo data_id personalizzato",
            "chat_history": []
        },
        {"configurable": {"session_id": "unused"}},
    )

    # Print the response from the agent
    print(response)
    print("#"*120 + "\n\n")
