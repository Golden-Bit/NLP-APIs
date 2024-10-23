from typing import Any
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.chat_models import ChatOpenAI
from chains.chain_scripts.utilities.dataloader import DocumentToolKitManager  # Assicurati che questo percorso sia corretto

# TODO:
#  - aggiungere eventuali documenti forniti in input (salvare temporaneamente per il processamento)
#  - aggiungere immagini fornite dall'utente (immagini vanno gestite come messaggi speciali)
# Funzione per ottenere una catena modificata senza memoria o cronologia chat
def get_chain(llm: Any = None):

    # Inizializza gli strumenti per i documenti
    doc_tools = DocumentToolKitManager().get_tools()

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
    agent = create_openai_tools_agent(llm, doc_tools, prompt)

    # Crea l'esecutore dell'agente senza memoria o cronologia chat
    agent_executor = AgentExecutor(agent=agent, tools=doc_tools, verbose=True)

    return agent_executor

# Esempio di esecuzione dell'agente
if __name__ == "__main__":
    # Configura il modello di chat OpenAI
    llm = ChatOpenAI(model="gpt-4",
                     temperature=0,
                     api_key="your_api_key")

    # Ottieni la catena (senza cronologia chat)
    chain = get_chain(llm=llm)

    # Query di esempio per l'elaborazione dei documenti
    response = chain.invoke(
        {
            #"input": "Crea un nuovo documento di testo locale in 'test.pdf' con il contenuto 'Ciao, mondo!'. Poi leggi il documento per confermare il contenuto. Successivamente, modifica il documento per avere il contenuto 'Ciao, OpenAI!'. Leggi nuovamente il documento per confermare le modifiche. Infine, elimina il documento.",
            "input": "Prima di tutto leggi contenuto del documento pdf 'bilancio provvisorio.pdf' usando funzione di read_local_document, ",
            #"input": "estrai informazioni e fai relazione riguardo https://www.goldsolarweb.com",
            "chat_history": []
        }
    )

    # Stampa la risposta dall'agente
    print(response)
    print("#"*120 + "\n\n")
