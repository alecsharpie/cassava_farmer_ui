import streamlit as st
import requests

jpg = st.file_uploader("Upload a breast cancer histology image",
                       type=([".jpg", '.png']))

if jpg:
    # save png
    #myuuid = uuid.uuid4()
    #IMG1 = f"{myuuid}.png"

    url = "http://127.0.0.1:8000/predict"  # local
    #url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (jpg.name, jpg, "multipart/form-data")}
    response = requests.post(url, files=files).json()
    st.write(response)

    col1, col2, col3, col4  = st.columns(4)

    col1.image()
