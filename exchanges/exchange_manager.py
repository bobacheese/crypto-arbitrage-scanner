"""
Exchange Manager untuk mengelola koneksi ke multiple exchanges
"""
import ccxt
import asyncio
import time
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from config.settings import EXCHANGES, BINANCE_API_KEY, BINANCE_SECRET, BYBIT_API_KEY, BYBIT_SECRET, KUCOIN_API_KEY, KUCOIN_SECRET, KUCOIN_PASSPHRASE, OKX_API_KEY, OKX_SECRET, OKX_PASSPHRASE

console = Console()

class ExchangeManager:
    def __init__(self):
        self.exchanges = {}
        self.markets_cache = {}
        self.fees_cache = {}
        self.last_market_update = {}
        self.last_fee_update = {}
        
    async def initialize_exchanges(self):
        """Initialize semua exchange connections"""
        console.print("[yellow]🔄 Menginisialisasi koneksi exchange...[/yellow]")
        
        for exchange_id, config in EXCHANGES.items():
            try:
                exchange_class = getattr(ccxt, config['class'])
                
                # Setup API credentials jika tersedia
                api_config = {
                    'apiKey': '',
                    'secret': '',
                    'sandbox': config['sandbox'],
                    'rateLimit': config['rateLimit'],
                    'enableRateLimit': config['enableRateLimit'],
                }
                
                if exchange_id == 'binance':
                    api_config.update({'apiKey': BINANCE_API_KEY, 'secret': BINANCE_SECRET})
                elif exchange_id == 'bybit':
                    api_config.update({'apiKey': BYBIT_API_KEY, 'secret': BYBIT_SECRET})
                elif exchange_id == 'kucoin':
                    api_config.update({
                        'apiKey': KUCOIN_API_KEY, 
                        'secret': KUCOIN_SECRET,
                        'password': KUCOIN_PASSPHRASE
                    })
                elif exchange_id == 'okx':
                    api_config.update({
                        'apiKey': OKX_API_KEY, 
                        'secret': OKX_SECRET,
                        'password': OKX_PASSPHRASE
                    })
                
                exchange = exchange_class(api_config)
                
                # Test connection
                await self._test_connection(exchange, exchange_id)
                self.exchanges[exchange_id] = exchange
                
                console.print(f"[green]✅ {config['name']} berhasil terhubung[/green]")
                
            except Exception as e:
                console.print(f"[red]❌ Gagal menghubungkan {config['name']}: {str(e)}[/red]")
                continue
        
        if not self.exchanges:
            raise Exception("Tidak ada exchange yang berhasil terhubung!")
        
        console.print(f"[green]🎉 Berhasil terhubung ke {len(self.exchanges)} exchange[/green]")
    
    async def _test_connection(self, exchange, exchange_id: str):
        """Test koneksi ke exchange"""
        try:
            # Test dengan fetch ticker untuk pair populer
            if hasattr(exchange, 'fetch_ticker'):
                await exchange.fetch_ticker('BTC/USDT')
            else:
                # Fallback ke load markets
                await exchange.load_markets()
        except Exception as e:
            raise Exception(f"Connection test failed: {str(e)}")
    
    async def get_all_markets(self, force_refresh: bool = False) -> Dict[str, Dict]:
        """Ambil semua markets dari semua exchange"""
        current_time = time.time()
        
        for exchange_id, exchange in self.exchanges.items():
            # Check cache validity
            if (not force_refresh and 
                exchange_id in self.markets_cache and 
                exchange_id in self.last_market_update and
                current_time - self.last_market_update[exchange_id] < 3600):  # 1 hour cache
                continue
            
            try:
                console.print(f"[yellow]📊 Mengambil markets dari {EXCHANGES[exchange_id]['name']}...[/yellow]")
                markets = await exchange.load_markets()
                self.markets_cache[exchange_id] = markets
                self.last_market_update[exchange_id] = current_time
                
            except Exception as e:
                console.print(f"[red]❌ Error mengambil markets dari {exchange_id}: {str(e)}[/red]")
                continue
        
        return self.markets_cache

    async def get_trading_fees(self, force_refresh: bool = False) -> Dict[str, Dict]:
        """Ambil trading fees dari semua exchange"""
        current_time = time.time()

        for exchange_id, exchange in self.exchanges.items():
            # Check cache validity
            if (not force_refresh and
                exchange_id in self.fees_cache and
                exchange_id in self.last_fee_update and
                current_time - self.last_fee_update[exchange_id] < 300):  # 5 minutes cache
                continue

            try:
                console.print(f"[yellow]💰 Mengambil fees dari {EXCHANGES[exchange_id]['name']}...[/yellow]")

                if hasattr(exchange, 'fetch_trading_fees'):
                    fees = await exchange.fetch_trading_fees()
                else:
                    # Fallback ke default fees
                    fees = {
                        'maker': 0.001,  # 0.1%
                        'taker': 0.001,  # 0.1%
                    }

                self.fees_cache[exchange_id] = fees
                self.last_fee_update[exchange_id] = current_time

            except Exception as e:
                console.print(f"[red]❌ Error mengambil fees dari {exchange_id}: {str(e)}[/red]")
                # Set default fees
                self.fees_cache[exchange_id] = {
                    'maker': 0.001,
                    'taker': 0.001,
                }
                continue

        return self.fees_cache

    async def get_ticker_prices(self, symbols: List[str]) -> Dict[str, Dict[str, float]]:
        """Ambil harga ticker untuk symbols tertentu dari semua exchange"""
        prices = {}

        for exchange_id, exchange in self.exchanges.items():
            prices[exchange_id] = {}

            for symbol in symbols:
                try:
                    ticker = await exchange.fetch_ticker(symbol)
                    prices[exchange_id][symbol] = {
                        'bid': ticker['bid'],
                        'ask': ticker['ask'],
                        'last': ticker['last'],
                        'volume': ticker['baseVolume']
                    }
                except Exception as e:
                    # Symbol tidak tersedia di exchange ini
                    continue

        return prices

    async def validate_deposit_withdrawal(self, symbol: str) -> Dict[str, Dict[str, bool]]:
        """Validasi apakah coin bisa deposit/withdraw di setiap exchange"""
        validation_results = {}

        for exchange_id, exchange in self.exchanges.items():
            validation_results[exchange_id] = {
                'deposit_enabled': True,
                'withdraw_enabled': True
            }

            try:
                # Cek currencies info jika tersedia
                if hasattr(exchange, 'currencies') and exchange.currencies:
                    currency_info = exchange.currencies.get(symbol.split('/')[0])
                    if currency_info:
                        validation_results[exchange_id]['deposit_enabled'] = currency_info.get('deposit', True)
                        validation_results[exchange_id]['withdraw_enabled'] = currency_info.get('withdraw', True)

            except Exception as e:
                # Default ke True jika tidak bisa validasi
                continue

        return validation_results

    def get_exchange_names(self) -> List[str]:
        """Dapatkan nama-nama exchange yang terhubung"""
        return [EXCHANGES[exchange_id]['name'] for exchange_id in self.exchanges.keys()]

    async def close_connections(self):
        """Tutup semua koneksi exchange"""
        for exchange_id, exchange in self.exchanges.items():
            try:
                if hasattr(exchange, 'close'):
                    await exchange.close()
            except Exception as e:
                console.print(f"[yellow]⚠️ Warning saat menutup {exchange_id}: {str(e)}[/yellow]")

        console.print("[green]🔒 Semua koneksi exchange ditutup[/green]")
