# Trader Performance vs. Market Sentiment Analysis (Hyperliquid)

This project explores the correlation between Bitcoin market sentiment (Fear & Greed Index) and the actual performance of traders on the Hyperliquid platform. By analyzing a dataset of over **184,000 trades**, we uncover how extreme market emotions impact profitability, win rates, and trading volume.

## 📊 Key Insights
- **Extreme Greed = Highest Win Rate**: Traders saw a **49.0%** success rate during extreme exuberance.
- **The "Neutral Trap"**: Performance was lowest during **Neutral** sentiment (**31.7%** win rate), suggesting choppy markets are the most difficult to trade.
- **Profitability Peak**: While Extreme Greed had the highest win *rate*, standard **Greed** yielded the highest average profit per trade (**$87.89**).
- **Fear-Driven Volume**: The majority of trade activity (**133k+ trades**) occurred during **Fear** phases, indicating high rebalancing/defensive activity during downturns.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Libraries: `pandas`, `matplotlib`, `seaborn`, `numpy`

### Installation
```bash
pip install pandas matplotlib seaborn numpy
```

### Running the Analysis
To regenerate the statistics and visualizations:
```bash
python analyze_trader_perf.py
```

## 📂 Project Structure
- `historical_data.csv`: Source trader data from Hyperliquid.
- `fear_greed_index.csv`: Daily Bitcoin sentiment classifications.
- `analyze_trader_perf.py`: Main processing and visualization script.
- `analysis_summary.txt`: Text-based summary of win rates and median PnL.
- `pnl_by_sentiment.png`: Boxplot showing profit distribution across sentiment levels.
- `win_rate_by_sentiment.png`: Comparison of successful trade percentages.
- `sentiment_vs_size_scatter.png`: Correlation between sentiment level and trade volume.

## 📈 Visualizations
The analysis generates three primary charts:
1. **PnL Distribution**: Highlighting how profit variance changes from Extreme Fear to Extreme Greed.
2. **Win Rate Analysis**: Comparing the percentage of winning trades (PnL > 0) per classification.
3. **Sentiment vs. Size**: Identifying if traders "size up" during specific sentiment phases.

---
*Created as part of the Hyperliquid Trader Performance Assignment.*
