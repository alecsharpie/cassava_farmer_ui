import streamlit as st
import requests
from PIL import Image
import io

titles = [
'Bacterial Blight',
'Brown Streak Disease',
'Green Mottle',
'Mosaic Disease',
'Healthy'
]

labels = [
'cassava_bacterial_blight',
'cassava_brown_streak_disease',
'cassava_green_mottle',
'cassava_mosaic_disease',
'healthy'
]
st.header("Cassava Disease Identifier")



jpg = st.sidebar.file_uploader("Upload a picture of one of your cassava leaves",
                       type=([".jpg", '.png']))


demo = st.sidebar.checkbox('use demo image', value=True)
if demo:
    image = Image.open('images/demo.jpg')

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    jpg = img_byte_arr

print(jpg)
print(type(jpg))
#print(jpg.__dict__)



if jpg:

    url = "http://127.0.0.1:8000/predict"  # local
    #url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": ('image_to_identify.jpg', jpg, "multipart/form-data")}
    response = requests.post(url, files=files).json()
    st.write('Your Results')
    cols = st.columns(4)
    for col, title, label in zip(cols, titles, labels):
        col.write(title)
        col.write(f'{str(round(response[label] * 100, 1))}%')
        col.image(f'images/{label}.jpg')

else:
    response = {
        'cassava_bacterial_blight': '?',
        'cassava_brown_streak_disease': '?',
        'cassava_green_mottle': '?',
        'cassava_mosaic_disease': '?',
        'healthy': '?'
    }
    st.write('Upload an image for your results...')
    cols = st.columns(4)
    for col, title, label in zip(cols, titles, labels):
        col.write(title)
        col.write(f'{response[label]}%')
        col.image(f'images/{label}.jpg')
