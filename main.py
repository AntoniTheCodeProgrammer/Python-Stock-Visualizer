from import_data import download_data
import matplotlib.pyplot as plt
import streamlit
import altair
import datetime

actual_date = datetime.date.today()
min_date = actual_date.replace(year=actual_date.year - 5)
# from dateutil.relativedelta import relativedelta
# min_date = actual_date - relativedelta(years=5)

streamlit.set_page_config(layout="wide")

main, candle_page = streamlit.tabs(["Main", "Candle Graph"])


with main:
    # Header
    left, right = streamlit.columns([1, 3], gap="medium")

    # Input
    with left, streamlit.container(border=True):
        streamlit.write("### DATA:")
        number = 2
        number = streamlit.slider("How many campanies?", 1, 5, 2)
        companies = ["AAPL", "GOOG"]

        start_date, end_date = streamlit.slider(
            label = "Date range",
            key = "range1",
            min_value = min_date,
            max_value = actual_date,
            value = (datetime.date(2021,3,12), datetime.date(2023,5,11)),
            format = "DD/MM/YY"
        )

        for i in range(0, number):
            if  i < len(companies): 
                ticker = streamlit.text_input("Campany name", companies[i], key=f"Company{i}")
                companies[i] = ticker
            else: 
                ticker = streamlit.text_input("Campany name", "", key=f"Company{i}")
                companies.append(ticker)
        for i in range(5-number):
            streamlit.space("large")

    with streamlit.spinner('Pobieranie danych z giełdy...'):
        companies = companies[:number]
        data = download_data(companies, start_date, end_date)
        close_prices = data["Close"]

    # Main chart
    with right:
        with streamlit.container(border=True):
            streamlit.line_chart(close_prices)
        with streamlit.container(border=True):
            streamlit.write("Price change:")
            stock_change = streamlit.columns(number, border=True)
            for i in range(number):
                if companies[i] != "":
                    start_price = data.head(1)["Close"][companies[i]].values[0]
                    end_price = data.tail(1)["Close"][companies[i]].values[0]
                    percent = (end_price - start_price)/start_price*100
                    stock_change[i].metric(label=companies[i], value=f"{round(end_price, 2)}$", delta=f"{round(percent, 2)}%")

with candle_page:
    left, right = streamlit.columns([1, 3], gap="medium")
    # Input
    with left, streamlit.container(border=True):
        streamlit.write("### Company:")
        
        candle_company = streamlit.text_input("Campany name", "AAPL", key=f"Company")

        start_date_candle, end_date_candle = streamlit.slider(
            label = "Date range",
            key = "range2",
            min_value = min_date,
            max_value = actual_date,
            value = (min_date, actual_date),
            format = "DD/MM/YY"
        )

    with right, streamlit.container(border=True):
        with streamlit.spinner('Pobieranie danych z giełdy...'):
            data_candle = download_data(candle_company, start_date_candle, end_date_candle)
        
            candles_df = data_candle.xs(candle_company, axis=1, level=1)
            lenght = candles_df.size/5
            print(lenght)
            bar_width = (1500 / lenght)
            # candles_df = data_candle['Close']
            # candles_df.columns = ["Close"]

            candles_df['Open'] = data_candle['Open']
            candles_df["Height"] = abs(candles_df['Close'] - candles_df['Open'])
            candles_df["y"] = candles_df[['Open', 'Close']].min(axis=1)
            candles_df["Color"] = candles_df.apply(lambda row: 'green' if row['Close'] >= row['Open'] else 'red', axis=1)
            source = candles_df.reset_index()

            # Tworzymy wykres
            chart = altair.Chart(source).mark_bar(
                size=bar_width
            ).encode(
                x='Date',
                y= altair.Y('Open', scale=altair.Scale(zero=False), title='Cena (USD)'),
                y2='Close',
                color=altair.Color('Color', scale=None),
                tooltip=['Date', 'Open', 'Close']
            ).interactive()

        streamlit.altair_chart(chart, use_container_width=True)
          
        
