"""
Konfigurasi untuk Crypto Arbitrage Scanner
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Exchange API Keys (opsional untuk public data)
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_SECRET = os.getenv('BINANCE_SECRET', '')

BYBIT_API_KEY = os.getenv('BYBIT_API_KEY', '')
BYBIT_SECRET = os.getenv('BYBIT_SECRET', '')

KUCOIN_API_KEY = os.getenv('KUCOIN_API_KEY', '')
KUCOIN_SECRET = os.getenv('KUCOIN_SECRET', '')
KUCOIN_PASSPHRASE = os.getenv('KUCOIN_PASSPHRASE', '')

OKX_API_KEY = os.getenv('OKX_API_KEY', '')
OKX_SECRET = os.getenv('OKX_SECRET', '')
OKX_PASSPHRASE = os.getenv('OKX_PASSPHRASE', '')

# Trading Configuration
CAPITAL_USD = 90  # $90 USD (1.5 juta IDR)
MIN_PROFIT_PERCENTAGE = 5.0  # Minimum 5% profit
MAX_PRICE_DIFFERENCE = 50.0  # Maximum 50% price difference
SLIPPAGE_PERCENTAGE = 5.0  # 5% slippage

# Exchange Configuration
EXCHANGES = {
    'binance': {
        'name': 'Binance',
        'class': 'binance',
        'sandbox': False,
        'rateLimit': 1200,
        'enableRateLimit': True,
    },
    'bybit': {
        'name': 'Bybit',
        'class': 'bybit',
        'sandbox': False,
        'rateLimit': 1000,
        'enableRateLimit': True,
    },
    'kucoin': {
        'name': 'KuCoin',
        'class': 'kucoin',
        'sandbox': False,
        'rateLimit': 1000,
        'enableRateLimit': True,
    },
    'okx': {
        'name': 'OKX',
        'class': 'okx',
        'sandbox': False,
        'rateLimit': 1000,
        'enableRateLimit': True,
    }
}

# Stablecoins to filter out
STABLECOINS = [
    'USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDP', 'USDD', 'FRAX',
    'LUSD', 'SUSD', 'GUSD', 'HUSD', 'USDN', 'USTC', 'FDUSD'
]

# Popular trading pairs to prioritize
PRIORITY_TOKENS = [
    'BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'SOL', 'DOT', 'DOGE', 'AVAX', 'SHIB',
    'MATIC', 'LTC', 'UNI', 'LINK', 'ATOM', 'ETC', 'XLM', 'BCH', 'ALGO', 'VET',
    'ICP', 'FIL', 'TRX', 'EOS', 'AAVE', 'GRT', 'SAND', 'MANA', 'AXS', 'CRV',
    'SUSHI', 'COMP', 'YFI', 'SNX', 'MKR', 'ENJ', 'BAT', 'ZRX', 'STORJ', 'ANKR'
]

# Refresh intervals (seconds)
PRICE_REFRESH_INTERVAL = 30
FEE_REFRESH_INTERVAL = 300  # 5 minutes
MARKET_REFRESH_INTERVAL = 3600  # 1 hour

# Display settings
MAX_OPPORTUNITIES_DISPLAY = 10
CONSOLE_WIDTH = 120
