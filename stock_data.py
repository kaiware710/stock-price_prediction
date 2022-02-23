import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas_datareader.data as pdr


def get_stock_data(code):
    """Stooqから株価データをdfで取得

    Args:
        code (int): 銘柄コード

    Returns:
        df (): 株価データのDataFrame
    """

    df = pdr.DataReader("{}.JP".format(code), "stooq").sort_index()
    print(type(df))

    return df


def stock_line_graph(df, column):
    """dfの特定列のデータの折れ線グラフを保存

    Args:
        df (_type_): 株価データのDataFrame
        column (str): 列名
    """

    plt.figure()
    df[column].plot()
    plt.savefig("./graph/stock_close.png")
    plt.close("all")


CODE = 4751
stock_data_df = get_stock_data(CODE)
print(stock_data_df.tail(100))

# stock_line_graph(stock_data_df, "Close")
