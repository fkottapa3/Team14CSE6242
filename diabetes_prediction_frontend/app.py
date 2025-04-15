
from flask import Flask, render_template, request, jsonify
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle
import pandas as pd
import joblib
import xgboost as xgb
import numpy as np

from flask_cors import CORS  # Add this line
DATA_PATH = "diabetes_prediction_dataset.csv"
# Load the voting classifier model
filename = 'scaler.pkl'
classifier = pickle.load(open(filename, 'rb'))

try:
    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = None
    
   

app = Flask(__name__)
CORS(app)  # Enable CORS for JavaScript fetch



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    global df

    data = request.get_json()
    print(data)
    
    # ====== 1. Load Models and Preprocessor ======
    preprocessor = joblib.load("scaler.pkl")
    model_xgboost = xgb.Booster()
    model_xgboost.load_model("model_xgboost.json")
    model_logreg = joblib.load("model_logreg.pkl")
    
    
    # Transforming the 'hypertension' value
    data['hypertension'] = 1 if data['hypertension'] == 'yes' else 0
    data['heart_disease'] = 1 if data['hypertension'] == 'yes' else 0
    
    # Helper function to encode smoking history
    def encode_smoking_history(smoking_status):
     return {
        "smoking_history_current": int(smoking_status == "current"),
        "smoking_history_former": int(smoking_status == "former"),
        "smoking_history_ever": int(smoking_status == "ever"),
        "smoking_history_never": int(smoking_status == "never")
    }

# Construct input_data dynamically
    smoking_encoded = encode_smoking_history(data['smoking_history'])

    
    
    input_data = pd.DataFrame([{
     "HbA1c_level": data['HbA1c_level'], 
    "blood_glucose_level":  data['blood_glucose_level'],
    "bmi":  data['bmi'],
    "age": data['age'],
    "hypertension": data['hypertension'],
    "heart_disease": data['heart_disease'],
    **smoking_encoded  # Dynamically unpack smoking history
}])

    # ====== 3. Preprocess the Input ======
    sample_scaled = preprocessor.transform(input_data)
    sample_scaled_df = pd.DataFrame(
    sample_scaled,
    columns=preprocessor.get_feature_names_out()
)

    # ====== 4. Convert to DMatrix and Predict ======
    d_sample = xgb.DMatrix(sample_scaled_df)
    xgb_prob = model_xgboost.predict(d_sample).reshape(-1, 1)

    final_prediction = model_logreg.predict(xgb_prob)
    final_probability = model_logreg.predict_proba(xgb_prob)
    
    #print("from predict functiom df", df)
    
    print("from predict functiom  printing", final_probability[0], final_prediction[0])
    
    
    #write it into csv file
    
    # Build DataFrame
    saveTocsv = pd.DataFrame([{
    "gender": 'Male',
    "age": data['age'],
    "hypertension": data['hypertension'],
    "heart_disease": data['heart_disease'],
    "smoking_history":  data['smoking_history'],
    "bmi": data['bmi'],
    "HbA1c_level": data['HbA1c_level'],
    "blood_glucose_level": data['blood_glucose_level'],
    "diabetes":  0 if final_probability[0][1] < 0.5 else 1
      }])
    
    df = pd.concat([df, saveTocsv], ignore_index=True)
    
    # Step 4: Save back to the same CSV
    df.to_csv(DATA_PATH, index=False)


    
    #prediction = round(random.uniform(0, 1), 2)
    prediction = final_probability[0][1]#round(final_proba, 2)
    return jsonify({'prediction': prediction})



@app.route('/data')
def get_chart_data():
    if df is not None:
         # Exclude rows where 'smoking_history' is 'No Info'
        filtered_df = df[df['smoking_history'] != 'No Info'].copy()

        # Select continuous features for clustering
        #features = filtered_df[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']]

        # Standardize the features (important for K-Means)
        #scaler = StandardScaler()
        #scaled_features = scaler.fit_transform(features)

        # Apply K-Means clustering
        #kmeans = KMeans(n_clusters=2, random_state=42)
        #filtered_df['cluster'] = kmeans.fit_predict(scaled_features)
        
        #print(filtered_df)

        # Convert the data to JSON format for frontend
        chart_data = filtered_df.to_dict(orient='records')
        
        # Return the data as JSON
        return jsonify(chart_data)
    
    return jsonify({'error': 'Dataset not available'})

if __name__ == '__main__':
    app.run(debug=True)
