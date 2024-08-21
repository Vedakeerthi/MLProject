import sys
from dataclasses import dataclass
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src import exception, logger, utils
@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path = os.path.join('artificats','preprocessor.pkl')

class DataTranformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()
        
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['writing_score','reading_score']
            categorical_columns = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            
            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            logger.logging.info('numerical columns encoding completed')
            
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('scaler',StandardScaler())
                ]
            )
            
            logger.logging.info('categorical columns encoding completed')
            
            preprocessor = ColumnTransformer([
                ('num_pipeline',num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipeline,categorical_columns)
            ])

            return preprocessor
        
        except Exception as e:
            raise exception.CustomException(e,sys)
            
    def initiate_data_transformation(self, train_path, test_path):
        
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logger.logging.info("Reading train and test data...")
            logger.logging.info('Obtaining Preprocessing object')
            
            preprocessing_obj = self.get_data_transformer_object()
            target_column_name = 'math_score'
            
            input_feature_train_df = train_df.drop(target_column_name,axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]
            logger.logging.info('Applying preprocessing object on training and test dataframe')
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            training_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            testing_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            logger.logging.info('Saved Preprocessing object.')
            
            utils.save_object(file_path=self.data_tranformation_config.preprocessor_ob_file_path,
                        obj= preprocessing_obj)
            
            return(training_arr, testing_arr, self.data_tranformation_config.preprocessor_ob_file_path)
            
        except Exception as e:
            raise exception.CustomException(e,sys)