import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify
import os
from alibi_detect.cd import KSDrift
from src.feature_store import RedisFeatureStore
from sklearn.preprocessing import StandardScaler
from src.logger import get_logger
from src.custom_exception import CustomException

from prometheus_client import start_http_server, Gauge, Counter



logger = get_logger(__name__)


app = Flask(__name__, template_folder = "templates")

predict_counter = Counter('predict_counter', 'Number of predictions made')
drift_count = Counter('drift_count', 'Number of times drift was detected')


MODEL_PATH = os.path.join("artifacts", "model", "random_forest_model.pkl")

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)


FEATURE_NAMES = ["Age", "Fare","Sex","Pclass","Embarked","Familysize","Isalone","HasCabin","Title","Pclass_Fare","Age_Fare"]

Feature_store = RedisFeatureStore()
scaler = StandardScaler()

def fit_scaler_on_ref_data():
    entity_ids = Feature_store.get_all_entity_ids()
    all_features = Feature_store.get_batch_features(entity_ids)
    all_features_df = pd.DataFrame.from_dict(all_features, orient='index')[FEATURE_NAMES]
    scaler.fit(all_features_df)

    return scaler.transform(all_features_df)

historical_data = fit_scaler_on_ref_data()

drift_detector = KSDrift(x_ref = historical_data,p_val=0.05)



@app.route('/')

def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        Age = float(data['Age'])
        Fare = float(data['Fare'])
        Pclass = int(data['Pclass'])
        Sex = data['Sex']
        Embarked = data['Embarked']
        Familysize = int(data['Familysize'])
        Isalone = int(data['Isalone'])
        HasCabin = int(data['HasCabin'])
        Title = data['Title']
        Pclass_Fare = float(data['Pclass_Fare'])
        Age_Fare = float(data['Age_Fare'])
        features = pd.DataFrame([[Age, Fare, Pclass, Sex, Embarked, Familysize, Isalone, HasCabin, Title, Pclass_Fare, Age_Fare]], columns=FEATURE_NAMES)

        # data drift detection
        features_scaled = scaler.transform(features)
        drift = drift_detector.predict(features_scaled)
        drift_response = drift.get('data',{})
        is_drift = drift_response.get('is_drift',None)
        if is_drift is not None and is_drift==1:
            print("Data drift detected.")
            logger.info("Data drift detected. The input data may not be consistent with the training data.")

            drift_count.inc()

        

        prediction = model.predict(features)
        predict_counter.inc()
        result = 'survived' if prediction[0] == 1 else 'not survived'

        return render_template('index.html', prediction_text=f'The prediction is {result}')
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    from flask import Response
    return Response(generate_latest(), content_type='text/plain; version=0.0.4')
if __name__ == "__main__":
    start_http_server(8000)
    app.run(debug=True, host='0.0.0.0', port=5000)

    

