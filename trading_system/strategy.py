class Strategy:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self, ticker, start_date, end_date):
        pass

    def calculate_indicators(self):
        pass

    def generate_signals(self):
        pass

