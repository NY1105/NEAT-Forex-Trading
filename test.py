from datetime import date
import pandas as pd


df = pd.DataFrame(columns=['time','open','close','low','high','volume'])

df.loc[len(df)] = [date(2022,6,1),100,101,100,10,5000]
df.loc[len(df)] = [date(2022,6,1),100,101,100,10,5000]
print(df)