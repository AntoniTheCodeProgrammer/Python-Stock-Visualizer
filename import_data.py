import yfinance as yf

# 1. Pobieramy dane dla Apple (ticker: AAPL)
print("Pobieranie danych...")
data = yf.download("AAPL", start="2023-01-01", end="2023-12-31")

# 2. Wyświetlamy pierwsze 5 wierszy, żeby zobaczyć czy coś przyszło
print(data.head())