from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from src.feature_store import RedisFeatureStore
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
import pickle

logger = get_logger(__name__)
class ModelTraining:
    def __init__(self, feature_store: RedisFeatureStore, model_save_path = "artifacts/model"):
        self.feature_store = feature_store
        self.model_save_path = model_save_path
        self.model = None

        os.makedirs(self.model_save_path, exist_ok=True)
        logger.info("ModelTraining initialized with feature store and model save path.")
    def load_data_from_redis(self,entity_ids):
        try:
            logger.info("Loading data from Redis feature store.")
            data = []
            for entity_id in entity_ids:
                features = self.feature_store.get_feature(entity_id)
                if features is not None:
                    data.append(features)
        
            logger.info("Data loaded successfully from Redis.")
            return data
        except Exception as e:
            logger.error(f"Error loading data from Redis: {e}")
            raise CustomException(f"Error loading data from Redis: {e}")
    def prepare_data(self):
        try:
            entity_ids = self.feature_store.get_all_entity_ids()

            train_entity_ids, test_entity_ids = train_test_split(entity_ids, test_size=0.2, random_state=42)
            train_data = self.load_data_from_redis(train_entity_ids)
            test_data = self.load_data_from_redis(test_entity_ids)

            train_df = pd.DataFrame(train_data)
            test_df = pd.DataFrame(test_data)
            X_train = train_df.drop(columns=['Survived'])
            y_train = train_df['Survived']
            X_test = test_df.drop(columns=['Survived'])
            y_test = test_df['Survived']

            logger.info("Data prepared for training and testing.")
            return X_train, y_train, X_test, y_test
        except Exception as e:
            logger.error(f"Error preparing data: {e}")
            raise CustomException(f"Error preparing data: {e}")
    def hyperparameter_tuning(self, X_train, y_train):
        try:
            param_distributions = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            }
            rf = RandomForestClassifier(random_state=42)
            random_search = RandomizedSearchCV(rf, param_distributions, n_iter=10, cv=3, scoring='accuracy', random_state=42)
            random_search.fit(X_train, y_train)
            logger.info("Hyperparameter tuning completed successfully.")
            return random_search.best_estimator_
        except Exception as e:
            logger.error(f"Error in hyperparameter tuning: {e}")
            raise CustomException(f"Error in hyperparameter tuning: {e}")
    def train_evaluate_model(self,X_train, y_train, X_test, y_test):
        try:
            logger.info("Starting model training and evaluation.")
            best_rf = self.hyperparameter_tuning(X_train, y_train)

            y_pred = best_rf.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            self.save_model(best_rf)
            logger.info(f"Model trained with accuracy: {accuracy:.2f}")
        except Exception as e:
            logger.error(f"Error in model training and evaluation: {e}")
            raise CustomException(f"Error in model training and evaluation: {e}")
        
    def save_model(self, model):
        try:
            model_filename = f"{self.model_save_path}/random_forest_model.pkl"
            with open(model_filename, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Model saved successfully at {model_filename}.")

        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise CustomException(f"Error saving model: {e}")
    def run(self):
        try:
            logger.info("Starting model training pipeline.")
            X_train, y_train, X_test, y_test = self.prepare_data()
            self.train_evaluate_model(X_train, y_train, X_test, y_test)
            logger.info("Model training pipeline completed successfully.")
        except Exception as e:
            logger.error(f"Error in model training pipeline: {e}")
            raise CustomException(f"Error in model training pipeline: {e}")
if __name__ == "__main__":
    feature_store = RedisFeatureStore()
    model_trainer = ModelTraining(feature_store)
    model_trainer.run()
    