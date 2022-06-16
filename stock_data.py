import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas_datareader.data as pdr
import plotly.graph_objs as go
import talib as ta
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
    df = df.tail(200)

    layout = {
        "title": {"text": "日立(6501)", "x": 0.5},
        "xaxis": {"title": "日付", "rangeslider": {"visible": False}},
        "yaxis": {"title": "価格(円)", "side": "left", "tickformat": ","},
        "plot_bgcolor": "light blue",
    }

    # ローソク足チャート
    # data = [
    #     go.Candlestick(
    #         x=df.index,
    #         open=df["Open"],
    #         high=df["High"],
    #         low=df["Low"],
    #         close=df["Close"],
    #         increasing_line_color="#00ada9",
    #         decreasing_line_color="#a0a0a0",
    #     )
    # ]
    # fig = go.Figure(layout=go.Layout(layout), data=data)
    # fig.show()

    # ゴールデンクロス(gc), デッドクロス(dc)を検知
    ma5, ma25 = df["ma5"], df["ma25"]
    cross = ma5 > ma25
    cross_shift = cross.shift(1)
    temp_gc = (cross != cross_shift) & (cross == True)
    temp_dc = (cross != cross_shift) & (cross == False)
    gc = [m if g == True else np.nan for g, m in zip(temp_gc, ma5)]
    dc = [m if d == True else np.nan for d, m in zip(temp_dc, ma25)]
    df["gc"], df["dc"] = gc, dc
    # 移動平均線 ゴールデンクロス デッドクロス
    data = [
        go.Candlestick(
            name="chart",
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="#00ada9",
            decreasing_line_color="#a0a0a0",
        ),
        go.Scatter(
            x=df.index, y=df["ma5"], name="MA5", line=dict(color="#ff007f", width=1.2)
        ),
        go.Scatter(
            x=df.index, y=df["ma25"], name="MA25", line=dict(color="#7fbfff", width=1.2)
        ),
        go.Scatter(
            x=df.index,
            y=df["gc"],
            name="Golden Cross",
            mode="markers",
            marker=dict(size=12, color="blueviolet"),
        ),
        go.Scatter(
            x=df.index,
            y=df["dc"],
            name="Dead Cross",
            mode="markers",
            marker=dict(size=12, color="black", symbol="x"),
        ),
    ]
    fig = go.Figure(data=data, layout=go.Layout(layout))
    fig.show()


def summary_predict_stock(df):
    # 株価取得
    close = df["Close"]
    close_list = close.tolist()

    # ボリンジャーバンド
    period = 25
    bbup, bbmid, bblow = (
        bb_up(close_list, period),
        bb_mid(close_list, period),
        bb_low(close_list, period),
    )
    df["bb_up"], df["bb_mid"], df["bb_low"] = bbup, bbmid, bblow

    # オシレーター 移動平均 (Ta-Lib)
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

    # ゴールデンクロス デッドクロス
    cross = ma5 > ma25
    cross_shift = cross.shift(1)
    temp_gc = (cross != cross_shift) & (cross == True)
    temp_dc = (cross != cross_shift) & (cross == False)
    gc = [m if g == True else np.nan for g, m in zip(temp_gc, ma5)]
    dc = [m if d == True else np.nan for d, m in zip(temp_dc, ma25)]
    df["gc"], df["dc"] = gc, dc

    # 計算結果 グラフ 120日分
    pdf = df.tail(120)
    layout = {
        "title": {"text": "5401", "x": 0.5},
        "xaxis": {"title": "日付", "rangeslider": {"visible": False}},
        "yaxis": {"title": "価格（円）", "tickformat": ","},
        "plot_bgcolor": "light blue",
    }
    data = [
        go.Candlestick(
            name="chart",
            x=pdf.index,
            open=pdf["Open"],
            high=pdf["High"],
            low=pdf["Low"],
            close=pdf["Close"],
            increasing_line_color="#00ada9",
            decreasing_line_color="#a0a0a0",
        ),
        go.Scatter(
            x=pdf.index, y=pdf["ma5"], name="MA5", line=dict(color="#ff007f", width=1.2)
        ),
        go.Scatter(
            x=pdf.index,
            y=pdf["ma25"],
            name="MA25",
            line=dict(color="#7fbfff", width=1.2),
        ),
        go.Scatter(
            x=pdf.index,
            y=pdf["gc"],
            name="Golden Cross",
            mode="markers",
            marker=dict(size=12, color="blueviolet"),
        ),
        go.Scatter(
            x=pdf.index,
            y=pdf["dc"],
            name="Dead Cross",
            mode="markers",
            marker=dict(size=12, color="black", symbol="x"),
        ),
        # ボリンジャーバンド
        go.Scatter(x=pdf.index, y=pdf["bb_up"], name="BB_Up", line=dict(width=0)),
        go.Scatter(
            x=pdf.index,
            y=pdf["bb_low"],
            name="BB_Low",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(170,170,170,0.25)",
        ),
    ]
    fig = go.Figure(data=data, layout=go.Layout(layout))

    # 日付と曜日を考慮
    df.reset_index(inplace=True)
    # 3日に1日の日付を取り出す
    days_list = [df.index[idx : idx + 3] for idx in range(0, len(df.index), 3)]
    dates = [df["Date"][r[0]] for r in days_list]
    # X軸を更新
    fig["layout"].update(
        {
            "xaxis": {
                "showgrid": True,
                "tickvals": np.arange(0, df.index[-1], 3),
                "ticktext": [x.strftime("%m/%d") for x in dates],
            }
        }
    )

    fig.show()


CODE = 5401
# 2897:日清食品 3563:food&life companies(スシロー) 4751:cyber agent 5401:日本製鉄
# 6501:日立 6670:MCJ 8591:オリックス 9101:日本郵船 9104:商船三井 9434:softbank
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
# golden_dead_cross(CODE, DF)
summary_predict_stock(DF)

plt.close("all")
