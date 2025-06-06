"""
Validator functions untuk memastikan akurasi arbitrage opportunities
"""
from typing import Dict, List, Tuple, Optional
from config.settings import STABLECOINS, MAX_PRICE_DIFFERENCE, MIN_PROFIT_PERCENTAGE

class ArbitrageValidator:
    
    @staticmethod
    def is_stablecoin_pair(symbol: str) -> bool:
        """Cek apakah trading pair melibatkan stablecoin"""
        base, quote = symbol.split('/')
        return base in STABLECOINS or quote in STABLECOINS
    
    @staticmethod
    def is_same_token_different_name(token1: str, token2: str) -> bool:
        """Cek apakah dua token adalah token yang sama dengan nama berbeda"""
        # Mapping untuk token yang sama dengan nama berbeda
        token_mappings = {
            'WBTC': 'BTC',
            'WETH': 'ETH',
            'WBNB': 'BNB',
            'WMATIC': 'MATIC',
            'WAVAX': 'AVAX',
        }
        
        # Normalize token names
        normalized_token1 = token_mappings.get(token1, token1)
        normalized_token2 = token_mappings.get(token2, token2)
        
        return normalized_token1 == normalized_token2
    
    @staticmethod
    def validate_price_difference(price1: float, price2: float) -> bool:
        """Validasi bahwa perbedaan harga tidak terlalu ekstrem"""
        if price1 <= 0 or price2 <= 0:
            return False
        
        higher_price = max(price1, price2)
        lower_price = min(price1, price2)
        
        price_diff_percentage = ((higher_price - lower_price) / lower_price) * 100
        
        return price_diff_percentage <= MAX_PRICE_DIFFERENCE
    
    @staticmethod
    def validate_minimum_profit(profit_percentage: float) -> bool:
        """Validasi bahwa profit memenuhi minimum threshold"""
        return profit_percentage >= MIN_PROFIT_PERCENTAGE
    
    @staticmethod
    def validate_volume_threshold(volume: float, min_volume: float = 1000) -> bool:
        """Validasi bahwa volume trading cukup untuk arbitrage"""
        return volume >= min_volume
    
    @staticmethod
    def validate_trading_pair_exists(markets: Dict[str, Dict], symbol: str, exchange_ids: List[str]) -> Dict[str, bool]:
        """Validasi bahwa trading pair masih aktif di semua exchange"""
        results = {}
        
        for exchange_id in exchange_ids:
            if exchange_id not in markets:
                results[exchange_id] = False
                continue
            
            exchange_markets = markets[exchange_id]
            
            # Cek apakah symbol ada dan aktif
            if symbol in exchange_markets:
                market_info = exchange_markets[symbol]
                # Cek status aktif
                is_active = market_info.get('active', True)
                results[exchange_id] = is_active
            else:
                results[exchange_id] = False
        
        return results
    
    @staticmethod
    def validate_deposit_withdrawal_support(validation_data: Dict[str, Dict[str, bool]], 
                                          buy_exchange: str, sell_exchange: str) -> bool:
        """Validasi bahwa deposit/withdrawal didukung untuk arbitrage"""
        # Untuk arbitrage, kita perlu:
        # 1. Withdraw dari sell_exchange
        # 2. Deposit ke buy_exchange
        
        if sell_exchange not in validation_data or buy_exchange not in validation_data:
            return False
        
        can_withdraw = validation_data[sell_exchange].get('withdraw_enabled', False)
        can_deposit = validation_data[buy_exchange].get('deposit_enabled', False)
        
        return can_withdraw and can_deposit
    
    @staticmethod
    def filter_valid_opportunities(opportunities: List[Dict]) -> List[Dict]:
        """Filter opportunities untuk hanya menampilkan yang valid"""
        valid_opportunities = []
        
        for opp in opportunities:
            # Skip stablecoin pairs
            if ArbitrageValidator.is_stablecoin_pair(opp['symbol']):
                continue
            
            # Validate price difference
            if not ArbitrageValidator.validate_price_difference(
                opp['buy_price'], opp['sell_price']
            ):
                continue
            
            # Validate minimum profit
            if not ArbitrageValidator.validate_minimum_profit(opp['profit_percentage']):
                continue
            
            # Validate volume (jika tersedia)
            if 'volume' in opp:
                if not ArbitrageValidator.validate_volume_threshold(opp['volume']):
                    continue
            
            valid_opportunities.append(opp)
        
        return valid_opportunities

    @staticmethod
    def calculate_realistic_profit(buy_price: float, sell_price: float,
                                 buy_fee: float, sell_fee: float,
                                 capital: float, slippage: float) -> Dict[str, float]:
        """Hitung profit realistis dengan semua biaya"""

        # Hitung jumlah token yang bisa dibeli
        buy_amount_after_fee = capital / (buy_price * (1 + buy_fee))

        # Hitung hasil penjualan setelah fee dan slippage
        sell_amount_after_slippage = buy_amount_after_fee * (1 - slippage / 100)
        sell_revenue = sell_amount_after_slippage * sell_price * (1 - sell_fee)

        # Hitung profit
        gross_profit = sell_revenue - capital
        profit_percentage = (gross_profit / capital) * 100

        # Hitung biaya slippage dalam USD
        slippage_cost = capital * (slippage / 100)

        return {
            'gross_profit_usd': gross_profit,
            'profit_percentage': profit_percentage,
            'slippage_cost_usd': slippage_cost,
            'net_profit_usd': gross_profit,
            'buy_amount': buy_amount_after_fee,
            'sell_amount': sell_amount_after_slippage
        }

    @staticmethod
    def rank_opportunities(opportunities: List[Dict]) -> List[Dict]:
        """Ranking opportunities berdasarkan profit dan risk"""
        def calculate_score(opp):
            # Base score dari profit percentage
            profit_score = opp['profit_percentage']

            # Bonus untuk volume tinggi
            volume_bonus = min(opp.get('volume', 0) / 10000, 5)  # Max 5 point bonus

            # Penalty untuk price difference yang terlalu tinggi (risk)
            price_diff = abs(opp['sell_price'] - opp['buy_price']) / opp['buy_price'] * 100
            risk_penalty = max(0, (price_diff - 10) * 0.1)  # Penalty jika > 10%

            return profit_score + volume_bonus - risk_penalty

        # Sort berdasarkan score
        opportunities.sort(key=calculate_score, reverse=True)

        return opportunities
