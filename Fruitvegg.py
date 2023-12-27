import pandas as pd


class Fruitvegg:
    def __init__(self):
        self.df = pd.read_csv("fruitvegprices-2017_2022.csv")
        self.df.date = pd.to_datetime(self.df.date)
        self.df.sort_index(ascending=True)

    def re(self):
        """

        :return: fruit and vegetable price data
        """
        return self.df


def tracer(fun):
    def new_fun(*args):
        s = ",".join(str(arg) for arg in args)
        print(f"{s}")
        return fun(*args)
    return new_fun



