import pandas as pd


def add_sma(df, column_name, k):
    if k == 0:
        return df[column_name]
    else:
        return df[column_name].rolling(k).mean()


def add_cruce_sma(df_copy, column_name, k1, k2):
    df = df_copy.copy()
    if k1 == 0:
        df['media1'] = df[column_name]

    else:
        df['media1'] = add_sma(df, column_name, k1)
    df['media2'] = add_sma(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['media1', 'media2'], axis=1, inplace=True)

    return df


def add_ema(df, column_name, k):
    if k == 0:
        return df[column_name]
    else:
        return df[column_name].ewm(span=k, adjust=False).mean()


def add_cruce_ema(df_copy, column_name, k1, k2):
    df = df_copy.copy()

    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_ema(df, column_name, k1)
    df['media2'] = add_ema(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['media1', 'media2'], axis=1, inplace=True)

    return df


def add_dema(df_copy, column_name, k):
    """
    DEMA = 2 * EMA1 - 2 * EMA2
    EMA 1 = EMA
    EMA 2 = EMA de EMA1
    """

    df = df_copy.copy()

    if k == 0:
        return df[column_name]
    else:
        df['media1'] = add_ema(df, column_name, k)
        df['ema_media1'] = add_ema(df, 'media1', k)
        return 2 * df['media1'] - df['ema_media1']


def add_cruce_dema(df_copy, column_name, k1, k2):
    """
    DEMA = 2 * EMA1 - 2 * EMA2
    EMA 1 = EMA
    EMA 2 = EMA de EMA1
    """
    df = df_copy.copy()
    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_dema(df, column_name, k1)

    df['media2'] = add_dema(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['dema1', 'dema2'], axis=1, inplace=True)

    return df


def add_tema(df_copy, column_name, k):
    """
    TEMA = 3 * EMA1 - 3 * EMA2 + EMA3
    EMA 1 = EMA
    EMA 2 = EMA de EMA1
    EMA 3 = EMA de EMA2
    """
    df = df_copy.copy()

    if k == 0:
        return df[column_name]
    else:
        df['media1'] = df[column_name].ewm(span=k, adjust=False).mean()
        df['ema_media1'] = df['media1'].ewm(span=k, adjust=False).mean()
        df['ema_ema_media1'] = df['ema_media1'].ewm(span=k, adjust=False).mean()
        return 3 * df['media1'] - 3 * df['ema_media1'] + df['ema_ema_media1']


def add_cruce_tema(df_copy, column_name, k1, k2):
    """
    TEMA = 3 * EMA1 - 3 * EMA2 + EMA3
    EMA 1 = EMA
    EMA 2 = EMA de EMA1
    EMA 3 = EMA de EMA2
    """

    df = df_copy.copy()
    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_tema(df, column_name, k1)

    df['media2'] = add_tema(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['tema1', 'tema2'], axis=1, inplace=True)

    return df


def add_wma(df_copy, column_name, k):
    """
    PESO = 1/n
    WMA = Sumatoria de los Precio z * i/n
    Siendo i partiendo de 1 a n
    Siendo z partiendo del mas alejado hacia el mas cercano
    """
    df = df_copy.copy()

    if k == 0:
        return df[column_name]
    else:
        return df[column_name].rolling(k).apply(lambda x: x[::-1].cumsum().sum() * 2 / k / (k + 1))


def add_cruce_wma(df_copy, column_name, k1, k2):
    """
    PESO = 1/n
    WMA = Sumatoria de los Precio z * i/n
    Siendo i partiendo de 1 a n
    Siendo z partiendo del mas alejado hacia el mas cercano
    """
    df = df_copy.copy()
    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_wma(df, column_name, k1)

    df['media2'] = add_wma(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['media1', 'media2'], axis=1, inplace=True)

    return df


def add_hma(df_copy, column_name, k):
    """
    HMA = WMA (RAW WMA periodo = sqrt(n)
    RAW WMA = 2 * WMA2 - WMA1
    WMA1 = WMA n
    WMA2 = (WMA n/2) * 2
    """
    df = df_copy.copy()
    k_a = round(k / 2)

    if k == 0:
        return df[column_name]
    else:
        df['media1'] = df[column_name].rolling(k).apply(lambda x: x[::-1].cumsum().sum() * 2 / k / (k + 1))
        df['media1_edit'] = df[column_name].rolling(k_a).apply(lambda x: x[::-1].cumsum().sum() * 2 / k_a / (k_a + 1))
        df['a1'] = df['media1_edit'] * 2 - df['media1']
        k_s = round(k ** 0.5)
        return df['a1'].rolling(k_s).apply(lambda x: x[::-1].cumsum().sum() * 2 / k_s / (k_s + 1))


def add_cruce_hma(df_copy, column_name, k1, k2):
    """
    HMA = WMA (RAW WMA periodo = sqrt(n)
    RAW WMA = 2 * WMA2 - WMA1
    WMA1 = WMA n
    WMA2 = (WMA n/2) * 2
    """

    df = df_copy.copy()

    if k1 == 0:
        df['media1'] = df[column_name]
    else:
        df['media1'] = add_hma(df, column_name, k1)

    df['media2'] = add_hma(df, column_name, k2)

    df['cruce'] = df['media1'] / df['media2'] - 1
    # df.drop(['hma1', 'hma2'], axis=1, inplace=True)

    return df


def add_indicator_cruce(df, indicador, k1, k2):
    for activo in df.columns:

        if indicador == 'SMA':
            df = add_cruce_sma(df, activo, k1, k2)

        elif indicador == 'EMA':
            df = add_cruce_ema(df, activo, k1, k2)

        elif indicador == 'WMA':
            df = add_cruce_wma(df, activo, k1, k2)

        elif indicador == 'DEMA':
            df = add_cruce_dema(df, activo, k1, k2)

        elif indicador == 'TEMA':
            df = add_cruce_tema(df, activo, k1, k2)

        elif indicador == 'HMA':
            df = add_cruce_hma(df, activo, k1, k2)

        else:
            df = pd.DataFrame()

    df.dropna(inplace=True)

    return df
