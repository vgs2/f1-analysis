import pandas as pd 
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
from pydeck.types import String




@st.cache
def load_datasets():
    # CARREGANDO OS DATASETS (EXTRACT)
    PATH = 'database/csv/'
    results = pd.read_csv(PATH+'results.csv')
    status = pd.read_csv(PATH+'status.csv')
    races = pd.read_csv(PATH+'races.csv')
    driver = pd.read_csv(PATH+'drivers.csv')
    circuits = pd.read_csv(PATH+'circuits.csv')
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
    results['driver_name'] = results.forename + ' '+ results.surname
    results.drop('url',axis=1,inplace=True)
    results.drop('forename',axis=1,inplace=True)
    results.drop('surname',axis=1,inplace=True)
    results.drop('driverRef',axis=1,inplace=True)
    results['pilot_dob'] = pd.to_datetime(results.dob)
    results.drop('dob',axis=1,inplace=True)
    results = results.merge(circuits,on='circuitId')
    results.drop('url',axis=1,inplace=True)
    results['lon'] = results['lng']
    results['nome_circuito'] = results.name_y
    results.drop('lng',axis=1,inplace=True)
    results.drop('name_y',axis=1,inplace=True)

    return results
def get_n_most_drivers(query_str,df,n=10):
    return df.query(query_str).groupby('driver_name').count().reset_index().sort_values(by='resultId',ascending=True).nlargest(n,'resultId').iloc[:,:2]


def load_markdown(arq):
    text = ''
    with open(arq,'r') as f:
        text = f.read()
    return text

def plot_map(df):

    layer = pdk.Layer(
    "TextLayer",
    df,
    pickable=True,
    get_position="[lon,lat]",
    get_text="nome_circuito",
    get_size=16,
    get_color=[0, 0, 0],
    get_angle=0,
    # Note that string constants in pydeck are explicitly passed as strings
    # This distinguishes them from columns in a data set
    get_text_anchor=String("middle"),
    get_alignment_baseline=String("center"),
    )
    view_state = pdk.ViewState(latitude=0, longitude=0,zoom=2)
    r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{nome_circuito}"},
    map_style="mapbox://styles/mapbox/light-v9",
    )
    st.pydeck_chart(r)
    


def main():
    st.set_page_config('Data Power',':male_mage:')
    opcoes = ('Página principal','Construtores','Corredores','Grand Prixes','Mapa')
    results = load_datasets()
    selecao = st.sidebar.selectbox('Selecione uma opção',opcoes)
    if selecao == 'Página principal':
        st.markdown(load_markdown('backend/tela_principal.md'),unsafe_allow_html=True)
    elif selecao == 'Corredores':
        st.write(results.head())
        st.write('Corredores com mais pódios')
        query = get_n_most_drivers('positionOrder == 1',results)
        fig, ax = plt.subplots()
        ax.barh(query['driver_name'],query['resultId'])
        st.write(fig)

        st.write('Corredores brasileiros com mais pódios')
        query = get_n_most_drivers('positionOrder == 1 & nationality == "Brazilian"',results)
        fig, ax = plt.subplots()
        ax.barh(query['driver_name'],query['resultId'])
        st.write(fig)
    elif selecao == 'Mapa':
        st.markdown('# Localização dos Autódromos pelo mundo')
        data = results[['lat','lon','nome_circuito']]
        data = data.drop_duplicates()
        
        plot_map(data)


        
if __name__ == '__main__':
    main()