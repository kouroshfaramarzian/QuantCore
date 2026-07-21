from src.core.exceptions import DataError

try:

    raise DataError("Dataset not found.")

except DataError as e:

    print(e)