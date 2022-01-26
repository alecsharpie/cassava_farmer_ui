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

st.markdown("""---""")

jpg = st.sidebar.file_uploader(
    "Upload a picture of one of your cassava leaves", type=([".jpg", '.png']))

if not jpg:
    demo = st.sidebar.radio("Use a demo image", ('Healthy Demo', 'Unhealthy Demo'))

    if demo == 'Unhealthy Demo':
        image = Image.open('images/unhealthy_demo.jpg')
    elif demo == 'Healthy Demo':
        image = Image.open('images/healthy_demo.jpg')

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    jpg = img_byte_arr

if jpg:
    st.sidebar.image(jpg, caption = 'Current Selection')

if jpg:
    url = "http://127.0.0.1:8000/predict"  # local
    #url = "https://idc-mvds5dflqq-ew.a.run.app/annotate"  # production
    files = {"file": ('image_to_identify.jpg', jpg, "multipart/form-data")}
    response = requests.post(url, files=files).json()
    if response['healthy'] > 0.5:
        new_title = '<span style="color:White; font-size: 24px;">Result:   </span><span style="color:Green; font-size: 26px;">Healthy Cassava</span>'
        st.markdown(new_title, unsafe_allow_html=True)
    else:
        new_title = '<span style="color:White; font-size: 24px;">Result:   </span><span style="color:Red; font-size: 26px;">Sick Cassava</span>'
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
        col.markdown(
            f"<p style='color:White; font-size: 24px;'>{str(round(pred * 100, 1))}%</p>",
            unsafe_allow_html=True)
        col.write(title)
        col.image(f'images/{label}.jpg', caption = f"Example of {title}")

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
