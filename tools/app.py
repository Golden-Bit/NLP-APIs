import streamlit as st
import requests

API_URL = "http://127.0.0.1:8108"

st.title("Tool Manager UI")


# Function to handle the add tool configuration form
def add_tool_config():
    with st.form("add_tool_config"):
        st.subheader("Add Tool Configuration")
        config_id = st.text_input("Config ID", value="example_tool_config")
        tool_class = st.text_input("Tool Class", value="PythonREPLTool")
        tool_kwargs = st.text_area("Tool Arguments", value='{"api_key": "your_api_key"}')
        submit = st.form_submit_button("Add", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "tool_class": tool_class,
                "tool_kwargs": eval(tool_kwargs)
            }
            response = requests.post(f"{API_URL}/add_tool_config/", json=payload)
            st.write(response.json())


# Function to handle the update tool configuration form
def update_tool_config():
    with st.form("update_tool_config"):
        st.subheader("Update Tool Configuration")
        config_id = st.text_input("Config ID", value="example_tool_config")
        tool_class = st.text_input("Tool Class", value="PythonREPLTool")
        tool_kwargs = st.text_area("Tool Arguments", value='{"api_key": "your_new_api_key"}')
        submit = st.form_submit_button("Update", use_container_width=True)

        if submit:
            payload = {
                "config_id": config_id,
                "tool_class": tool_class,
                "tool_kwargs": eval(tool_kwargs)
            }
            response = requests.put(f"{API_URL}/update_tool_config/{config_id}", json=payload)
            st.write(response.json())


# Function to handle the delete tool configuration form
def delete_tool_config():
    with st.form("delete_tool_config"):
        st.subheader("Delete Tool Configuration")
        config_id = st.text_input("Config ID", value="example_tool_config")
        submit = st.form_submit_button("Delete", use_container_width=True)

        if submit:
            response = requests.delete(f"{API_URL}/delete_tool_config/{config_id}")
            st.write(response.json())


# Function to handle the get tool configuration form
def get_tool_config():
    with st.form("get_tool_config"):
        st.subheader("Get Tool Configuration")
        config_id = st.text_input("Config ID", value="example_tool_config")
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/get_tool_config/{config_id}")
            st.write(response.json())


# Function to handle the list tool configurations form
def list_tool_configs():
    with st.form("list_tool_configs"):
        st.subheader("List Tool Configurations")
        submit = st.form_submit_button("List", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/list_tool_configs/")
            st.write(response.json())


# Function to handle the instantiate tool form
def instantiate_tool():
    with st.form("instantiate_tool"):
        st.subheader("Instantiate Tool")
        config_id = st.text_input("Config ID", value="example_tool_config")
        submit = st.form_submit_button("Instantiate", use_container_width=True)

        if submit:
            payload = {"config_id": config_id}
            response = requests.post(f"{API_URL}/instantiate_tool/", json=payload)
            st.write(response.json())


# Function to handle the remove tool instance form
def remove_tool_instance():
    with st.form("remove_tool_instance"):
        st.subheader("Remove Tool Instance")
        tool_id = st.text_input("Tool ID", value="123e4567-e89b-12d3-a456-426614174000")
        submit = st.form_submit_button("Remove", use_container_width=True)

        if submit:
            payload = {"tool_id": tool_id}
            response = requests.post(f"{API_URL}/remove_tool_instance/", json=payload)
            st.write(response.json())


# Function to handle the get tool instance form
def get_tool_instance():
    with st.form("get_tool_instance"):
        st.subheader("Get Tool Instance")
        tool_id = st.text_input("Tool ID", value="123e4567-e89b-12d3-a456-426614174000")
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/get_tool_instance/{tool_id}")
            st.write(response.json())


# Function to handle the list tool instances form
def list_tool_instances():
    with st.form("list_tool_instances"):
        st.subheader("List Tool Instances")
        submit = st.form_submit_button("List", use_container_width=True)

        if submit:
            response = requests.get(f"{API_URL}/list_tool_instances/")
            st.write(response.json())


# Function to handle the execute tool method form
def execute_tool_method():
    with st.form("execute_tool_method"):
        st.subheader("Execute Tool Method")
        tool_id = st.text_input("Tool ID", value="123e4567-e89b-12d3-a456-426614174000")
        method = st.text_input("Method", value="method_name")
        args = st.text_area("Arguments", value="[]")
        kwargs = st.text_area("Keyword Arguments", value="{}")
        submit = st.form_submit_button("Execute", use_container_width=True)

        if submit:
            payload = {
                "tool_id": tool_id,
                "method": method,
                "args": eval(args),
                "kwargs": eval(kwargs)
            }
            response = requests.post(f"{API_URL}/execute_tool_method/", json=payload)
            st.write(response.json())


# Function to handle the get tool attribute form
def get_tool_attribute():
    with st.form("get_tool_attribute"):
        st.subheader("Get Tool Attribute")
        tool_id = st.text_input("Tool ID", value="123e4567-e89b-12d3-a456-426614174000")
        attribute = st.text_input("Attribute", value="attribute_name")
        submit = st.form_submit_button("Get", use_container_width=True)

        if submit:
            payload = {
                "tool_id": tool_id,
                "attribute": attribute
            }
            response = requests.post(f"{API_URL}/get_tool_attribute/", json=payload)
            st.write(response.json())


# Tabs for each functionality
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(
    ["Add Tool Config", "Update Tool Config", "Delete Tool Config",
     "Get Tool Config", "List Tool Configs", "Instantiate Tool",
     "Remove Tool Instance", "Get Tool Instance", "List Tool Instances",
     "Execute Tool Method", "Get Tool Attribute"])

with tab1:
    add_tool_config()
with tab2:
    update_tool_config()
with tab3:
    delete_tool_config()
with tab4:
    get_tool_config()
with tab5:
    list_tool_configs()
with tab6:
    instantiate_tool()
with tab7:
    remove_tool_instance()
with tab8:
    get_tool_instance()
with tab9:
    list_tool_instances()
with tab10:
    execute_tool_method()
with tab11:
    get_tool_attribute()
