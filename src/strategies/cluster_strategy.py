import pandas as pd
import numpy as np
import pybroker
from pybroker import YFinance, Strategy, StrategyConfig

pybroker.enable_data_source_cache('ranking_and_pos_sizing')

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

def buy_baseline(ctx):
    # always hold a long position from begin to end
    ctx.buy_shares = ctx.calc_target_shares(1)

def buy_highest_signal(ctx):
    # If there are no long positions across all tickers being traded:
    if not tuple(ctx.long_positions()):
        # ctx.calc_target_shares(position) seems to work, but config max long positions seems not working
        ctx.buy_shares = ctx.calc_target_shares(1)
        ctx.hold_bars = 3
        ctx.score = ctx.signal[-1]

# 
def baseline_strategy(demo_data_source, baseline_symbol, start_date, end_date):
    df = pd.read_csv(demo_data_source)
    df = df[df.symbol==baseline_symbol].copy()
    df['date'] = pd.to_datetime(df['date'])
    
    strategy = Strategy(df, start_date, end_date)
    strategy.add_execution(buy_baseline, [baseline_symbol])
    return strategy

def ml_strategy(demo_data_source, position_num, start_date, end_date):
    df = pd.read_csv(demo_data_source).copy()
    df['date'] = pd.to_datetime(df['date'])
    stock_pool = df.symbol.unique().tolist()
    # print('stock_pool: \t', stock_pool)
    stock_num = len(stock_pool)

    pybroker.register_columns('signal')
    pybroker.enable_data_source_cache('ranking_and_pos_sizing')
    config = StrategyConfig(max_long_positions = position_num)
    strategy = Strategy(df, start_date, end_date, config)
    strategy.add_execution(buy_highest_signal, stock_pool)
    return strategy

def create_strategy(demo_data_source, cluster_n, start_date, end_date):
    # load data from local storage, csv file, selected by cluster_n
    df = pd.read_csv(demo_data_source)
    df = df[df.cluster==cluster_n].copy()
    df['date'] = pd.to_datetime(df['date'])
    stock_pool = df.symbol.unique().tolist()
    stock_num = len(stock_pool)
    pybroker.register_columns('signal')
    print('df_cluster: \t', df.head())
    # maximum number of long positions
    config = StrategyConfig(max_long_positions = 5 if int(stock_num/2)>=5 else 2)

    strategy = Strategy(df, start_date, end_date, config)
    strategy.add_execution(buy_highest_signal, stock_pool)
    
    return strategy
