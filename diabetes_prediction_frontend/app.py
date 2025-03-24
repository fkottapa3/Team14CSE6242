
from flask import Flask, render_template, request, jsonify
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd
from flask_cors import CORS  # Add this line
DATA_PATH = "diabetes_prediction_dataset.csv"

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
    
    data = request.get_json()
    print(data)
    
    print("df", df)
    
    prediction = round(random.uniform(0, 1), 2)
    return jsonify({'prediction': prediction})



@app.route('/data')
def get_chart_data():
    if df is not None:
         # Exclude rows where 'smoking_history' is 'No Info'
        filtered_df = df[df['smoking_history'] != 'No Info'].copy()

        # Select continuous features for clustering
        features = filtered_df[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']]

        # Standardize the features (important for K-Means)
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=2, random_state=42)
        filtered_df['cluster'] = kmeans.fit_predict(scaled_features)
        
        print(filtered_df)

        # Convert the data to JSON format for frontend
        chart_data = filtered_df.to_dict(orient='records')
        
        # Return the data as JSON
        return jsonify(chart_data)
    
    return jsonify({'error': 'Dataset not available'})

if __name__ == '__main__':
    app.run(debug=True)
