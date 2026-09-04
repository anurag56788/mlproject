import sys
from pathlib import Path
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

import os

@dataclass
class DataTranformationConfig:
    preprocessor_obj_file_path=os.path.join("artifact",'preprocessor.pkl')


class DataTransformation:
        def __init__(self):
            self.data_transformation_config=DataTranformationConfig()

        def get_data_transformer_object(self):
            try:
                numerical_coumns=["writing_score","reading_score"]
                categorical_columns=[
                    "gender",
                    "race_ethnicity",
                    "parental_level_of_education",
                    "lunch",
                    "test_preparation_course",
                ]

                num_pipeline=Pipeline(
                    steps=[
                        ('imputer',SimpleImputer(strategy='median')),
                        ('scaler',StandardScaler())
                    ])

                cat_pipeline=Pipeline(
                        steps=[
                            ("imputer",SimpleImputer(strategy="most_frequent")),
                            ("one_hot_encoder",OneHotEncoder()),
                            ("scaler",StandardScaler(with_mean=False))
                            ]
                        )    
                        
                logging.info("Numerical coloumns standard scaling completed")
                logging.info("categorical coloumns encoding completed")

                preprocessor=ColumnTransformer(
                    [
                        ("num_pipeline",num_pipeline,numerical_coumns),
                        ("cat_pipeline",cat_pipeline,categorical_columns)

                    ]
                )


                return preprocessor
            except Exception as e:
                raise CustomException(e,sys)


        def iniate_data_transformation(self,train_path,test_path):

            try:
                train_df=pd.read_csv(train_path)
                test_df= pd.read_csv(test_path)

                logging.info("Read train and test data completed")

                logging.info("Obtaining preprocessing object")

                preprocessing_obj=self.get_data_transformer_object()

                target_col_name="math_score"

                input_features_train_df=train_df.drop(columns=[target_col_name])
                target_features_train_df=train_df[target_col_name]

                
                input_features_test_df=test_df.drop(columns=[target_col_name])
                target_features_test_df=test_df[target_col_name]

                logging.info(
                    f"Applying the preprocessing object on training dataframe and testing dataframe"
                )

                input_features_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
                input_features_test_arr=preprocessing_obj.transform(input_features_test_df)


                train_arr=np.c_[
                    input_features_train_arr,np.array(target_features_train_df)
                ]       

                test_arr=np.c_[
                                    input_features_test_arr,np.array(target_features_test_df)
                                ]           

                save_object(
                    file_path=self.data_transformation_config.preprocessor_obj_file_path,
                    obj=preprocessing_obj
                )

                
                return (
                    train_arr,
                    test_arr,
                    self.data_transformation_config.preprocessor_obj_file_path,
                )  
            
            except  Exception as e:
                raise CustomException(e,sys)
                
                

if __name__ == "__main__":
    data_transformation = DataTransformation()
    data_transformation.iniate_data_transformation(
        os.path.join("artifact", "train.csv"),
        os.path.join("artifact", "test.csv"),
    )



