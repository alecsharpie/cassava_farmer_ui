import streamlit as st
import requests
from PIL import Image
import io

titles = [
    'Bacterial Blight', 'Brown Streak Disease', 'Green Mottle',
    'Mosaic Disease', 'Healthy'
]

labels = [
    'cassava_bacterial_blight', 'cassava_brown_streak_disease',
    'cassava_green_mottle', 'cassava_mosaic_disease', 'healthy'
]
st.header("Cassava Disease Identifier")

jpg = st.sidebar.file_uploader(
    "Upload a picture of one of your cassava leaves", type=([".jpg", '.png']))

demo = st.sidebar.checkbox('use demo image', value=True)
if demo:
    image = Image.open('images/demo.jpg')

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    jpg = img_byte_arr

if jpg:

    url = "http://127.0.0.1:8000/predict"  # local
    #url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": ('image_to_identify.jpg', jpg, "multipart/form-data")}
    response = requests.post(url, files=files).json()

    st.write('Results')
    if response['healthy'] > 0.5:
        new_title = '<p style="color:Green; font-size: 24px;">Healthy Cassava</p>'
        st.markdown(new_title, unsafe_allow_html=True)
    else:
        new_title = '<p style="color:Red; font-size: 24px;">Sick Cassava</p>'
        st.markdown(new_title, unsafe_allow_html=True)

    cols = st.columns(4)
    predictions = list(response.values())[:-1]
    titles_sort = [
        x for _, x in sorted(zip(predictions, titles[:-1]), reverse=True)
    ]
    labels_sort = [
        x for _, x in sorted(zip(predictions, labels[:-1]), reverse=True)
    ]
    predictions_sort = sorted(predictions, reverse=True)
    for col, pred, title, label in zip(cols, predictions_sort, titles_sort,
                                       labels_sort):
        col.write(title)
        col.markdown(
            f"<p style='color:White; font-size: 24px;'>{str(round(pred * 100, 1))}%</p>",
            unsafe_allow_html=True)
        col.image(f'images/{label}.jpg')
        #new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'
        #col.markdown(new_title, unsafe_allow_html=True)

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
