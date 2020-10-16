import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('messages.csv', index_col=0)

def parse(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.dropna()
    return df

def add_col_type(df):
    df['type'] = ''
    for index, row in df.iterrows():
        title = row['title'].upper().replace('/','')
        for model in ['B', 'C', 'D', 'E']:
            model = ' ' + model + ' '
            if model in title:
                df.loc[index,'type'] = model.strip()
    return df

def plt_type_av(df, window):
    df = parse(df)
    df = add_col_type(df)
    df = df[['price', 'date', 'type']]

    b = df[df['type']=='B']
    b['av'] = b['price'].rolling(window=window).mean()
    c = df[df['type']=='C']
    c['av'] = c['price'].rolling(window=window).mean()
    d = df[df['type']=='D']
    d['av'] = d['price'].rolling(window=window).mean()
    e = df[df['type']=='E']
    e['av'] = e['price'].rolling(window=window).mean()
    no_type = df[df['type']=='']
    no_type['av'] = no_type['price'].rolling(window=window).mean()

    plt.scatter(b.date, b.price, label='B', color='blue')
    #plt.plot(b.date, b.av, label='B', color='blue')
    plt.scatter(c.date, c.price, label='C', color='orange')
    #plt.plot(c.date, c.av, label='C', color='orange')
    plt.scatter(d.date, d.price, label='D', color='green')
    #plt.plot(d.date, d.av, label='D', color='green')
    plt.scatter(e.date, e.price, label='E', color='red')
    #plt.plot(e.date, e.av, label='E', color='red')
    plt.scatter(no_type.date, no_type.price, label='None', color='black')
    #plt.plot(no_type.date, no_type.av, label='None', color='black')

    plt.legend()
    plt.show()
    return


def plt_moving_av(df):
    df = parse(df)
    df = add_col_type(df)
    df = df[['price', 'date']]

    df['20d'] = df['price'].rolling(window=20).mean()
    df['30d'] = df['price'].rolling(window=30).mean()

    plt.plot(df.date, df['20d'], label='MA20', color='blue')
    plt.plot(df.date, df['30d'], label='MA30', color='black')
    plt.show()
    return

#plt_moving_av(df)

df = plt_type_av(df, window=3)

print(df)
