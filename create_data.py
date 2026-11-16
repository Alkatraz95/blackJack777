import csv
import json

import pandas as pd

operations = [
    {
        "id": 87320,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "amount": "31957.58",
        "currency_name": "RUB",
        "description": "Перевод организации",
    },
    {
        "id": 154927927,
        "state": "CANCELED",
        "date": "2019-10-17T21:51:29.076402",
        "amount": "67314.70",
        "currency_name": "USD",
        "description": "Перевод с карты на карту",
    },
    {
        "id": 64914,
        "state": "PENDING",
        "date": "2019-03-23T01:38:48.977053",
        "amount": "48523.23",
        "currency_name": "RUB",
        "description": "Открытие вклада",
    },
    {
        "id": 598736,
        "state": "EXECUTED",
        "date": "2020-01-15T14:12:33.003511",
        "amount": "564231.43",
        "currency_name": "RUB",
        "description": "Покупка в «Ленте»",
    },
]

# JSON
with open("data/operations.json", "w", encoding="utf-8") as f:
    json.dump(operations, f, ensure_ascii=False, indent=2)

# CSV — разделитель ';' как ожидает readers.py
with open("data/operations.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(operations[0].keys()), delimiter=";")
    writer.writeheader()
    writer.writerows(operations)

# XLSX
pd.DataFrame(operations).to_excel("data/operations.xlsx", engine="openpyxl", index=False)

print("Готово: 4 операции записаны в json, csv и xlsx")

