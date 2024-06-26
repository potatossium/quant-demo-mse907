# from src.strategy import create_strategy
from src.strategies.cluster_strategy import create_strategy, baseline_strategy, ml_strategy
from src.config import START_DATE, END_DATE, DEMO_DATA_SOURCE, CLUSTERS

def run_backtest(cluster_num=0):
    strategy = create_strategy(DEMO_DATA_SOURCE, CLUSTERS[cluster_num], START_DATE, END_DATE)
    result = strategy.backtest(warmup=20)
    return result

def ml_backtest():
    strategy = ml_strategy("data/processed/factors1_y_without_cluster_signal2.csv", 10, START_DATE, END_DATE)
    result = strategy.backtest(warmup=20)
    return result

def baseline_backtest():
    strategy = baseline_strategy(DEMO_DATA_SOURCE, 'SPY', START_DATE, END_DATE)
    result = strategy.backtest(warmup=20)
    return result
