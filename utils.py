import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

def load_data(path):
    data = pd.read_csv(path)
    data['Fecha-I'] = pd.to_datetime(data['Fecha-I'], format="%Y/%m/%d %H:%M:%S")
    data['Fecha-O'] = pd.to_datetime(data['Fecha-O'], format="%Y/%m/%d %H:%M:%S")
    data = data.sort_values(by='Fecha-I')

    return data

def is_temporada_alta(fecha):
    if (
        fecha < date(2017, 3, 3) or
        fecha > date(2017, 12, 15) or
        date(2017, 7, 15) < fecha < date(2017, 7, 31) or
        date(2017, 9, 11) < fecha < date(2017, 9, 30)
        ):
        
        return True
    else:
        return False

def get_minutes_difference(row):
    return (row['Fecha-O']-row['Fecha-I']).total_seconds() / 60


def periodo_dia(hora):
    if hora >= 5 and hora < 12:
        return 'mañana'
    
    elif hora >=12 and hora < 19:
        return 'tarde'
    
    else:
        return 'noche'

def create_feature_dif_min(data):
    df = data.copy()
    df['dif_min'] = df.apply(lambda x: get_minutes_difference(x),axis=1)
    return df

def create_feature_atraso_15(data):
    df = data.copy()
    df['atraso_15'] = df['dif_min'].apply(lambda x: 1 if x > 15 else 0)
    
    return df

def create_feature_temporada_alta(data):
    df = data.copy()
    df['temporada_alta'] = data['Fecha-I'].apply(lambda x: 1 if is_temporada_alta(x) else 0)
    
    return df


def create_hour(data):
    
    df = data.copy()
    
    df['HORA'] = pd.DatetimeIndex(data['Fecha-I']).hour


    return df

def create_feature_periodo_dia(data):
    df = data.copy()
    
    df['periodo_dia'] = df['HORA'].apply(lambda x: periodo_dia(x)) 
    
    return df

def create_syntethic_features(data):
    df = data.copy()
    
    df = create_feature_temporada_alta(df)
    df = create_feature_dif_min(df)                                     
    df = create_feature_atraso_15(df)
    
    df = create_feature_periodo_dia(df)
    
    return df

def save_syntethic_features(data, path):
    SYNTHETIC_FEATURES = ['temporada_alta', 'dif_min', 'atraso_15', 'periodo_dia']
    
    data[SYNTHETIC_FEATURES].to_csv(path, index=False)
    
    
def plot_distribucion(data,var):
    data.groupby(var).count()['atraso_15'].sort_values(axis=0,ascending=False)[:20].plot.barh(figsize=(12,5))
    plt.xlabel('Conteo de vuelos')

    
def plot_retraso_promedio(data,var):
    data.groupby(var).mean()['atraso_15'].sort_values(axis=0,ascending=False)[:20].plot.barh(figsize=(12,5))
    plt.xlabel('Fracción de vuelos retrasados')
