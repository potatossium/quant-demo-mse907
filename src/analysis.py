import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_results(results):
    trades = results.trades
    pnl = trades.groupby('symbol').agg({'pnl': 'sum'})
    pnl.plot(kind='bar')
    plt.title('PnL by Stock')
    plt.xlabel('Stock')
    plt.ylabel('PnL')
    plt.show()

def plot_ml_vs_baseline(ml_results, model_name, baseline_results):
    # 
    ml_results_df = ml_results.portfolio.copy()
    ml_results_df['return'] = ml_results_df['market_value'].pct_change().cumsum().fillna(0)
    baseline_results_df = baseline_results.portfolio
    baseline_results_df['return'] = baseline_results_df['market_value'].pct_change().cumsum().fillna(0)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=ml_results_df, x=ml_results_df.index, y='return', label=model_name)
    sns.lineplot(data=baseline_results_df, x=baseline_results_df.index, y='return', label='Baseline')
    plt.title('Cumulative Returns: ' + model_name +' vs Baseline')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()

def plot_cluster_vs_baseline(cluster_results, cluster_num, baseline_results):
    # 
    cluster_results_df = cluster_results.portfolio.copy()
    cluster_results_df['return'] = cluster_results_df['market_value'].pct_change().cumsum().fillna(0)
    baseline_results_df = baseline_results.portfolio
    baseline_results_df['return'] = baseline_results_df['market_value'].pct_change().cumsum().fillna(0)
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=cluster_results_df, x=cluster_results_df.index, y='return', label='Cluster '+str(cluster_num))
    sns.lineplot(data=baseline_results_df, x=baseline_results_df.index, y='return', label='Baseline')
    plt.title('Cumulative Returns: Cluster vs Baseline')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()