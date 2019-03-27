import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta,datetime

plt.style.use("ggplot")

df = pd.read_csv(r'bitmex_xbt_4h.csv')
df.index = pd.to_datetime(df['datetime'])

df_resample = pd.DataFrame(index=df.resample('4H').mean().index)
df_resample['close'] = df['close'].resample('4H').last()
df_resample['high'] = df['high'].resample('4H').max()
df_resample['low'] = df['low'].resample('4H').min()
df_resample['open'] = df['open'].resample('4H').first()


class KDJ_calculator:
    """

    """

    def __init__(self, data, n_period):
        self.data = data
        self.n_period = n_period

    def rsv(self):
        n_high = self.data.high.rolling(self.n_period).max()
        n_low = self.data.low.rolling(self.n_period).min()
        rsv = ((self.data.close - n_low) / (n_high - n_low)) * 100
        rsv.dropna(inplace=True)
        self.rsv = rsv

    def kdj_calculator(self):
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
        self.kdj_df = pd.DataFrame([self.k_values, self.d_values, self.j_values]).T
        self.kdj_df.columns = ['K', 'D', 'J']
        return self.kdj_df

    def combine_kdj_to_raw_data(self):
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

start = datetime(year=2018,month=9,day=3,hour=10)
end = start + timedelta(hours=40)

print(result[(result.index<end)&(result.index>start)])
