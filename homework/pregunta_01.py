"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
from datetime import datetime
import os


def limp_str_simp(df, col):
    df[col] = df[col].str.lower()
    return df

def limpieza_texto(df, col):
    return (
        df[col]
        .astype(str)
        .str.lower()
        .str.replace(r'[-_]', ' ', regex=True)
        .str.strip()
    )

def parse_fecha(fecha):
    formatos = [
        '%d/%m/%Y',
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%d %b %Y',
        '%d %B %Y',
        '%Y.%m.%d', 
    ]
    
    for fmt in formatos:
        try:
            return datetime.strptime(fecha, fmt)
        except:
            continue
    return pd.NaT

def limpiar_fecha(df, col):
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].apply(parse_fecha)
    return df

def limpiar_monto(df, col):
    df[col] = (
        df[col].astype(str)
        .str.replace(r'[^0-9.,]', '', regex=True) 
        .str.replace(',', '') 
        .str.replace(r'\.00$', '', regex=True)
        .astype(float)
        .astype(int)
    )
    return df

def pregunta_01():

    os.makedirs('files/output', exist_ok=True)

    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    df = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';')

    df.drop(['Unnamed: 0'], axis=1, inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    df['sexo'] = limpieza_texto(df, 'sexo')
    df['tipo_de_emprendimiento'] = limpieza_texto(df, 'tipo_de_emprendimiento')
    df['idea_negocio'] = limpieza_texto(df, 'idea_negocio')
    df['línea_credito'] = limpieza_texto(df, 'línea_credito')

    df['barrio'] = df['barrio'].str.lower().replace(['-', '_'], ' ', regex=True) 

    df = limpiar_fecha(df, 'fecha_de_beneficio')
    df = limpiar_monto(df, 'monto_del_credito')

    df.drop_duplicates(inplace=True)
    df.to_csv('files/output/solicitudes_de_credito.csv', index=False, sep=';')

    return