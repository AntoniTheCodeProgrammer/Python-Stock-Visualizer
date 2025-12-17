import yfinance as yf

def download_data(companies, start_date, end_date):
    print("Pobieranie danych...")
    
    data = yf.download(companies, start_date, end_date)
    data.fillna(method = "ffill", inplace=True)

    return data