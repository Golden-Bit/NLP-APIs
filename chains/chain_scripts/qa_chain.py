# from langchain_experimental.chat_models.llm_wrapper import ChatWrapper

import json
from typing import Any

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


#   class Qwen2Chat(ChatWrapper):
#    """Wrapper for Qwen2-1.5B-Instruct model."""
#
#    @property
#    def _llm_type(self) -> str:
#        return "qwen2-style"
#
#    sys_beg: str = "[INST] <<SYS>>\n"
#    sys_end: str = "\n<</SYS>>"
#    ai_n_beg: str = "[ASSISTANT] "
#    ai_n_end: str = " </s>"
#    usr_n_beg: str = "[USER] "
#    usr_n_end: str = " [/USER]"
#    usr_0_beg: str = "[USER] "
#    usr_0_end: str = " [/USER]"


# First we need a prompt that we can pass into an LLM to generate this search query
def get_chain(llm: Any, retriever: Any):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    #retriever_chain = create_history_aware_retriever(ChatWrapper(llm=llm), retriever, prompt)
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    #document_chain = create_stuff_documents_chain(ChatWrapper(llm=llm), prompt)
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    return create_retrieval_chain(retriever_chain, document_chain)


def get_chain_(llm: Any, retriever: Any):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    #retriever_chain = create_history_aware_retriever(ChatWrapper(llm=llm), retriever, prompt)
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user's questions based on the below context:\n\n{context}",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

    #document_chain = create_stuff_documents_chain(ChatWrapper(llm=llm), prompt)
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

    return create_retrieval_chain(retriever_chain, document_chain)




