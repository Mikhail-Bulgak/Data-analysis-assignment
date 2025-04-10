import pandas as pd
import numpy as np
import streamlit as st 

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression

st.write("""
# Прогноз определения длины и ширины шва
Приложение создано на основе имеющихся данных
""")

st.sidebar.header('Пользовательские параметры')

def user_input_features():
    param_iw = st.sidebar.slider('Величина сварочного тока (IW)', 40.0, 50.0, 45.0)
    param_if = st.sidebar.slider('Ток фокусировки электронного пучка (IF)', 130.0, 150.0, 140.0)
    param_vw = st.sidebar.slider('Скорость сварки (VW)', 4.0, 12.0, 8.0)
    param_fp = st.sidebar.slider('Расстояние от образцов до электронно-оптической системы (FP)', 50.0, 130.0, 90.0)
    data = {'IW': param_iw,
            'IF': param_if,
            'VW': param_vw,
            'FP': param_fp}
    features = pd.DataFrame(data, index=[0])
    return features

data1 = user_input_features()

st.subheader('Входные пользовательские параметры')
st.write(data1)

df = pd.read_csv('ebw_data1.csv')
df.drop_duplicates(inplace=True)

features = df.drop(['Depth', 'Width'], axis=1)
target = df[['Depth', 'Width']]

parameters_lr = {'n_jobs': [-1],
                 'normalize': [True]}
model_lr = LinearRegression()
grid_lr = GridSearchCV(estimator=model_lr, param_grid=parameters_lr, scoring='neg_mean_absolute_error', cv=5)
grid_lr.fit(features, target)
predict_lr = grid_lr.predict(data1)

st.subheader('Прогноз глубины')
st.write(predict_lr[:,0])

st.subheader('Прогноз ширины')
st.write(predict_lr[:,1])
