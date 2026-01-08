from data import download_data, all_movers, download_info, correlation
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
import datetime

actual_date = datetime.date.today()
min_date = actual_date.replace(year=actual_date.year - 5)

st.set_page_config(layout="wide")

main_page, changes_page, correlation_heatmap_page, single_company_page = st.tabs(["Main", "Changes Page", "Correlation Heatmap", "Single Company"])


with main_page, st.spinner("Site loading..."):
    left, right = st.columns([1, 3])
    # Input
    with left, st.container(border=True):
        st.write("### DATA:")
        number = 2
        number = st.slider("How many campanies?", 1, 5, 2)
        companies = ["AAPL", "GOOG"]

        start_date, end_date = st.slider(
            label = "Date range",
            key = "range1",
            min_value = min_date,
            max_value = actual_date,
            value = (datetime.date(2021,3,12), datetime.date(2023,5,11)),
            format = "DD/MM/YY"
        )

        for i in range(0, number):
            if  i < len(companies): 
                ticker = st.text_input("Campany name", companies[i], key=f"Company{i}")
                companies[i] = ticker
            else: 
                ticker = st.text_input("Campany name", "", key=f"Company{i}")
                companies.append(ticker)
        for i in range(5-number):
            st.space("large")

    with st.spinner(f"Loading data..."):
        companies = companies[:number]
        data = download_data(companies, start_date, end_date)
        close_prices = data["Close"]

    # Main chart
        with right:
            with st.container(border=True):
                st.line_chart(close_prices)

            with st.container(border=True):
                st.write("Price change:")

                borders = 0
                for i in range(number):
                    if companies[i] != "":
                        borders += 1

                stock_change = st.columns(len([comp for comp in companies if comp.strip() != ""]), border=True)
                for i in range(number):
                    if companies[i] != "":
                        start_price = data.head(1)["Close"][companies[i]].values[0]
                        end_price = data.tail(1)["Close"][companies[i]].values[0]
                        percent = (end_price - start_price)/start_price*100
                        stock_change[i].metric(label=companies[i], value=f"{round(end_price, 2)}$", delta=f"{round(percent, 2)}%")
          
with changes_page, st.spinner("Site loading..."):
    left, right = st.columns([1, 3])

    with st.container(border=True):
        st.write("### Actual Changes")

        options = ["Day", "Week", "Month", "Year"]

        selection = st.segmented_control(
            "Period", options, selection_mode="single", default="Month"
        )

    with st.spinner(f"Loading data..."):    
        data_changes = all_movers(selection)    
        data_sorted = data_changes.sort_values(by="Change", ascending=False)
        
        top_gainers = data_sorted.head(5)
        top_losers = data_sorted.tail(5).sort_values(by="Change", ascending=True)
        
        col1, col2 = st.columns(2)

        with col1, st.container(border=True):
            st.success("Top Gainers")
            st.table(top_gainers.set_index("Name").style.format({
                "Change": "{:.2f}%",   
            }))

        with col2, st.container(border=True):
            st.error("Top Losers")
            st.table(top_losers.set_index("Name").style.format({
                "Change": "{:.2f}%",   
            }))


        with st.container(border=True):
            chart_data = data_sorted.reset_index()
            x_axis_column = 'Name' if 'Name' in chart_data.columns else 'index'

            max_change = chart_data["Change"].iloc[0]
            min_change = chart_data["Change"].iloc[-1]

            domain_ = [min_change, 0, max_change]

            range_ = ['red', 'white', 'green']

            chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X(x_axis_column, sort='-y', title='Name'),
                y=alt.Y('Change', title='Change (%)'),
        
                color=alt.Color(
                    'Change',
                    scale=alt.Scale(
                        domain=domain_,
                        range=range_,
                        type='linear'
                    ),
                ),

                tooltip=[x_axis_column, alt.Tooltip('Change', format='.2f')]
            ).interactive()

            st.altair_chart(chart)

with correlation_heatmap_page, st.spinner("Site loading..."):
    left, right = st.columns([1, 3])
    # Input
    with left, st.container(border=True):
        st.write("### DATA:")
        corr_number = 2
        corr_number = st.slider("How many campanies?", 2, 10, 3, key="corr_slider")
        corr_companies = ["AAPL", "GOOG", "MSFT"]

        for i in range(0, corr_number):
            if  i < len(corr_companies): 
                corr_ticker = st.text_input("Campany name", corr_companies[i], key=f"corr_Company{i}")
                corr_companies[i] = corr_ticker
            else: 
                corr_ticker = st.text_input("Campany name", "", key=f"corr_Company{i}")
                corr_companies.append(corr_ticker)

    with right, st.container(border=True):
        with st.spinner("Calculating correlation..."):
            data_corr = correlation(corr_companies)
            st.write("### Correlation Matrix")
            
            data_corr.columns = ['Ticker1', 'Ticker2', 'Correlation']
            
            base = alt.Chart(data_corr).encode(
                x=alt.X('Ticker1', title=None),
                y=alt.Y('Ticker2', title=None)
            )
            
            heatmap = base.mark_rect().encode(
                color=alt.Color(
                    'Correlation',
                    scale=alt.Scale(scheme='redyellowgreen', domain=[-1, 1]),
                    title="Correlation"
                ),
                tooltip=['Ticker1', 'Ticker2', alt.Tooltip('Correlation', format='.2%')]
            )

            text = base.mark_text().encode(
                text=alt.Text('Correlation', format='.0%'),
                color=alt.condition(
                    alt.datum.Correlation > 0.5, 
                    alt.value('black'),
                    alt.value('white')
                )
            )

            final_chart = (heatmap + text).properties(
                width=600,
                height=500
            ).interactive()

            st.altair_chart(final_chart, use_container_width=True)
                
            st.caption("Logic: 100% (Green) = Strong Positive Correlation -> -100% (Red) = Strong Negative Correlation.")

with single_company_page, st.spinner("Site loading..."):
    left, right = st.columns([1, 3])
    # Input
    with left, st.container(border=True):
        st.write("### Company:")
        
        single_company = st.text_input("Campany name", "AAPL", key=f"Company")

        start_date_candle, end_date_candle = st.slider(
            label = "Date range",
            key = "range2",
            min_value = min_date,
            max_value = actual_date,
            value = (min_date, actual_date),
            format = "DD/MM/YY"
        )


    with right, st.container(border=True), st.spinner(f"Loading data..."):
        with st.spinner('Pobieranie danych z giełdy...'):
            data_candle = download_data(single_company, start_date_candle, end_date_candle)
        
            candles_df = data_candle.xs(single_company, axis=1, level=1)
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
            chart = alt.Chart(source).mark_bar(
                size=bar_width
            ).encode(
                x='Date',
                y= alt.Y('Open', scale=alt.Scale(zero=False), title='Cena (USD)'),
                y2='Close',
                color=alt.Color('Color', scale=None),
                tooltip=['Date', 'Open', 'Close']
            ).interactive()

        st.altair_chart(chart, use_container_width=True)   
        

    with st.expander(f"Show info of stock", expanded=True):
        info_data = download_info(single_company)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sector", info_data.get('sector', 'No Data'))
            st.metric("", info_data.get('fullTimeEmployees', 'No Data'))
            st.metric("P/E Ratio", info_data.get('trailingPE', '-'))
        
        with col2:
            st.write("**Description:**")
            st.caption(info_data.get('longBusinessSummary', 'No description.'))
            st.write(f"**WWW site:** {info_data.get('website', '-')}")