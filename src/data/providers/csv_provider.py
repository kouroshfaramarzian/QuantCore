def load_data(
    self,
    symbol: str = "",
    timeframe: str = "",
    start=None,
    end=None,
) -> pd.DataFrame:

    if not self.file_path.exists():
        raise FileNotFoundError(f"{self.file_path} not found")

    return pd.read_csv(self.file_path)