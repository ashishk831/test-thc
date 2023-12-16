import gradio as gr
import pickle
import pandas as pd
import glob
import os
import joblib


def get_latest_folder(directory):
    folders = [folder for folder in glob.glob(os.path.join(directory, '*')) if os.path.isdir(folder)]
    if not folders:
        return None
    return max(folders, key=os.path.getctime)

def load_pickle_from_latest_folder(directory, pickle_filename):
    latest_folder = get_latest_folder(directory)
    if latest_folder is None:
        print("No folders found in the specified directory.")
        return None

    pickle_path = os.path.join(latest_folder, pickle_filename)

    if not os.path.exists(pickle_path):
        print(f"No pickle file '{pickle_filename}' found in the latest folder.")
        return None

    with open(pickle_path, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
        return data

# Example usage
directory_path = 'model.pkl'
pickle_filename = 'model.pkl'

def Model_Prediction(x):
    return x[::-1]


def Model_Monitoring(x):
    return np.fliplr(x)

model = joblib.load('/home/unibash/G3/B/SALE_CNV_OPT/model.pkl')
with gr.Blocks() as demo:
    gr.Markdown("Sales Optimization Model.")
    with gr.Tab("Model Prediction"):
        def predict(ad_id, age, gender, interest, Impressions, Clicks, Spent, Total_Conversion, CTR, CPC):
            if gender == 'Male':
                gender = 0
            else:
                gender = 1
            ad_id = int(ad_id)
            age = int(age)
            gender = int(gender)
            interest = int(interest)
            Impressions = int(Impressions)
            Clicks = int(Clicks)
            Spent = float(Spent)
            Total_Conversion = int(Total_Conversion)
            CTR = float(CTR)
            CPC = float(CPC)

        # Create a dictionary with input values
            input_data = {
                'ad_id': [ad_id],
                'age': [age],
                'gender': [gender],
                'interest': [interest],
                'Impressions': [Impressions],
                'Clicks': [Clicks],
                'Spent': [Spent],
                'Total_Conversion': [Total_Conversion],
                'CTR': [CTR],
                'CPC': [CPC]
            }
    # Create a DataFrame from the input data
            input_df = pd.DataFrame(input_data)

    # Make prediction
            prediction = model.predict(input_df)
    # Return the predicted value for Approved_Conversion
            return round(prediction[0])
        
        inputs = [
        gr.Number(label='Ad ID', info='Enter the advertisement ID',minimum= 0),
        gr.Number(label='Age', info='Enter the target age group',minimum= 0),
        #gr.Number(label='Gender', info='Enter the gender (0 for female, 1 for male)',minimum= 0,maximum=1),
        gr.Radio(["Male", "Female"], label="Gender", info="Enter the gender"),
        gr.Dropdown(label='Interest', choices=[2, 7, 10, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 
                        26, 27, 28, 29, 30, 31, 32, 36, 63, 64, 65, 66, 100, 101, 102, 
                        103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114], 
                        info='Select the target audience interest'),
        gr.Number(label='Impressions', info='Enter the number of impressions',minimum= 0),
        gr.Number(label='Clicks', info='Enter the number of clicks',minimum= 0),
        gr.Number(label='Spent', info='Enter the amount spent on the ad',minimum= 0),
        gr.Number(label='Total Conversion', info='Enter the total conversion count',minimum= 0),
        gr.Number(label='CTR', info='Enter the Click-Through Rate',minimum= 0),
        gr.Number(label='CPC', info='Enter the Cost Per Click',minimum= 0)
    ]
        # Create Gradio interface with improved styling
        iface = gr.Interface(
        fn=predict,
        inputs=inputs,
        outputs=gr.Textbox(type='text', label='Predicted Approved_Conversion', placeholder='Prediction will appear here')
    )

    with gr.Tab("Model Monitoring"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Flip")    

    #text_button.click(fn=predict, inputs=inputs, outputs=gr.Textbox(type='text', label='Predicted Approved_Conversion', placeholder='Prediction will appear here'))
    image_button.click(Model_Monitoring, inputs=image_input, outputs=image_output)

demo.launch()
