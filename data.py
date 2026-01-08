import yfinance
import pandas

def download_data(companies, start_date, end_date):
    print("Downloading Data...")
    
    data = yfinance.download(companies, start_date, end_date)
    data.fillna(method = "ffill", inplace=True)

    print("Data downloaded!")
    return data

def all_movers(period = "Month"):
    companies_list = [
    # --- Magnificent 7 & Big Tech ---
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
    # --- Tech & Semiconductors ---
    "AVGO", "ORCL", "CRM", "ADBE", "AMD", "QCOM", "CSCO", "INTU", "IBM", "AMAT", "NOW", "TXN",
    # --- Finance & Payments ---
    "BRK-B", "JPM", "V", "MA", "BAC", "WFC", "MS", "AXP", "BLK",
    # --- Healthcare & Pharma ---
    "LLY", "UNH", "JNJ", "MRK", "ABBV", "TMO", "AMGN", "PFE",
    # --- Consumer & Retail ---
    "WMT", "PG", "COST", "HD", "KO", "PEP", "MCD", "DIS", "NKE", "PM",
    # --- Energy & Industry ---
    "XOM", "CVX", "GE", "CAT", "LIN",
    # --- Media & Telecom ---
    "NFLX", "TMUS", "CMCSA", "VZ"
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
                # "ChangeText": str(round(percent, 2))+"%",
                "Change" : round(percent, 2),
                "Start Price" : round(start_price, 2),
                "End Price" : round(end_price, 2)
            })

        except:
            continue

    df_result = pandas.DataFrame(result)
    # print(df_result.head(5))
    return df_result

def download_info(name):

    stock_info = yfinance.Ticker(name).info

    return stock_info

def correlation(companies):
    print("Downloading Data...")

    data = yfinance.download(companies, period="5y")
    data.fillna(method = "ffill", inplace=True)

    if 'Close' in data:
        df_close = data['Close']
    else:
        df_close = data

    corr_matrix = df_close.pct_change().corr()

    corr_matrix.index.name = "Ticker1"
    corr_matrix.columns.name = "Ticker2"
    
    # print(corr_matrix)
    corr_data = corr_matrix.stack().reset_index(name="Correlation")
    print("Data downloaded!")
    return corr_data
