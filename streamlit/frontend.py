import requests
from PIL import Image

import streamlit as st



# layout of webpage
st.set_page_config(
    page_title='House Price',
    layout='centered',
    page_icon=None,
    initial_sidebar_state='auto',
)

#image for webpage
IMAGE_PATH = 'images/house.jpg'



def predict(row, feats_col):
    '''
    Sends a prediction request to the Flask API endpoints and returns the predicted listed price
    '''
    
    inputs = dict(zip(feats_col,row))
    
    
    
    # Send to the API
    url = "http://prediction_service:9696/predict"
    response = requests.post(url, json=inputs)

    # Leave for now exception here
    if response.status_code == 200:  # pylint: disable=no-else-return
        return response.json()
    else:
        raise Exception(f"Status: {response.status_code}")

    

def app():
    '''
    The actual app
    '''

    st.markdown(
        "<h2 style='text-align: center; color: Grey;'>Predict House Price</h2>",
        unsafe_allow_html=True,
    )

    col1 ,mid, col2 = st.columns([40,5,40])

    image = Image.open(IMAGE_PATH)
    with col1:
        st.markdown("""***""")
        st.image(image)
        st.markdown("""***""")
    with col2:

        # Get the input from user for prediction with a form

    
        with st.form("predict"):
            age = st.slider(
                "X2 house age",
        
            )
            distance = st.slider(
                "X3 distance to the nearest MRT station",
                min_value=1, max_value=10000
            )
            stores = st.slider(
                "X4 number of convenience stores",
        
            )
            latitude = st.slider(
                "X5 latitude",
    
            )
            longitude = st.slider(
                "X6 longitude",

            )
            
            feat_cols = [
                "X2 house age",
                    "X3 distance to the nearest MRT station",
                    "X4 number of convenience stores",
                    "X5 latitude",
                    "X6 longitude",
            ]

            row = [
                age,
                distance,
                stores,
                latitude,
                longitude,
            ]

            st.text("\n")

            if st.form_submit_button('Predict Price'):
                result_json = predict(row, feat_cols)
                result = result_json['price']

                st.write(f'The house should be listed around: `{result * 10000}$` Naira')


if __name__ == '__main__':
    app()