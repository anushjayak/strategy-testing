from trading_system.momentum_strategy import MomentumStrategy

class Backtesting:
    def __init__(self, strategy, initial_capital):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0
        self.positions = []
        self.portfolio_value = []

    def run_backtest(self):
        pass

    def performative_metrics(self):
        pass

    def plot_results(self):
        pass

    def scoring(self):
        pass



