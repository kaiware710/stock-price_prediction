import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas_datareader.data as pdr
from pyti.bollinger_bands import lower_bollinger_band as bb_low
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from pyti.bollinger_bands import upper_bollinger_band as bb_up


def get_stock_data(code):
    """Stooqから株価データ5年分をdfで取得
    Args:
        code (int): 銘柄コード
    Returns:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """
    df = pdr.DataReader("{}.JP".format(code), "stooq").sort_index()
    return df


def stock_line_graph(df, column, code):
    """dfの特定列のデータの折れ線グラフを保存
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
        column (str): 列名
        code (int): 銘柄コード
    """
    plt.figure()
    df[column].plot()
    plt.savefig("./graph/" + column + "_" + str(code) + ".png")


def stock_candle_graph(df, number_of_data, mav, code):
    """ローソク足チャート、移動平均線、出来高を表示
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
        number_of_data (int): 可視化するデータ数（最新からの数）
        mav (tuple - int): {mav}日の移動平均線
    """
    mpf.plot(
        df.tail(number_of_data),
        type="candle",
        mav=mav,
        volume=True,
        savefig="./graph/candle-mav-vol_" + str(code) + ".png",
    )


def candle_bollingerband(df, column, period, code):
    """ボリンジャーバンド:period日線と株価の変動範囲を折れ線グラフで表示

    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
        column (str): 列名
        period (int): 相場の振れ幅を計算する期間
    """
    data = df[column].tolist()
    period = period
    bollinger_band_up = bb_up(data, period)
    bollinger_band_mid = bb_mid(data, period)
    bollinger_band_low = bb_low(data, period)
    df["bb_up"] = bollinger_band_up
    df["bb_mid"] = bollinger_band_mid
    df["bb_low"] = bollinger_band_low
    plt.figure()
    apd = mpf.make_addplot(df[["bb_up", "bb_mid", "bb_low"]])
    mpf.plot(
        df,
        type="candle",
        addplot=apd,
        volume=True,
        savefig="./graph/candle-bollingerband_" + str(code) + ".png",
    )


CODE = 3563
# 2897:日清食品  3563:food&life companies(スシロー)  4751: cyber agent  6501:日立
# 9101:日本郵船  9104:商船三井  9434:softbank

stock_data_df = get_stock_data(CODE)

COLUMN = "Close"
# stock_line_graph(stock_data_df, COLUMN, CODE)

# NUMBER_OF_DATA = len(stock_data_df.index)
NUMBER_OF_DATA = 500
MOVING_AVARAGE = (5, 25, 75)
# stock_candle_graph(stock_data_df, NUMBER_OF_DATA, MOVING_AVARAGE, CODE)

NUMBER_OF_DATA = 300
COLUMN = "Close"
PERIOD = 25
candle_bollingerband(stock_data_df.tail(NUMBER_OF_DATA), COLUMN, PERIOD, CODE)

plt.close("all")
