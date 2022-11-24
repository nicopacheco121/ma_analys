import pandas as pd
import numpy as np


def add_state(df):

    name = 'cruce'

    df['estado'] = np.where(df[name] > 0, 'LONG', 'SHORT')

    return df


def operations(df):

    df['operacion'] = np.where((df['estado'] == 'LONG') & (df['estado'].shift() == 'SHORT'), 'LONG',
                               np.where((df['estado'] == 'SHORT') & (df['estado'].shift() == 'LONG'), 'SHORT',
                                        ''))

    filtro_operaciones = df.loc[df['operacion'] != '']

    return filtro_operaciones


def add_trades(df, side='both'):

    filtro_trades = pd.DataFrame()

    filtro_trades['price_open'] = df.close
    filtro_trades['price_close'] = df.close.shift(-1)
    filtro_trades['side'] = df.operacion
    filtro_trades['date_init'] = df.index
    filtro_trades['date_fin'] = filtro_trades['date_init'].shift(-1)
    filtro_trades = filtro_trades.iloc[:-1]
    filtro_trades.reset_index(inplace=True)
    filtro_trades.drop(['Date'], axis=1, inplace=True)

    if side != 'BOTH':
        filtro_trades = filtro_trades.loc[filtro_trades['side'] == side]

    return filtro_trades


def add_results(df):

    df['dias'] = df['date_fin'] - df['date_init']

    df['rdo'] = np.where(df['side'] == 'LONG', df['price_close'] / df['price_open'] - 1,
                         df['price_open'] / df['price_close'] - 1) * 100

    df['rdo_acu'] = ((df['rdo'] / 100 + 1).cumprod() - 1) * 100

    count_operations = df['rdo'].groupby([df['rdo'] > 0]).count().to_dict()
    n_ganadores = count_operations[True]
    n_perdedores = count_operations[False]

    per_n_ganadores = (n_ganadores / (n_perdedores + n_ganadores)) * 100
    per_n_perdedores = (n_perdedores / (n_perdedores + n_ganadores)) * 100

    per_operations = df['rdo'].groupby([df['rdo'] > 0]).mean().to_dict()
    per_ganadores = per_operations[True]
    per_perdedores = per_operations[False]

    last_data = df.iloc[-1].to_dict()

    result = {}
    result['resultadodo_acumulado'] = last_data['rdo_acu']
    result['operaciones_totales'] = df.index[-1] + 1
    result['n_ganadores'] = n_ganadores
    result['n_perdedores'] = n_perdedores
    result['porcentaje_ganadores'] = per_n_ganadores
    result['porcentaje_perdedores'] = per_n_perdedores
    result['resultado_promedio_ganadores'] = per_ganadores
    result['resultado_promedio_perdedores'] = per_perdedores

    return result




