import streamlit as st
import pandas as pd

from modules.ml import Prediction_5000_data_with_data_frame_v1_0 as p
from modules.ml import prediction as pred
def show_PredictivePerformance():
    # st.set_page_config(
    #     page_title="Predictive Performance",
    #     page_icon="🤖",
    #     layout='wide',
    # )

    st.subheader('🤖  Predictive Performance')

    result_vol_df = p.get_vol_prediction_for_6month('Production Volume (units)')
    result_rev_df = p.get_rev_prediction_for_6month('Revenue ($)') #pd.read_csv('C:\\compny project\\form-factory-main\\form-factory-main\\modules\\ml\\output_results.csv')
    result_foam_df = p.get_foam_prediction_for_6month('Foam Density')

    #print(result_df.dtypes)
    pred.predictionPage(result_vol_df,result_rev_df,result_foam_df)
