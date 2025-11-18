from import_data import download_data

while True:
    n = input("Ile chcesz spółek? (1-5) \nOdp: ")
    if n.isnumeric():
        n = int(n)
        if n in range(1,5):
            break

companies = []
for i in range(n):
    companies.append(input(f"Spółka {i+1}: "))

print(download_data(companies))