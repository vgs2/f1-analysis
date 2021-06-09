import numpy as np
import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns



def load_datasets():
    # CARREGANDO OS DATASETS (EXTRACT)
    PATH = '../database/csv/'
    results = pd.read_csv(PATH+'results.csv')
    status = pd.read_csv(PATH+'status.csv')
    races = pd.read_csv(PATH+'races.csv')
    driver = pd.read_csv(PATH+'drivers.csv')
    # JUNTANDO EM UMA TABELA E TRANSFORMANDO OS DADOS (TRANSFORM)
    results = results.merge(status,on='statusId')
    results.drop('statusId',axis=1,inplace=True)
    results.drop('positionText',axis=1,inplace=True)
    results = results.merge(races,on='raceId')
    # O campo time em races possui 18469 de 25040 campos em branco, como perdemos muita informação, melhor não utilizá-lo
    results.drop('url',axis=1,inplace=True)
    results.drop('time_y',axis=1,inplace=True)
    results['date'] = pd.to_datetime(results.date)
    results = results.merge(driver,on='driverId')
    results['name'] = results.forename + ' '+ results.surname
    results.drop('url',axis=1,inplace=True)
    results.drop('forename',axis=1,inplace=True)
    results.drop('surname',axis=1,inplace=True)
    results.drop('driverRef',axis=1,inplace=True)
    results['pilot_dob'] = pd.to_datetime(results.dob)
    results.drop('dob',axis=1,inplace=True)


    return results
def get_n_most_drivers(query_str,df,n=10):
    return df.query(query_str).groupby('name').count().sort_values(by='resultId',ascending=False).nlargest(n,'resultId').reset_index().iloc[:,:2]
results = load_datasets()
query = get_n_most_drivers('positionOrder == 1 & nationality == "Brazilian"',results)
fig, ax = plt.subplots()
ax.barh(query['name'],query['resultId'])
st.write(fig)
