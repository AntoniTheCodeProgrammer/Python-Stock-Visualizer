import yfinance
import pandas

def download_data(companies, start_date, end_date):
    print("Pobieranie danych...")
    
    data = yfinance.download(companies, start_date, end_date)
    data.fillna(method = "ffill", inplace=True)

    return data

def all_movers(period = "Month"):
    companies_list = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX",
        "AMD", "INTC", "IBM", "ORCL", "CRM", "ADBE",
        "DIS", "NKE", "SBUX", "MCD", "KO", "PEP",
        "JPM", "BAC", "V", "MA", "PYPL"
    ]

    converter = {"Day" : "2d", "Week" : "5d", "Month" : "1mo", "Year" : "1y"}
    updated_period = converter[period]

    data = yfinance.download(
        companies_list, period=updated_period, group_by='ticker'
    )

    result = []

    for company in companies_list:
        try:
            data_company = data[company]["Close"]
            
            start_price = data_company.iloc[0]
            end_price = data_company.iloc[-1]
            percent = (end_price - start_price)/start_price*100

            result.append({
                "Name" : company,
                "Change" : round(percent, 2),
                "Start Price" : round(start_price, 2),
                "End Price" : round(end_price, 2)
            })

        except:
            continue

    df_result = pandas.DataFrame(result)
    # print(df_result.head(5))
    return df_result
