import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")
df = pd.read_csv(r'bitmex_xbt_4h.csv')
df = df[200:-100]
df.index = pd.to_datetime(df['datetime'])
df = df.resample('D').mean()


class KDJ_calculator:
    """
    calculator KDJ indicator according the close  price
    """

    def __init__(self, data, n_period):
        """
        initialise the class with raw data
        :param data:
        :param n_period: the cycle be chose to calc
        """
        self.data = data
        self.n_period = n_period

    def rsv(self):
        # past n periods of HIGH price
        n_high = self.data.high.rolling(self.n_period).max()
        # past n periods of LOW price
        n_low = self.data.low.rolling(self.n_period).min()
        # the RSV values
        rsv = ((self.data.close - n_low) / (n_high - n_low)) * 100
        rsv.dropna(inplace=True)
        self.rsv = rsv

    def kdj_calculator(self):
        """
        calculate according the algorithm
        :return:
        """
        self.k_values, self.d_values, self.j_values = [], [], []

        for idx, value in enumerate(self.rsv):
            if idx == 0:
                K, D, J = 50, 50, 50
                self.k_values.append(K)
                self.d_values.append(D)
                self.j_values.append(J)
            else:
                K = (2 / 3) * self.k_values[-1] + (1 / 3) * value
                D = (2 / 3) * self.d_values[-1] + (1 / 3) * K
                J = 3 * K - 2 * D
                self.k_values.append(K)
                self.d_values.append(D)
                self.j_values.append(J)

    def show_kdj_indicator(self):
        """

        :return: 3 columns data contains the K D J values
        """
        self.kdj_df = pd.DataFrame([self.k_values, self.d_values, self.j_values]).T
        self.kdj_df.columns = ['K', 'D', 'J']
        return self.kdj_df

    def combine_kdj_to_raw_data(self):
        """
        combine the K D J columns with the exist raw dataframe
        :return: combined dataframe
        """
        tmp_df = self.data[self.n_period - 1:]
        self.kdj_df.index = tmp_df.index
        self.kdj_indicators = pd.concat([tmp_df, self.kdj_df], axis=1)
        return self.kdj_indicators


kdj = KDJ_calculator(df, 9)

kdj.rsv()

kdj.kdj_calculator()

kdj.show_kdj_indicator()

kdj.combine_kdj_to_raw_data()

result = kdj.combine_kdj_to_raw_data()[['K', 'D', 'J']]

result.plot(figsize=(40, 10))
