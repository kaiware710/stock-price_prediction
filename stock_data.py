import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas_datareader.data as pdr


def get_stock_data(code):
    """Stooqから株価データ5年分をdfで取得

    Args:
        code (int): 銘柄コード

    Returns:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """

    df = pdr.DataReader("{}.JP".format(code), "stooq").sort_index()

    return df


def stock_line_graph(df, column):
    """dfの特定列のデータの折れ線グラフを保存

    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
        column (str): 列名
    """

    plt.figure()
    df[column].plot()
    plt.savefig("./graph/stock_close.png")
    plt.close("all")


def stock_candle_graph(df, number_of_data, mav):
    """ローソク足チャート、移動平均線、出来高を表示

    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
        number_of_data (int): 可視化するデータ数（最新からの数）
        mav (tuple - int): {mav}日の移動平均線
    """

    mpf.plot(df.tail(number_of_data), type="candle", mav=mav, volume=True)


CODE = 4751

stock_data_df = get_stock_data(CODE)

# stock_line_graph(stock_data_df, "Close")

NUMBER_OF_DATA = 200
MOVING_AVARAGE = (5, 25, 75)
stock_candle_graph(stock_data_df, NUMBER_OF_DATA, MOVING_AVARAGE)
