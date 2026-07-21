from src.data.pipeline import DataPipeline
from src.data.providers.csv_provider import CSVProvider


provider = CSVProvider("datasets/test.csv")

pipeline = DataPipeline(provider)

df = pipeline.run()

print(df)