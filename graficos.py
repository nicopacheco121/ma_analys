import matplotlib.pyplot as plt
from indicators import add_indicator_cruce
from positions import add_state, operations


def plot_activo_trade(data):

    df_copy = data.copy()
    df_copy['compras'] = (data.close * 0.90).loc[data.operacion == 'LONG']
    df_copy['ventas'] = (data.close * 1.10).loc[data.operacion == 'SHORT']


    plt.figure(figsize=(20, 6))

    plt.plot(data.close, color='black')
    plt.plot(data.media1)
    plt.plot(data.media2)
    plt.legend(['Precio', 'Media Rapida', 'Media Lenta'])

    plt.plot(data.index, df_copy.compras, '^', markersize=10, c='grey')
    plt.plot(data.index, df_copy.ventas, 'v', markersize=10, c='grey')

    plt.grid(which='major', axis='y', color='black', lw=1, alpha=0.15)
    plt.suptitle('Estrategia Cruce Medias', y=0.92)

    plt.savefig('grafico_estrategia')

    plt.show()


def grafico_best(data, resultados, k1, k2):
    indicador = resultados.iloc[0, 8]

    data_indicadores = add_indicator_cruce(data, indicador, k1=k1, k2=k2)
    data_estados = add_state(data_indicadores)
    operaciones = operations(data_estados)

    plot_activo_trade(data_indicadores)



