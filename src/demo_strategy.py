import pandas as pd
import numpy as np

from pybroker import YFinance, Strategy, StrategyConfig
# from pybroker.indicator import macd

def buy_low(ctx):
    # If shares were already purchased and are currently being held, then return.
    if ctx.long_pos():
        return
    # If the latest close price is less than the previous day's low price,
    # then place a buy order.
    if ctx.bars >= 2 and ctx.close[-1] < ctx.low[-2]:
        # Buy a number of shares that is equal to 25% the portfolio.
        ctx.buy_shares = ctx.calc_target_shares(0.25)
        # Set the limit price of the order.
        ctx.buy_limit_price = ctx.close[-1] - 0.01
        # Hold the position for 3 bars before liquidating (in this case, 3 days).
        ctx.hold_bars = 3

# def macd_signal(ctx):
#     macd_line, signal_line, _ = macd(ctx.close, fastperiod=12, slowperiod=26, signalperiod=9)
#     if macd_line[-1]>signal_line[-1] and macd_line[-2] <= signal_line[-2]:
#         # Buy a number of shares that is equal to 50% the portfolio.
#         ctx.buy_shares = ctx.calc_target_shares(0.5)
#         ctx.hold_bars = 3

def volume_signal(ctx):
    if not tuple(ctx.long_positions()):
        ctx.buy_shares = ctx.calc_target_shares(0.5)
        ctx.hold_bars = 2
        ctx.score = ctx.volume[-1]

def create_strategy(stock_pool_macd, stock_pool_volume, start_date, end_date):
    config = StrategyConfig(max_long_positions=2)
    strategy = Strategy(YFinance(), start_date, end_date, config)
    
    strategy.add_execution(buy_low, stock_pool_macd)
    strategy.add_execution(volume_signal, stock_pool_volume)
    
    return strategy
