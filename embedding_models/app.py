import streamlit as st
import requests

base_url = "http://127.0.0.1:8104"

def configure_model_form():
    with st.form(key='configure_model_form'):
        st.header("Configure Embedding Model")
        config_id = st.text_input("Config ID", "example_embedding_config")
        model_id = st.text_input("Model ID", "example_model")
        model_class = st.selectbox("Model Class", ["HuggingFaceEmbeddings", "OpenAIEmbeddings"])
        model_kwargs = st.text_area("Model Kwargs (JSON format)", '{"model_name": "distilbert-base-uncased"}')
        submit_button = st.form_submit_button(label='Configure Model')

        if submit_button:
            data = {
                "config_id": config_id,
                "model_id": model_id,
                "model_class": model_class,
                "model_kwargs": eval(model_kwargs)
            }
            response = requests.post(f"{base_url}/configure_embedding_model/", json=data)
            st.write(response.json())

def load_model_form():
    with st.form(key='load_model_form'):
        st.header("Load Embedding Model")
        config_id = st.text_input("Config ID", "example_embedding_config")
        submit_button = st.form_submit_button(label='Load Model')

        if submit_button:
            response = requests.post(f"{base_url}/load_embedding_model/{config_id}")
            st.write(response.json())

def unload_model_form():
    with st.form(key='unload_model_form'):
        st.header("Unload Embedding Model")
        model_id = st.text_input("Model ID", "example_model")
        submit_button = st.form_submit_button(label='Unload Model')

        if submit_button:
            response = requests.post(f"{base_url}/unload_embedding_model/{model_id}")
            st.write(response.json())

def inference_form():
    with st.form(key='inference_form'):
        st.header("Perform Inference")
        model_id = st.text_input("Model ID", "example_model")
        texts = st.text_area("Texts (separated by newline)", "Hello world\nHow are you?")
        inference_kwargs = st.text_area("Inference Kwargs (JSON format)", "{}")
        submit_button = st.form_submit_button(label='Perform Inference')

        if submit_button:
            data = {
                "model_id": model_id,
                "texts": texts.split("\n"),
                "inference_kwargs": eval(inference_kwargs)
            }
            response = requests.post(f"{base_url}/embedding_inference/", json=data)
            st.write(response.json())

def execute_method_form():
    with st.form(key='execute_method_form'):
        st.header("Execute Model Method")
        model_id = st.text_input("Model ID", "example_model")
        method_name = st.text_input("Method Name", "generate")
        args = st.text_area("Arguments (JSON format)", "[]")
        kwargs = st.text_area("Keyword Arguments (JSON format)", "{}")
        submit_button = st.form_submit_button(label='Execute Method')

        if submit_button:
            data = {
                "model_id": model_id,
                "method_name": method_name,
                "args": eval(args),
                "kwargs": eval(kwargs)
            }
            response = requests.post(f"{base_url}/execute_embedding_method/", json=data)
            st.write(response.json())

def get_attribute_form():
    with st.form(key='get_attribute_form'):
        st.header("Get Model Attribute")
        model_id = st.text_input("Model ID", "example_model")
        attribute_name = st.text_input("Attribute Name", "attribute_name")
        submit_button = st.form_submit_button(label='Get Attribute')

        if submit_button:
            data = {
                "model_id": model_id,
                "attribute_name": attribute_name
            }
            response = requests.post(f"{base_url}/get_embedding_attribute/", json=data)
            st.write(response.json())

def list_loaded_models():
    st.header("List Loaded Models")
    if st.button("List Models"):
        response = requests.get(f"{base_url}/list_loaded_embedding_models/")
        st.write(response.json())

def get_model_config_form():
    with st.form(key='get_model_config_form'):
        st.header("Get Model Configuration")
        config_id = st.text_input("Config ID", "example_embedding_config")
        submit_button = st.form_submit_button(label='Get Config')

        if submit_button:
            response = requests.get(f"{base_url}/embedding_model_config/{config_id}")
            st.write(response.json())

def delete_model_config_form():
    with st.form(key='delete_model_config_form'):
        st.header("Delete Model Configuration")
        config_id = st.text_input("Config ID", "example_embedding_config")
        submit_button = st.form_submit_button(label='Delete Config')

        if submit_button:
            response = requests.delete(f"{base_url}/embedding_model_config/{config_id}")
            st.write(response.json())

def main():
    st.title("Embedding Model Manager")

    tabs = st.tabs(["Configure Model", "Load Model", "Unload Model", "Inference", "Execute Method", "Get Attribute", "List Loaded Models", "Get Model Config", "Delete Model Config"])

    with tabs[0]:
        configure_model_form()

    with tabs[1]:
        load_model_form()

    with tabs[2]:
        unload_model_form()

    with tabs[3]:
        inference_form()

    with tabs[4]:
        execute_method_form()

    with tabs[5]:
        get_attribute_form()

    with tabs[6]:
        list_loaded_models()

    with tabs[7]:
        get_model_config_form()

    with tabs[8]:
        delete_model_config_form()

if __name__ == "__main__":
    main()
