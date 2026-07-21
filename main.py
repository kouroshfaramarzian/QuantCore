from src.data.providers.csv_provider import CSVProvider


provider = CSVProvider("datasets/test.csv")

print(provider.connect())

df = provider.load_data()

print(df)