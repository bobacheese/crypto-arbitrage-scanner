# 🚀 Crypto Arbitrage Scanner v2.0

<div align="center">

![Crypto Arbitrage](https://img.shields.io/badge/Crypto-Arbitrage-gold?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Exchanges](https://img.shields.io/badge/Exchanges-4-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Advanced Multi-Exchange Arbitrage Opportunity Detector**

*Temukan peluang arbitrage crypto yang valid dan akurat di 4 exchange utama*

</div>

---

## 🌟 Overview

Crypto Arbitrage Scanner adalah tool canggih yang dirancang untuk mendeteksi peluang arbitrage cryptocurrency yang **benar-benar valid dan akurat** di multiple exchanges. Dengan sistem validasi berlapis dan perhitungan profit realistis, tool ini membantu trader menemukan opportunities yang bisa dieksekusi dengan aman.

### 🎯 Mengapa Tool Ini Berbeda?

- **✅ Validasi Berlapis**: Sistem validasi komprehensif untuk memastikan opportunities yang ditampilkan benar-benar valid
- **💰 Perhitungan Realistis**: Menghitung profit dengan mempertimbangkan fees, slippage, dan biaya transfer
- **🛡️ Smart Filtering**: Otomatis filter stablecoin pairs dan opportunities yang tidak valid
- **⚡ Real-time Data**: Menggunakan data real-time dari exchange APIs
- **🎨 Beautiful UI**: Interface yang menarik menggunakan Rich library

---

## 🏢 Supported Exchanges

| Exchange | Status | Features |
|----------|--------|----------|
| **Binance** | ✅ Active | Spot trading, Real-time fees |
| **Bybit** | ✅ Active | Spot trading, Volume validation |
| **KuCoin** | ✅ Active | Deposit/withdrawal validation |
| **OKX** | ✅ Active | Advanced market data |

---

## 🚀 Key Features

### 🔍 **Advanced Detection System**
- Multi-exchange price comparison
- Real-time arbitrage opportunity scanning
- Prioritized popular token analysis
- Cross-validation antar exchanges

### 💎 **Comprehensive Validation**
- ✅ Stablecoin pair filtering
- ✅ Price difference validation (max 50%)
- ✅ Minimum profit threshold (5%+)
- ✅ Volume dan liquidity checking
- ✅ Deposit/withdrawal support validation
- ✅ Trading pair availability verification

### 💰 **Realistic Profit Calculation**
- Trading fees dari setiap exchange
- Slippage cost calculation (5%)
- Network transfer fees consideration
- Capital efficiency analysis

### 🎨 **Beautiful Interface**
- Rich console interface dengan colors
- Real-time progress indicators
- Detailed opportunity tables
- Futuristic trading signal format

---

## 📦 Installation

### Prerequisites
- Python 3.8 atau lebih tinggi
- Internet connection yang stabil
- (Opsional) API keys untuk akses penuh

### Quick Start

```bash
# Clone repository
git clone https://github.com/bobacheese/crypto-arbitrage-scanner.git
cd crypto-arbitrage-scanner

# Install dependencies
pip install -r requirements.txt

# Run the scanner
python main.py
```

### 🔐 API Configuration (Optional)

Buat file `.env` untuk API keys (opsional, tool bisa jalan tanpa API keys):

```env
# Binance
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET=your_binance_secret

# Bybit
BYBIT_API_KEY=your_bybit_api_key
BYBIT_SECRET=your_bybit_secret

# KuCoin
KUCOIN_API_KEY=your_kucoin_api_key
KUCOIN_SECRET=your_kucoin_secret
KUCOIN_PASSPHRASE=your_kucoin_passphrase

# OKX
OKX_API_KEY=your_okx_api_key
OKX_SECRET=your_okx_secret
OKX_PASSPHRASE=your_okx_passphrase
```

---

## ⚙️ Configuration

### Trading Settings

Tool ini dikonfigurasi dengan parameter yang optimal untuk trading:

```python
CAPITAL_USD = 90          # $90 USD (~1.5 juta IDR)
MIN_PROFIT_PERCENTAGE = 5.0   # Minimum 5% profit
MAX_PRICE_DIFFERENCE = 50.0   # Maximum 50% price difference
SLIPPAGE_PERCENTAGE = 5.0     # 5% slippage tolerance
```

### Customization

Edit `config/settings.py` untuk menyesuaikan:
- Capital amount
- Profit thresholds
- Exchange configurations
- Token priorities

---

## 🎮 Usage

### Basic Usage

```bash
python main.py
```

Program akan:
1. 🔄 Connect ke semua exchanges
2. 📊 Load market data dan trading fees
3. 🔍 Scan untuk arbitrage opportunities
4. ✅ Validate setiap opportunity
5. 📈 Display hasil dengan ranking

### Sample Output

```
🎯 ARBITRAGE OPPORTUNITIES DITEMUKAN (3)
Capital: $90 USD | Minimum Profit: 5% | Slippage: 5%

┌─────────────────────────────────────────────────────────────┐
│                    Opportunity #1                           │
├─────────────────────────────────────────────────────────────┤
│ 🪙 Trading Pair    │ BTC/USDT                              │
│ 💰 Buy Exchange    │ KUCOIN @ $43,250.50                  │
│ 💸 Sell Exchange   │ BYBIT @ $43,890.25                   │
│ 📈 Profit          │ 6.45% ($5.81)                        │
│ 💳 Fees            │ Buy: 0.10% | Sell: 0.10%             │
│ ⚡ Slippage Cost   │ $4.50                                 │
│ 📊 Volume          │ 1,250,000                             │
│ 🎯 Buy Amount      │ 0.002075 BTC                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧠 How It Works

### 1. **Multi-Exchange Connection**
- Connects ke Binance, Bybit, KuCoin, dan OKX
- Real-time market data fetching
- Automatic retry dan error handling

### 2. **Smart Pair Detection**
- Finds common trading pairs across exchanges
- Prioritizes popular tokens (BTC, ETH, BNB, dll)
- Validates pair availability dan status

### 3. **Arbitrage Analysis**
- Compares bid/ask prices antar exchanges
- Calculates potential profit untuk setiap scenario
- Considers trading fees dan slippage

### 4. **Advanced Validation**
- ❌ Filters out stablecoin arbitrage
- ❌ Removes extreme price differences
- ❌ Excludes low-profit opportunities
- ✅ Validates deposit/withdrawal support
- ✅ Checks minimum volume requirements

### 5. **Profit Calculation**
```python
# Realistic profit calculation
buy_amount = capital / (buy_price * (1 + buy_fee))
sell_revenue = buy_amount * sell_price * (1 - sell_fee) * (1 - slippage)
profit = sell_revenue - capital
```

---

## 📊 Validation System

### Multi-Layer Validation

1. **Price Validation**
   - Maximum 50% price difference
   - Positive profit requirement
   - Realistic market conditions

2. **Market Validation**
   - Trading pair availability
   - Active market status
   - Sufficient volume

3. **Exchange Validation**
   - Deposit support verification
   - Withdrawal support verification
   - Fee structure validation

4. **Risk Assessment**
   - Slippage impact calculation
   - Network fee consideration
   - Liquidity risk evaluation

---

## 🛡️ Safety Features

- **Smart Filtering**: Otomatis filter opportunities yang tidak valid
- **Rate Limiting**: Respect exchange API limits
- **Error Handling**: Robust error handling dan recovery
- **Graceful Shutdown**: Proper Ctrl+C handling
- **Connection Management**: Automatic connection cleanup

---

## 🔧 Technical Details

### Architecture

```
crypto-arbitrage-scanner/
├── main.py                 # Entry point
├── config/
│   └── settings.py        # Configuration
├── exchanges/
│   └── exchange_manager.py # Exchange connections
├── arbitrage/
│   └── scanner.py         # Core scanning logic
├── utils/
│   └── validators.py      # Validation functions
└── requirements.txt       # Dependencies
```

### Dependencies

- **ccxt**: Exchange connectivity
- **rich**: Beautiful console interface
- **asyncio**: Asynchronous operations
- **python-dotenv**: Environment variables
- **pandas/numpy**: Data processing

---

## 🚨 Important Notes

### ⚠️ Risk Disclaimer

- Tool ini untuk educational purposes
- Selalu verify opportunities secara manual
- Consider network fees dan transfer time
- Crypto trading involves risks

### 💡 Best Practices

1. **Start Small**: Test dengan capital kecil
2. **Verify Manually**: Double-check setiap opportunity
3. **Monitor Fees**: Network fees bisa berubah
4. **Check Liquidity**: Pastikan sufficient liquidity
5. **Time Sensitivity**: Arbitrage opportunities cepat hilang

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests if applicable
5. Submit pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **CCXT Library**: For excellent exchange connectivity
- **Rich Library**: For beautiful console interface
- **Crypto Community**: For inspiration dan feedback

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ for the crypto community

</div>