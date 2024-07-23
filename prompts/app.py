import streamlit as st
import requests

API_URL = "http://127.0.0.1:8107"

st.set_page_config(layout="wide")
st.title("Prompt Manager UI")


# Function to handle the add prompt configuration form
def add_prompt_config():
    with st.form("add_prompt_config"):
        st.subheader("Add Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_prompt_config")
        template = st.text_area("Template", value="Tell me a {adjective} joke about {content}.")
        type_ = st.selectbox("Type", ["string", "chat"])
        variables = st.text_input("Variables", value="adjective, content")
        submit = st.form_submit_button("Add", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "template": template,
                "type": type_,
                "variables": variables.split(", ")
            }
            response = requests.post(f"{API_URL}/add_prompt_config/", json=payload)
            st.write(response.json())


# Function to handle the add chat prompt configuration form
def add_chat_prompt_config():
    with st.form("add_chat_prompt_config"):
        st.subheader("Add Chat Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_chat_prompt_config")
        messages = st.text_area("Messages", value='[{"role": "system", "content": "You are a helpful AI bot. Your name is {name}."}, '
                                                '{"role": "human", "content": "Hello, how are you doing?"}, '
                                                '{"role": "ai", "content": "I\'m doing well, thanks!"}, '
                                                '{"role": "human", "content": "{user_input}"}]')
        variables = st.text_input("Variables", value="name, user_input")
        submit = st.form_submit_button("Add", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "messages": eval(messages),
                "variables": variables.split(", ")
            }
            response = requests.post(f"{API_URL}/add_chat_prompt_config/", json=payload)
            st.write(response.json())


# Function to handle the update prompt configuration form
def update_prompt_config():
    with st.form("update_prompt_config"):
        st.subheader("Update Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_prompt_config")
        template = st.text_area("Template", value="Tell me a {adjective} story about {content}.")
        type_ = st.selectbox("Type", ["string", "chat"])
        variables = st.text_input("Variables", value="adjective, content")
        submit = st.form_submit_button("Update", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "template": template,
                "type": type_,
                "variables": variables.split(", ")
            }
            response = requests.put(f"{API_URL}/update_prompt_config/{config_id}", json=payload)
            st.write(response.json())


# Function to handle the update chat prompt configuration form
def update_chat_prompt_config():
    with st.form("update_chat_prompt_config"):
        st.subheader("Update Chat Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_chat_prompt_config")
        messages = st.text_area("Messages", value='[{"role": "system", "content": "You are a helpful AI bot. Your name is {name}."}, '
                                                '{"role": "human", "content": "Hello, how are you doing?"}, '
                                                '{"role": "ai", "content": "I\'m doing well, thanks!"}, '
                                                '{"role": "human", "content": "{user_input}"}]')
        variables = st.text_input("Variables", value="name, user_input")
        submit = st.form_submit_button("Update", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "messages": eval(messages),
                "variables": variables.split(", ")
            }
            response = requests.put(f"{API_URL}/update_chat_prompt_config/{config_id}", json=payload)
            st.write(response.json())


# Function to handle the delete prompt configuration form
def delete_prompt_config():
    with st.form("delete_prompt_config"):
        st.subheader("Delete Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_prompt_config")
        submit = st.form_submit_button("Delete", use_container_width=True)

        if submit:
            response = requests.delete(f"{API_URL}/delete_prompt_config/{config_id}")
            st.write(response.json())


# Function to handle the delete chat prompt configuration form
def delete_chat_prompt_config():
    with st.form("delete_chat_prompt_config"):
        st.subheader("Delete Chat Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_chat_prompt_config")
        submit = st.form_submit_button("Delete", use_container_width=True)

        if submit:
            response = requests.delete(f"{API_URL}/delete_chat_prompt_config/{config_id}")
            st.write(response.json())


# Function to handle the get prompt configuration form
def get_prompt_config():
    with st.form("get_prompt_config"):
        st.subheader("Get Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_prompt_config")
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/get_prompt_config/{config_id}")
            st.write(response.json())


# Function to handle the get chat prompt configuration form
def get_chat_prompt_config():
    with st.form("get_chat_prompt_config"):
        st.subheader("Get Chat Prompt Configuration")
        config_id = st.text_input("Config ID", value="example_chat_prompt_config")
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/get_chat_prompt_config/{config_id}")
            st.write(response.json())


# Function to handle listing all prompt configurations
def list_prompt_configs():
    st.subheader("List Prompt Configurations")
    response = requests.get(f"{API_URL}/list_prompt_configs/")
    if response.status_code == 200:
        configs = response.json()
        for config in configs:
            st.json(config)
    else:
        st.write("Error: Unable to fetch prompt configurations.")


# Function to handle listing all chat prompt configurations
def list_chat_prompt_configs():
    st.subheader("List Chat Prompt Configurations")
    response = requests.get(f"{API_URL}/list_chat_prompt_configs/")
    if response.status_code == 200:
        configs = response.json()
        for config in configs:
            st.json(config)
    else:
        st.write("Error: Unable to fetch chat prompt configurations.")


# Function to handle the instantiate prompt form
def get_prompt():
    with st.form("get_prompt"):
        st.subheader("Get Prompt")
        config_id = st.text_input("Config ID", value="example_prompt_config")
        variables = st.text_area("Variables", value='{"adjective": "funny", "content": "chickens"}')
        partial = st.checkbox("Partial", value=False)
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "variables": eval(variables),
                "partial": partial
            }
            response = requests.post(f"{API_URL}/get_prompt/", json=payload)
            st.write(response.json())


# Function to handle the instantiate chat prompt form
def get_chat_prompt():
    with st.form("get_chat_prompt"):
        st.subheader("Get Chat Prompt")
        config_id = st.text_input("Config ID", value="example_chat_prompt_config")
        variables = st.text_area("Variables", value='{"name": "Bob", "user_input": "What is your name?"}')
        partial = st.checkbox("Partial", value=False)
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "variables": eval(variables),
                "partial": partial
            }
            response = requests.post(f"{API_URL}/get_chat_prompt/", json=payload)
            st.write(response.json())


# Tabs for each functionality
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(
    ["Add Prompt Config", "Add Chat Prompt Config", "Update Prompt Config",
     "Update Chat Prompt Config", "Delete Prompt Config", "Delete Chat Prompt Config",
     "Get Prompt Config", "Get Chat Prompt Config", "Get Prompt", "Get Chat Prompt",
     "List Prompt Configs", "List Chat Prompt Configs"])

with tab1:
    add_prompt_config()
with tab2:
    add_chat_prompt_config()
with tab3:
    update_prompt_config()
with tab4:
    update_chat_prompt_config()
with tab5:
    delete_prompt_config()
with tab6:
    delete_chat_prompt_config()
with tab7:
    get_prompt_config()
with tab8:
    get_chat_prompt_config()
with tab9:
    get_prompt()
with tab10:
    get_chat_prompt()
with tab11:
    list_prompt_configs()
with tab12:
    list_chat_prompt_configs()
