import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8106/llm"

st.set_page_config(layout="wide")

st.title("LLM Model Management and Inference")

# Funzione per configurare un nuovo modello
def configure_model():
    with st.form("configure_model_form"):
        st.subheader("Configure Model")
        config_id = st.text_input("Config ID", value="example_configuration")
        model_id = st.text_input("Model ID", value="example_model")
        model_type = st.selectbox("Model Type", ["openai", "vllm"])
        model_kwargs = st.text_area("Model Kwargs (JSON format)", value='{"temperature": 0.7}')
        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted:
            model_kwargs = json.loads(model_kwargs)
            data = {
                "config_id": config_id,
                "model_id": model_id,
                "model_type": model_type,
                "model_kwargs": model_kwargs
            }
            response = requests.post(f"{API_URL}/configure_model/", json=data)
            st.write(response.json())

# Funzione per caricare un modello
def load_model():
    with st.form("load_model_form"):
        st.subheader("Load Model")
        config_id = st.text_input("Config ID")
        submitted = st.form_submit_button("Load Model", use_container_width=True)

        if submitted:
            response = requests.post(f"{API_URL}/load_model/{config_id}")
            st.write(response.json())

# Funzione per scaricare un modello
def unload_model():
    with st.form("unload_model_form"):
        st.subheader("Unload Model")
        model_id = st.text_input("Model ID")
        submitted = st.form_submit_button("Unload Model", use_container_width=True)

        if submitted:
            response = requests.post(f"{API_URL}/unload_model/{model_id}")
            st.write(response.json())

# Funzione per eseguire un'inferenza
def inference():
    with st.form("inference_form"):
        st.subheader("Model Inference")
        model_id = st.text_input("Model ID")
        prompt = st.text_input("Prompt", value="What is the capital of France?")
        inference_kwargs = st.text_area("Inference Kwargs (JSON format)", value='{"max_tokens": 50}')
        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted:
            inference_kwargs = json.loads(inference_kwargs)
            data = {
                "model_id": model_id,
                "prompt": prompt,
                "inference_kwargs": inference_kwargs
            }
            response = requests.post(f"{API_URL}/inference/", json=data)
            st.write(response.json())

# Funzione per eseguire un'inferenza in streaming
def streaming_inference():
    with st.form("streaming_inference_form"):
        st.subheader("Streaming Inference")
        model_id = st.text_input("Model ID")
        prompt = st.text_input("Prompt", value="What is the capital of France?")
        inference_kwargs = st.text_area("Inference Kwargs (JSON format)", value='{"max_tokens": 50}')
        stream_only_content = st.checkbox("Stream Only Content", value=False)
        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted:
            inference_kwargs = json.loads(inference_kwargs)
            data = {
                "model_id": model_id,
                "prompt": prompt,
                "inference_kwargs": inference_kwargs,
                "stream_only_content": stream_only_content
            }
            response = requests.post(f"{API_URL}/streaming_inference/", json=data, stream=True)

            for line in response.iter_lines():
                if line:
                    st.write(line.decode('utf-8'))

# Funzione per elencare tutte le configurazioni dei modelli
def list_configurations():
    st.subheader("List Model Configurations")
    response = requests.get(f"{API_URL}/configurations/")
    st.write(response.json())

# Funzione per ottenere una configurazione specifica
def get_configuration():
    with st.form("get_configuration_form"):
        st.subheader("Get Model Configuration")
        config_id = st.text_input("Config ID")
        submitted = st.form_submit_button("Get Configuration", use_container_width=True)

        if submitted:
            response = requests.get(f"{API_URL}/configuration/{config_id}")
            st.write(response.json())

# Funzione per cancellare una configurazione specifica
def delete_configuration():
    with st.form("delete_configuration_form"):
        st.subheader("Delete Model Configuration")
        config_id = st.text_input("Config ID")
        submitted = st.form_submit_button("Delete Configuration", use_container_width=True)

        if submitted:
            response = requests.delete(f"{API_URL}/configuration/{config_id}")
            st.write(response.json())

# Funzione per elencare i modelli caricati
def list_loaded_models():
    st.subheader("List Loaded Models")
    response = requests.get(f"{API_URL}/loaded_models/")
    st.write(response.json())

# Interfaccia principale con le sezioni raggruppate in tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Configure Model", "Load Model", "Unload Model", "Inference", "Streaming Inference", "List Configurations", "Get Configuration", "Delete Configuration", "List Loaded Models"])

with tab1:
    configure_model()
with tab2:
    load_model()
with tab3:
    unload_model()
with tab4:
    inference()
with tab5:
    streaming_inference()
with tab6:
    list_configurations()
with tab7:
    get_configuration()
with tab8:
    delete_configuration()
with tab9:
    list_loaded_models()
