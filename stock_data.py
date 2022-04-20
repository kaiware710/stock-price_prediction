import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas_datareader.data as pdr
import plotly.graph_objs as go
import talib as ta
from pyquery import PyQuery as pq
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


def macd(df):
    """終値からMACDを計算し、可視化
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """
    close = df["Close"]
    macd, macdsignal, _ = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df["macd"] = macd
    df["macd_signal"] = macdsignal
    mdf = df.tail(100)  # 直近100日分のデータ
    apd = [
        mpf.make_addplot(mdf["macd"], panel=2, color="red"),  # 赤:MACDライン
        mpf.make_addplot(mdf["macd_signal"], panel=2, color="blue"),  # 青:シグナルライン
    ]
    mpf.plot(mdf, type="candle", volume=True, addplot=apd)


def rsi(df):
    """終値からRSIを計算し、可視化  売られすぎ:0 〜 買われすぎ:100
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """
    close = df["Close"]
    rsi14 = ta.RSI(close, timeperiod=14)
    rsi28 = ta.RSI(close, timeperiod=28)
    df["rsi14"], df["rsi28"] = rsi14, rsi28
    mdf = df.tail(100)
    apd = [
        mpf.make_addplot(mdf["rsi14"], panel=2, color="red"),
        mpf.make_addplot(mdf["rsi28"], panel=2, color="blue"),
    ]
    mpf.plot(mdf, type="candle", volume=True, addplot=apd)


def sma(df):
    """TA-Libを使って移動平均線を表示
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """
    close = df["Close"]
    ma5, ma25, ma75 = (
        ta.SMA(close, timeperiod=5),
        ta.SMA(close, timeperiod=25),
        ta.SMA(close, timeperiod=75),
    )
    df["ma5"], df["ma25"], df["ma75"] = ma5, ma25, ma75
    mdf = df.tail(200)
    apd = [
        mpf.make_addplot(mdf["ma5"], panel=0, color="blue"),
        mpf.make_addplot(mdf["ma25"], panel=0, color="purple"),
        mpf.make_addplot(mdf["ma75"], panel=0, color="yellow"),
    ]
    mpf.plot(mdf, type="candle", volume=True, addplot=apd)


def macd_rsi_sma(df):
    """macd, rsi, 移動平均線を可視化
    Args:
        df (pandas.core.frame.DataFrame): 株価データのDataFrame
    """
    close = df["Close"]
    macd, macdsignal, _ = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df["macd"], df["macd_signal"] = macd, macdsignal
    rsi14, rsi28 = ta.RSI(close, timeperiod=14), ta.RSI(close, timeperiod=28)
    df["rsi14"], df["rsi28"] = rsi14, rsi28
    ma5, ma25, ma75 = (
        ta.SMA(close, timeperiod=5),
        ta.SMA(close, timeperiod=25),
        ta.SMA(close, timeperiod=75),
    )
    df["ma5"], df["ma25"], df["ma75"] = ma5, ma25, ma75

    mdf = df.tail(200)
    apd = [
        mpf.make_addplot(mdf["ma5"], panel=0, color="blue"),
        mpf.make_addplot(mdf["ma25"], panel=0, color="purple"),
        mpf.make_addplot(mdf["ma75"], panel=0, color="yellow"),
        mpf.make_addplot(mdf["macd"], panel=2, color="red"),
        mpf.make_addplot(mdf["macd_signal"], panel=2, color="blue"),
        mpf.make_addplot(mdf["rsi14"], panel=3, color="red"),
        mpf.make_addplot(mdf["rsi28"], panel=3, color="blue"),
    ]
    mpf.plot(mdf, type="candle", volume=True, addplot=apd)


def golden_dead_cross(code, df):
    close = df["Close"]
    # 5日, 25日の移動平均
    ma5, ma25 = ta.SMA(close, timeperiod=5), ta.SMA(close, timeperiod=25)
    df["ma5"], df["ma25"] = ma5, ma25

    # 200日分のローソク足チャート
    df = df.tail(200)

    url = "https://kabutan.jp/stock/?code={}".format(code)
    q = pq(url)
    print(q)

    # layout = {"title": {"text": ""}}


CODE = 6501
# 2897:日清食品 3563:food&life companies(スシロー) 4751: cyber agent 6501:日立
# 6670:MCJ 8591:オリックス 9101:日本郵船 9104:商船三井 9434:softbank
# リゾート 航空 ドル建て 情勢

DF = get_stock_data(CODE)

COLUMN = "Close"
# stock_line_graph(DF, COLUMN, CODE)

# NUMBER_OF_DATA = len(DF.index)
NUMBER_OF_DATA = 500
MOVING_AVARAGE = (5, 25, 75)
# stock_candle_graph(DF, NUMBER_OF_DATA, MOVING_AVARAGE, CODE)

NUMBER_OF_DATA = 300
COLUMN = "Close"
PERIOD = 25
# candle_bollingerband(DF.tail(NUMBER_OF_DATA), COLUMN, PERIOD, CODE)

# macd(DF)

# rsi(DF)

# sma(DF)

# macd_rsi_sma(DF)

golden_dead_cross(CODE, DF)

plt.close("all")
