import matplotlib.pyplot as plt
class Backtest:
    def __init__(self,trades_dates:list,balance_history:list,recent_high:float):
        self.win_count=0
        self.loss_count=0
        self.break_even_count=0
        self.trade_count=0
        self.total_win_amount=0
        self.total_loss_amount=0
        self.max_drawdown=0
        self.trades_dates=trades_dates
        self.trades:list=[]
        self.live_trades:list=[]
        self.balance_history=balance_history
        self.recent_high=recent_high

    def print_summary(self):
        
        win_rate = ((self.win_count / (self.win_count+self.loss_count)) * 100) if (self.win_count+self.loss_count) > 0 else 0.0
        
        gross_win = self.total_win_amount
        gross_loss = abs(self.total_loss_amount) 
        
        net_profit = gross_win - gross_loss
        profit_factor = (gross_win / gross_loss) if gross_loss > 0 else float('inf')
        
        initial_balance = self.balance_history[0] if self.balance_history else 0.0
        final_balance = self.balance_history[-1] if self.balance_history else 0.0
        total_return = ((final_balance - initial_balance) / initial_balance * 100) if initial_balance > 0 else 0.0

        log_output = f"""
{'='*50}
             BACKTEST RESULTS SUMMARY             
{'='*50}

[ PERFORMANCE METRICS ]
Total Trades       : {self.trade_count}
Wins               : {self.win_count}
Losses             : {self.loss_count}
Break-Evens        : {self.break_even_count}
Win Rate           : {win_rate:.2f}%

[ FINANCIALS ]
Initial Balance    : ${initial_balance:,.2f}
Final Balance      : ${final_balance:,.2f}
Net Profit         : ${net_profit:,.2f} ({total_return:+.2f}%)
Average Win        : ${gross_win/self.win_count}
Average Loss       : ${gross_loss/self.loss_count}
Gross Wins         : ${gross_win:,.2f}
Gross Losses       : -${gross_loss:,.2f}
Profit Factor      : {profit_factor:.2f}
Max Drawdown       : {self.max_drawdown:.2f}%

[ STATUS ]
Completed Trades   : {len(self.trades)}
Live Trades Left   : {len(self.live_trades)}

{'='*50}
"""
        print(log_output)
    def draw_graph(self):

        # PLOTTING the BALANCE
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(self.balance_history)), self.balance_history, label='Account Balance', color='green', linewidth=1)

        # Formatting
        plt.title(f'Account Balance Growth - Final: ${round(self.balance_history[-1], 2)}')
        plt.xlabel('Date')
        plt.ylabel('Balance (USD)')
        plt.axhline(y=self.balance_history[0], color='r', linestyle='--', label='Starting Balance')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.tight_layout()

        # Show the plot
        plt.show()
        