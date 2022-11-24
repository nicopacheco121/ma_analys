import pandas as pd
pd.options.display.max_columns = 10

from data_apis import data_etfs
from indicators import add_indicator_cruce
from positions import add_state, operations, add_trades, add_results
from graficos import grafico_best


def run(tickers, indicadores, m_rapida, m_lenta, side):

    resultados = []

    data = data_etfs(tickers)
    data.columns = ['close']

    for indicador in indicadores:

        # AGREGO INDICADORES
        data_indicadores = add_indicator_cruce(data, indicador, k1=m_rapida, k2=m_lenta)

        # AGREGO ESTADOS
        data_estados = add_state(data_indicadores)

        # AGREGO OPERACIONES
        operaciones = operations(data_estados)

        # ARMO LOS TRADES
        trades = add_trades(operaciones, side)

        # RESULTADOS
        resultado = add_results(trades)
        resultado['indicador'] = indicador
        resultado['medias'] = str(m_rapida) + '_' + str(m_lenta)

        resultados.append(resultado)

    resultados = pd.DataFrame(resultados)
    resultados.sort_values(by='resultadodo_acumulado', axis=0, ascending=False, inplace=True)
    print(resultados)
    resultados.to_excel('resultados.xlsx')

    # PLOTEO
    grafico_best(data, resultados, m_rapida, m_lenta)


if __name__ == '__main__':
    tickers = ['SPY']
    indicadores = ['SMA', 'EMA', 'DEMA', 'TEMA', 'WMA', 'HMA']
    m_rapida = 20
    m_lenta = 50
    side = 'BOTH'

    run(tickers=tickers, indicadores=indicadores, m_rapida=m_rapida, m_lenta=m_lenta, side=side)