import streamlit as st
import requests

titles = {
'Bacterial Blight',
'Brown Streak Disease',
'Green Mottle',
'Mosaic Disease',
'Healthy'
}

labels = [
'cassava_bacterial_blight',
'cassava_brown_streak_disease',
'cassava_green_mottle',
'cassava_mosaic_disease',
'healthy'
]

jpg = st.file_uploader("Upload a picture of one of your cassava leaves",
                       type=([".jpg", '.png']))

if jpg:

    url = "http://127.0.0.1:8000/predict"  # local
    #url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": (jpg.name, jpg, "multipart/form-data")}
    response = requests.post(url, files=files).json()

    print(type(response))
    print(response.get('cassava_bacterial_blight'))

    #col1, col2, col3, col4  = st.columns(4)

    cols = st.columns(4)
    for col, title, label in zip(cols, titles, labels):
        col.write(title)
        col.write(f'{str(round(response[label], 2) * 100)}')
        col.image(f'images/{label}.jpg')




    # col1.write('Bacterial Blight')
    # col1.image('images/cassava_bacterial_blight.jpg')
    # col1.write('Brown Streak Disease')
    # col2.image('images/cassava_brown_streak_disease.jpg')
    # col1.write('Green Mottle')
    # col3.image('images/cassava_green_mottle.jpg')
    # col1.write('Mosaic Disease')
    # col4.image('images/cassava_mosaic_disease.jpg')
