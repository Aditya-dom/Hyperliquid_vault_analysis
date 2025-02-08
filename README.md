# HyperLiquid Vault Analyzer

A Streamlit application that analyzes HyperLiquid vaults, providing metrics like Sharpe ratio, Sortino ratio, drawdown, and more.

## Features

-   Real-time vault data analysis
-   Automated daily cache updates
-   Multiple filtering options
-   Key metrics calculation (Sharpe ratio, Sortino ratio, Max drawdown)
-   Interactive UI with Streamlit

## Deployment

The application is automatically deployed to Streamlit Cloud and the cache is updated daily. You can access it at:
https://hyperliquid-vault-analyzer.streamlit.app

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/aditya-dom/hyperliquid-vault-analysis.git
cd hyperliquid-vault-analyzer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run main.py
```

### Deployment on Streamlit Cloud

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Add your Streamlit credentials as a GitHub secret named `STREAMLIT_CREDENTIALS`
5. Deploy!

## Cache System

The application uses a caching system that:

-   Updates automatically every 24 hours via GitHub Actions
-   Stores vault data to minimize API calls
-   Maintains historical data for analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
