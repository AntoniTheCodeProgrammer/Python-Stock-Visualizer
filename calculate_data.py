from import_data import download_data
import numpy 
import pandas
import matplotlib.pyplot as plt
import streamlit
import altair

daily_returns = close_prices.pct_change().dropna()

sma_20 = close_prices.rolling(window = 20).mean().dropna()

logarytm = numpy.log(close_prices / close_prices.shift(1)).dropna()

daily_sigma = logarytm[-21:].std()
odchylenie = daily_sigma * numpy.sqrt(252)



# WYDRUK WSKAŹNIKÓW
# print("--- Ostatnie 21 dni danych ---")
# print(data[-21:])
# print("\n--- Dzienne Stopy Zwrotu ---")
# print(daily_returns)
# print("\n--- Logarytmiczne Stopy Zwrotu ---")
# print(logarytm)
# print("\n--- 20-dniowa Średnia Krocząca ---")
# print(sma_20)
# print("\n--- Roczna Zmienność (na podstawie ostatnich 21 dni) ---")
# print(odchylenie)

aapl_returns = daily_returns['AAPL'].dropna() 

plt.figure(figsize=(10, 6))
plt.hist(aapl_returns, bins = 50, edgecolor='black', color='skyblue') 
plt.savefig("wykres1.png")

plt.figure(figsize=(10, 6))

# plt.plot(
#     close_prices.index,
#     close_prices["AAPL"], # Poprawny dostęp do kolumny AAPL
#     color="blue",
#     linewidth=1.5,
#     label='Cena Zamknięcia'
# )
# # Wykres SMA 20
# plt.plot(
#     sma_20.index,
#     sma_20["AAPL"],
#     color="orange",
#     linewidth=2,
#     label='SMA 20 Dni'
# )
# plt.legend()
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.savefig("wykres2.png")

streamlit.write("""
# My first app
Hello *world!*
""")

streamlit.line_chart(aapl_returns)

columns = {
    "Close": close_prices["AAPL"], 
    "SMA": sma_20["AAPL"]
}
df = pandas.DataFrame(columns)
streamlit.line_chart(df)

# streamlit.pyplot(candle)




# WYKRES SWIECOWY

candles_df = data['Close']['AAPL'].to_frame(name='Close').tail(45) # Przykładowe uproszczenie
candles_df['Open'] = data['Open']['AAPL'].tail(45)

candles_df["Height"] = abs(candles_df['Close'] - candles_df['Open'])

candles_df["y"] = candles_df[['Open', 'Close']].min(axis=1)

candles_df["Color"] = candles_df.apply(lambda row: 'green' if row['Close'] >= row['Open'] else 'red', axis=1)

source = candles_df.reset_index()

# Tworzymy wykres
chart = altair.Chart(source).mark_bar().encode(
    x='Date',
    y= altair.Y('Open', scale=altair.Scale(zero=False), title='Cena (USD)'),
    y2='Close',
    color=altair.Color('Color', scale=None),
    tooltip=['Date', 'Open', 'Close']
).interactive()

streamlit.altair_chart(chart, use_container_width=True)



import altair as alt


source['Change'] = source['Close'] - source['Open']


import altair as alt

# --- KROK 1: Obliczenie kolumny 'Change' ---
# To jest kluczowe! Musimy wiedzieć, JAK DUŻA była zmiana,
# żeby przypisać jej odpowiednio intensywny kolor.
# Zakładam, że Twoja ramka danych nazywa się 'source'
# i ma kolumny 'Close' oraz 'Open'.
source['Change'] = source['Close'] - source['Open']

# --- KROK 2: Przygotowanie skali kolorów ---
# Znajdujemy największy spadek i największy wzrost, żeby ustawić granice gradientu.
min_change = source['Change'].min()
max_change = source['Change'].max()

# To są "punkty kontrolne" naszej skali.
domain_ = [min_change, 0, max_change]
# To są kolory odpowiadające tym punktom:
# - min_change -> ciemnoczerwony ('darkred')
# - 0 -> jasnoszary ('lightgray') - neutralny środek
# - max_change -> ciemnozielony ('darkgreen')
range_ = ['darkred', 'lightgray', 'darkgreen']

# --- KROK 3: Tworzenie wykresu z gradientem ---
chart = alt.Chart(source).mark_bar(
    # Użyj swojej zmiennej do obliczenia szerokości, jeśli chcesz
    # np. size = (700 / len(source)) * 0.8
    size=10  # Przykładowa stała szerokość
).encode(
    x='Date',
    y=alt.Y('Open', scale=alt.Scale(zero=False), title='Cena (USD)'),
    y2='Close',
    # ---> GŁÓWNA ZMIANA JEST TUTAJ <---
    color=alt.Color(
        'Change',  # Używamy nowej, obliczonej kolumny 'Change'
        scale=alt.Scale(
            domain=domain_,  # Nasze punkty: [min, 0, max]
            range=range_,    # Nasze kolory: [czerwony, szary, zielony]
            type='linear'    # 'linear' tworzy płynny gradient między punktami
        ),
        title='Zmiana Ceny (Gradient)'
    ),
    # Dodajemy 'Change' do dymka, żeby było widać dokładną wartość
    tooltip=['Date', 'Open', 'Close', alt.Tooltip('Change', format='.2f')]
).interactive()

# W Twojej aplikacji Streamlit użyj:
# st.altair_chart(chart, use_container_width=True)
