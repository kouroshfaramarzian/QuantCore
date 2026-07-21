from src.data.providers.csv_provider import CSVProvider
from src.data.validator import DataValidator

provider = CSVProvider("datasets/test.csv")

provider.connect()

df = provider.load_data()

print(df)

print(DataValidator.validate(df))