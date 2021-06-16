import pandas as pd 
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
from pydeck.types import String


def separa_turnos(horario):
  if horario.hour in range(0,6):
    return 'Madrugada'
  elif horario.hour in range(6,13):
    return 'Manhã'
  elif horario.hour in range(13,19):
    return 'Tarde'
  else:
     return 'Noite'


def create_dw():
    columns = ['driverId','circuitId','constructorId','position_ql','positionOrder','points','laps','fastestLapTime','fastestLapSpeed','milliseconds','quantidade_pits', 'soma_tempo_pits','status']
    PATH = 'database/csv/'
    # CARREGA OS DATASETS
    results = pd.read_csv(PATH+'results.csv')
    status = pd.read_csv(PATH+'status.csv')
    races = pd.read_csv(PATH+'races.csv')    
    qualifying = pd.read_csv(PATH+'qualifying.csv')
    pit_stops = pd.read_csv(PATH+'pit_stops.csv')
    drivers = pd.read_csv(PATH+'drivers.csv')
    constructors = pd.read_csv(PATH+'constructors.csv')
    circuits = pd.read_csv(PATH+'circuits.csv')

    # JUNTA AS RELAÇÕES
    data = results.merge(status,on='statusId') 
    data.drop('statusId',inplace=True,axis=1)
    
    data = data.merge(races,on='raceId')
    

    data = data.merge(qualifying,on=['raceId','driverId','constructorId'],suffixes=(None,'_ql'),how='left')
    

    pits = pit_stops.groupby(['raceId','driverId']).agg({'lap':'count','milliseconds':'sum'}).rename(columns={'lap':'quantidade_pits','milliseconds':'soma_tempo_pits'}).reset_index()
    data = data.merge(pits,on=['raceId','driverId'],how='left')
    
    data.replace(r'\N',-1,inplace=True)

    # PREPARA A DIMENSÃO TEMPO

    dim_time = pd.DataFrame()#data[['raceId','driverId']].copy()
    dim_time['dia'] = pd.to_datetime(data.date).dt.day
    dim_time['mes'] = pd.to_datetime(data.date).dt.month
    dim_time['ano'] = pd.to_datetime(data.date).dt.year
    dim_time['dia_semana'] = pd.to_datetime(data.date).dt.weekday
    dim_time['turno'] = pd.to_datetime(data.time_y).apply(separa_turnos)
    dim_time = dim_time.drop_duplicates(subset=['dia','mes','ano'])
    indexes = dim_time.reset_index()
    dim_time['id_tempo'] = indexes.index.astype('int')

    # PREPARA A DIMENSÃO PILOTO

    dim_piloto = drivers[['driverId','forename','surname','dob','nationality']].copy()
    dim_piloto['nome_piloto']  = dim_piloto.forename + ' ' + dim_piloto.surname
    dim_piloto.drop(['forename','surname'],axis=1,inplace=True)
    dim_piloto.rename(columns={'driverId':'id_piloto','dob':'data_nasc_piloto',
    'nationality':'nacionalidade_piloto'},inplace=True)

    # PREPARA A DIMENSÃO CONSTRUTOR

    dim_construtor = constructors[['constructorId','name','nationality']].copy()
    dim_construtor.rename(columns={'constructorId':'id_construtor','name':'nome_construtor',
        'nationality':'nacionalidade_construtor'},inplace=True)

    # PREPARA A DIMENSÃO CIRCUITO
    dim_circuito = circuits[['circuitId','name','country','lat','lng','alt']].copy()
    dim_circuito.rename(columns={'circuitId':'id_circuito','name':'nome_circuito','country':'pais_circuito',
        'lat':'latitude','lng':'longitude','alt':'altitude'},inplace=True)
   
    # TABELA FATOS
    fact_table = data[columns].copy()
    fact_table = fact_table.join(dim_time['id_tempo'],rsuffix='time')
    fact_table['id_tempo'] = fact_table.id_tempo.fillna(method='ffill').astype('int')
    

    fact_table.replace(r'\N',-1,inplace=True)
    fact_table['volta_mais_rapida'] = pd.to_datetime(fact_table.fastestLapTime).dt.time
    fact_table['maior_velocidade'] = fact_table.fastestLapSpeed.astype('float')
    fact_table['tempo_corrida'] = fact_table.milliseconds.astype('int')
    fact_table.drop(['fastestLapTime','fastestLapSpeed','milliseconds'],axis=1,inplace=True)

    fact_table.rename(columns={'driverId':'id_piloto','circuitId':'id_circuito','constructorId':'id_construtor',
    'position_ql':'posicao_qualify','positionOrder':'posicao_corrida','points':'pontos','laps':'numero_voltas'},inplace=True)
    
    fact_table.to_csv('FATO_corrida.csv',index=False)
    dim_circuito.to_csv('DIM_circuito.csv',index=False)
    dim_piloto.to_csv('DIM_piloto.csv',index=False)
    dim_construtor.to_csv('DIM_construtor.csv',index=False)
    dim_time.to_csv('DIM_tempo.csv',index=False)





