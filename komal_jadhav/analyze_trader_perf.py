import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Setup aesthetics
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def analyze_trader_performance():
    print("--- Loading Datasets ---")
    try:
        trader_df = pd.read_csv('historical_data.csv')
        sentiment_df = pd.read_csv('fear_greed_index.csv')
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print("\n--- Cleaning & Preprocessing ---")
    
    # 1. Convert trader timestamps to daily dates
    # Assuming Timestamp is in milliseconds (e.g., 1.73e12)
    trader_df['date'] = pd.to_datetime(trader_df['Timestamp'], unit='ms').dt.date
    
    # 2. Convert sentiment dates
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date
    
    # 3. Handle missing Closed PnL (ensure it's numeric)
    trader_df['Closed PnL'] = pd.to_numeric(trader_df['Closed PnL'], errors='coerce').fillna(0)
    trader_df['Size USD'] = pd.to_numeric(trader_df['Size USD'], errors='coerce').fillna(0)
    
    # Merge datasets
    merged_df = pd.merge(trader_df, sentiment_df, on='date', how='inner')
    print(f"Merged Data: {len(merged_df)} rows.")

    if merged_df.empty:
        print("Warning: Merged data is empty! Check timestamp overlaps.")
        return

    print("\n--- Performance Metrics by Sentiment ---")
    
    # Group by classification
    sentiment_perf = merged_df.groupby('classification').agg({
        'Closed PnL': ['mean', 'median', 'sum', 'count'],
        'Size USD': 'mean',
        'value': 'mean'
    })
    print(sentiment_perf)

    # Calculate Win rate per sentiment
    merged_df['is_win'] = merged_df['Closed PnL'] > 0
    win_rate = merged_df.groupby('classification')['is_win'].mean() * 100
    print("\nWin Rate per Sentiment (%):")
    print(win_rate)

    print("\n--- Visualizing Findings ---")
    
    # 1. Boxplot: PnL Distribution by Sentiment
    plt.figure()
    # Limit extreme outliers for readability
    pnl_cap = merged_df['Closed PnL'].quantile(0.95)
    pnl_floor = merged_df['Closed PnL'].quantile(0.05)
    filtered_df = merged_df[(merged_df['Closed PnL'] <= pnl_cap) & (merged_df['Closed PnL'] >= pnl_floor)]
    
    sns.boxplot(x='classification', y='Closed PnL', data=filtered_df, order=['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed'])
    plt.title('PnL Distribution by Market Sentiment (Outliers Capped)')
    plt.xlabel('Bitcoin Sentiment')
    plt.ylabel('Closed PnL (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('pnl_by_sentiment.png')
    
    # 2. Bar Chart: Win Rate by Sentiment
    plt.figure()
    win_rate_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    # Filter only available classifications in data
    available_order = [c for c in win_rate_order if c in win_rate.index]
    sns.barplot(x=available_order, y=win_rate[available_order])
    plt.title('Trader Win Rate per Sentiment Classification')
    plt.ylabel('Win Rate (%)')
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig('win_rate_by_sentiment.png')

    # 3. Scatter: Sentiment Value vs. Trade Size
    plt.figure()
    sns.scatterplot(x='value', y='Size USD', data=merged_df, alpha=0.3)
    plt.title('Market Sentiment Value vs. Trade Size')
    plt.xlabel('Sentiment Value (0=Extreme Fear, 100=Extreme Greed)')
    plt.ylabel('Trade Size (USD)')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('sentiment_vs_size_scatter.png')

    print("\nAnalysis complete. Results and plots generated.")
    
    # Output findings to a summary text
    with open('analysis_summary.txt', 'w') as f:
        f.write("TRADER PERFORMANCE VS SENTIMENT SUMMARY\n")
        f.write("=========================================\n")
        f.write(f"Total Trades Analyzed: {len(merged_df)}\n\n")
        f.write("Win Rate by Sentiment:\n")
        f.write(win_rate.to_string())
        f.write("\n\nMedian PnL by Sentiment:\n")
        f.write(sentiment_perf['Closed PnL']['median'].to_string())

if __name__ == "__main__":
    analyze_trader_performance()
