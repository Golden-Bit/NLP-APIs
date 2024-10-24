import asyncio
from typing import Any
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chat_models import ChatOpenAI
from chains.chain_scripts.utilities.dataloader import DocumentToolKitManager  # Assicurati che questo percorso sia corretto
from chains.chain_scripts.utilities.mongodb import MongoDBToolKitManager


# Funzione per ottenere una catena modificata senza memoria o cronologia chat
# TODO:
#  - aggiungere eventuali documenti forniti in input (salvare temporaneamente per il processamento)
#  - aggiungere immagini fornite dall'utente (immagini vanno gestite come messaggi speciali)
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


    # Definisci il prompt con un placeholder per agent_scratchpad (richiesto dagli strumenti)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Sei un assistente utile in grado di eseguire vari compiti utilizzando strumenti."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),  # Placeholder richiesto per i passaggi intermedi
        ]
    )

    # Crea l'agente con il prompt e gli strumenti strutturati (strumenti per documenti in questo caso)
    agent = create_openai_tools_agent(llm, tools, prompt)

    # Crea l'esecutore dell'agente senza memoria o cronologia chat
    agent_executor = AgentExecutor(agent=agent, tools=tools)#, verbose=True)

    return agent_executor


"""# Esempio di esecuzione dell'agente
async def main():
    # Configura il modello di chat OpenAI
    llm = ChatOpenAI(model="gpt-4o",
                     temperature=0,
                     api_key="",
                     streaming=True)

    # Ottieni la catena (senza cronologia chat)
    chain = get_chain(llm=llm)

    # Query di esempio per l'elaborazione dei documenti
    async for token in chain.astream_events(version="v1",
        input={
            #"input": "Crea un nuovo documento di testo locale in 'test.pdf' con il contenuto 'Ciao, mondo!'. Poi leggi il documento per confermare il contenuto. Successivamente, modifica il documento per avere il contenuto 'Ciao, OpenAI!'. Leggi nuovamente il documento per confermare le modifiche. Infine, elimina il documento.",
            #"input": "Prima di tutto leggi contenuto del documento pdf 'bilancio provvisorio.pdf' usando funzione di read_local_document, ",
            "input": "estrai informazioni e fai relazione riguardo https://www.goldsolarweb.com",
            "chat_history": []
        }
    ):
        print(token, end="|")

    # Stampa la risposta dall'agente
    #print(response)
    #print("#"*120 + "\n\n")

asyncio.run(main())"""