@st.cache
def load_dw():
    # CARREGANDO OS DATASETS (EXTRACT)
    fact_table = pd.read_csv('FATO_corrida.csv')
    dim_circuito = pd.read_csv('DIM_circuito.csv')
    dim_construtor = pd.read_csv('DIM_construtor.csv')
    dim_piloto = pd.read_csv('DIM_piloto.csv')
    dim_tempo = pd.read_csv('DIM_tempo.csv')
    return (fact_table,dim_circuito,dim_construtor,dim_piloto,dim_tempo)

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
    fact_table,dim_circuito,dim_construtor,dim_piloto,dim_tempo = load_dw()
    selecao = st.sidebar.selectbox('Selecione uma opção',opcoes)
    if selecao == 'Página principal':
        st.markdown(load_markdown('backend/tela_principal.md'),unsafe_allow_html=True)
    elif selecao == 'Construtores':
        constructor_data = fact_table.merge(dim_construtor,on='id_construtor')
        # PLOT DE MAIOR VELOCIDADE
        with st.echo(code_location='below'):
            grouped_constructor = constructor_data.groupby('nome_construtor').agg({'maior_velocidade':np.max}).sort_values(by='maior_velocidade',ascending=False)
            grouped_constructor = grouped_constructor[grouped_constructor.maior_velocidade != -1]
            fig,ax = plt.subplots()
            ax = sns.barplot(y=grouped_constructor.index,x='maior_velocidade',data=grouped_constructor,palette='dark')
            ax.set(xlabel='Maior velocidade (Km/h)',ylabel='Construtores')
            ax.set_title('Maiores velocidades totais por construtor')
            
            st.write(fig)
        

        # EVOLUÇÃO DAS VELOCIDADES POR CONSTRUTORES
        constructor_data_time = constructor_data.merge(dim_tempo,on='id_tempo')
        grouped_time_constructor = constructor_data_time.groupby(['ano','nome_construtor']).agg({'maior_velocidade':np.max}).sort_values(by='maior_velocidade',ascending=False)
        grouped_time_constructor = grouped_time_constructor[grouped_time_constructor.maior_velocidade != -1].reset_index()
        fig,ax = plt.subplots()
        equipe = st.selectbox('Escolha uma construtora',grouped_time_constructor['nome_construtor'])
        montadora = grouped_time_constructor.query('nome_construtor == @equipe').sort_values('ano')
        ax = sns.lineplot(x=montadora.ano.astype('str'),y='maior_velocidade',hue='nome_construtor',data=montadora)
        plt.xticks(rotation=45)
        ax.set(xlabel='Maior velocidade (Km/h)',ylabel='Construtora')
        ax.set_title(f'Evolução de velocidade pela equipe {equipe} pelo tempo')
        st.pyplot(fig)
        # CONSTRUTORES GANHADORES POR ANO

        grouped_points = constructor_data_time.groupby(['ano','nome_construtor']).agg({'pontos':np.sum}).reset_index().sort_values(by=['ano','pontos'],ascending=[True,False])
        winner_year = grouped_points.loc[grouped_points.groupby('ano')['pontos'].idxmax()]
        winner_year = winner_year[winner_year.ano > 1958]
        winner_times = winner_year.groupby('nome_construtor').agg({'ano':'count'}).rename(columns={'ano':'Quantidade_campeonatos'}).sort_values(by='Quantidade_campeonatos',ascending=False).reset_index()

        st.table(winner_year)

    elif selecao == 'Mapa':
        pass
        st.markdown('# Localização dos Autódromos pelo mundo')
        data = dim_circuito[['latitude','longitude','nome_circuito']].rename(columns={'latitude':'lat','longitude':'lon'})
        data = data.drop_duplicates()
        
        plot_map(data)


        
if __name__ == '__main__':
        create_dw()
    #main()
           