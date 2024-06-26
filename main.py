# from pybroker import YFinance

# yfinance = YFinance()
# df = yfinance.query(['AAPL', 'MSFT'], start_date='12/1/2021', end_date='3/1/2022')
# print(df.head())
import pandas as pd
from src.backtest import run_backtest, baseline_backtest, ml_backtest
from src.analysis import plot_results, plot_cluster_vs_baseline, plot_ml_vs_baseline
import pybroker

def main():
    # pybroker.enable_data_source_cache('ranking_and_pos_sizing')

    # results = ml_backtest()
    # results.portfolio.to_csv('portfolio_adaboost2_10.csv', index=True)
    # print(results.portfolio.tail())
    # print("results.trades: ")
    # print(results.trades[:20])
    # baseline_results = baseline_backtest()
    # plot_ml_vs_baseline(results, 'AdaBoost', baseline_results)
    for cluster_num in range(0, 5):
        results = run_backtest(cluster_num)
        # results = ml_backtest()
        baseline_results = baseline_backtest()
        print("results.trades: ")
        print(results.trades)
        # results.portfolio.to_csv('portfolio_'+str(cluster_num)+'_.csv', index=True)
        # results.trades.to_csv('temp_trades.csv', index=False)
        print("results.metrics\t", results.metrics_df)
        # print("baseline.metrics\t", baseline_results.metrics_df)
        # plot_results(results)
        # plot_cluster_vs_baseline(results, cluster_num, baseline_results)
        # plot_ml_vs_baseline(results, 'AdaBoost', baseline_results)

if __name__ == '__main__':
    main()