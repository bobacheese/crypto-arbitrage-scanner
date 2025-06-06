"""
Arbitrage Scanner - Core logic untuk mencari arbitrage opportunities
"""
import asyncio
import time
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from exchanges.exchange_manager import ExchangeManager
from utils.validators import ArbitrageValidator
from config.settings import PRIORITY_TOKENS, CAPITAL_USD, SLIPPAGE_PERCENTAGE, MAX_OPPORTUNITIES_DISPLAY

console = Console()

class ArbitrageScanner:
    def __init__(self):
        self.exchange_manager = ExchangeManager()
        self.validator = ArbitrageValidator()
        self.running = False
        
    async def initialize(self):
        """Initialize scanner"""
        await self.exchange_manager.initialize_exchanges()
        
    async def find_arbitrage_opportunities(self) -> List[Dict]:
        """Cari arbitrage opportunities di semua exchange"""
        console.print("\n[bold cyan]🔍 Mencari Arbitrage Opportunities...[/bold cyan]")
        
        # Get markets dan fees
        markets = await self.exchange_manager.get_all_markets()
        fees = await self.exchange_manager.get_trading_fees()
        
        # Find common trading pairs
        common_pairs = self._find_common_trading_pairs(markets)
        console.print(f"[green]📊 Ditemukan {len(common_pairs)} trading pairs yang tersedia di multiple exchange[/green]")
        
        if not common_pairs:
            console.print("[red]❌ Tidak ada trading pairs yang sama di multiple exchange[/red]")
            return []
        
        # Get prices untuk common pairs
        opportunities = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Menganalisis harga...", total=len(common_pairs))
            
            for symbol in common_pairs:
                try:
                    # Get prices dari semua exchange untuk symbol ini
                    prices = await self.exchange_manager.get_ticker_prices([symbol])
                    
                    # Validate deposit/withdrawal support
                    base_token = symbol.split('/')[0]
                    deposit_withdrawal = await self.exchange_manager.validate_deposit_withdrawal(base_token)
                    
                    # Find arbitrage opportunities untuk symbol ini
                    symbol_opportunities = self._analyze_symbol_arbitrage(
                        symbol, prices, fees, deposit_withdrawal
                    )
                    
                    opportunities.extend(symbol_opportunities)
                    
                except Exception as e:
                    console.print(f"[red]❌ Error analyzing {symbol}: {str(e)}[/red]")
                    continue
                finally:
                    progress.advance(task)
        
        # Filter dan rank opportunities
        valid_opportunities = self.validator.filter_valid_opportunities(opportunities)
        ranked_opportunities = self.validator.rank_opportunities(valid_opportunities)
        
        console.print(f"[green]✅ Ditemukan {len(ranked_opportunities)} arbitrage opportunities yang valid[/green]")
        
        return ranked_opportunities[:MAX_OPPORTUNITIES_DISPLAY]
    
    def _find_common_trading_pairs(self, markets: Dict[str, Dict]) -> List[str]:
        """Cari trading pairs yang tersedia di minimal 2 exchange"""
        if len(markets) < 2:
            return []
        
        # Collect semua symbols dari setiap exchange
        exchange_symbols = {}
        for exchange_id, exchange_markets in markets.items():
            exchange_symbols[exchange_id] = set(exchange_markets.keys())
        
        # Find intersection - symbols yang ada di minimal 2 exchange
        common_symbols = set()
        exchange_ids = list(exchange_symbols.keys())
        
        for i in range(len(exchange_ids)):
            for j in range(i + 1, len(exchange_ids)):
                exchange1_symbols = exchange_symbols[exchange_ids[i]]
                exchange2_symbols = exchange_symbols[exchange_ids[j]]
                common_symbols.update(exchange1_symbols.intersection(exchange2_symbols))
        
        # Prioritize popular tokens
        prioritized_symbols = []
        other_symbols = []
        
        for symbol in common_symbols:
            base_token = symbol.split('/')[0]
            if base_token in PRIORITY_TOKENS:
                prioritized_symbols.append(symbol)
            else:
                other_symbols.append(symbol)
        
        # Return prioritized first, then others
        return prioritized_symbols + other_symbols

    def _analyze_symbol_arbitrage(self, symbol: str, prices: Dict[str, Dict],
                                fees: Dict[str, Dict],
                                deposit_withdrawal: Dict[str, Dict]) -> List[Dict]:
        """Analyze arbitrage opportunities untuk satu symbol"""
        opportunities = []
        exchange_ids = list(prices.keys())

        # Compare setiap pasangan exchange
        for i in range(len(exchange_ids)):
            for j in range(i + 1, len(exchange_ids)):
                exchange1 = exchange_ids[i]
                exchange2 = exchange_ids[j]

                # Skip jika salah satu exchange tidak punya data untuk symbol ini
                if (symbol not in prices[exchange1] or
                    symbol not in prices[exchange2]):
                    continue

                price1 = prices[exchange1][symbol]
                price2 = prices[exchange2][symbol]

                # Scenario 1: Buy di exchange1, sell di exchange2
                opp1 = self._calculate_arbitrage_opportunity(
                    symbol, exchange1, exchange2,
                    price1['ask'], price2['bid'],
                    fees.get(exchange1, {}), fees.get(exchange2, {}),
                    price1.get('volume', 0), deposit_withdrawal
                )

                if opp1:
                    opportunities.append(opp1)

                # Scenario 2: Buy di exchange2, sell di exchange1
                opp2 = self._calculate_arbitrage_opportunity(
                    symbol, exchange2, exchange1,
                    price2['ask'], price1['bid'],
                    fees.get(exchange2, {}), fees.get(exchange1, {}),
                    price2.get('volume', 0), deposit_withdrawal
                )

                if opp2:
                    opportunities.append(opp2)

        return opportunities

    def _calculate_arbitrage_opportunity(self, symbol: str, buy_exchange: str, sell_exchange: str,
                                       buy_price: float, sell_price: float,
                                       buy_fees: Dict, sell_fees: Dict,
                                       volume: float, deposit_withdrawal: Dict) -> Optional[Dict]:
        """Calculate arbitrage opportunity"""

        # Basic validation
        if buy_price <= 0 or sell_price <= 0 or sell_price <= buy_price:
            return None

        # Validate deposit/withdrawal support
        if not self.validator.validate_deposit_withdrawal_support(
            deposit_withdrawal, buy_exchange, sell_exchange
        ):
            return None

        # Get fees
        buy_fee = buy_fees.get('taker', 0.001)  # Default 0.1%
        sell_fee = sell_fees.get('taker', 0.001)  # Default 0.1%

        # Calculate realistic profit
        profit_calc = self.validator.calculate_realistic_profit(
            buy_price, sell_price, buy_fee, sell_fee,
            CAPITAL_USD, SLIPPAGE_PERCENTAGE
        )

        # Validate minimum profit
        if not self.validator.validate_minimum_profit(profit_calc['profit_percentage']):
            return None

        # Validate price difference
        if not self.validator.validate_price_difference(buy_price, sell_price):
            return None

        return {
            'symbol': symbol,
            'buy_exchange': buy_exchange,
            'sell_exchange': sell_exchange,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'buy_fee_percentage': buy_fee * 100,
            'sell_fee_percentage': sell_fee * 100,
            'volume': volume,
            'profit_percentage': profit_calc['profit_percentage'],
            'profit_usd': profit_calc['gross_profit_usd'],
            'slippage_cost_usd': profit_calc['slippage_cost_usd'],
            'capital_required': CAPITAL_USD,
            'buy_amount': profit_calc['buy_amount'],
            'timestamp': time.time()
        }

    async def start_continuous_scan(self):
        """Start continuous scanning untuk arbitrage opportunities"""
        self.running = True
        console.print("[bold green]🚀 Memulai continuous arbitrage scanning...[/bold green]")
        console.print("[yellow]Tekan Ctrl+C untuk berhenti[/yellow]\n")

        try:
            while self.running:
                opportunities = await self.find_arbitrage_opportunities()

                if opportunities:
                    self._display_opportunities(opportunities)
                else:
                    console.print("[yellow]⏳ Belum ada arbitrage opportunities yang valid. Mencoba lagi...[/yellow]")

                # Wait sebelum scan berikutnya
                await asyncio.sleep(30)  # 30 detik

        except KeyboardInterrupt:
            console.print("\n[yellow]🛑 Stopping scanner...[/yellow]")
            self.running = False
        except Exception as e:
            console.print(f"\n[red]❌ Error dalam scanning: {str(e)}[/red]")
            self.running = False
        finally:
            await self.exchange_manager.close_connections()

    def _display_opportunities(self, opportunities: List[Dict]):
        """Display arbitrage opportunities dengan rich formatting"""

        # Header
        console.print(f"\n[bold green]🎯 ARBITRAGE OPPORTUNITIES DITEMUKAN ({len(opportunities)})[/bold green]")
        console.print(f"[dim]Capital: ${CAPITAL_USD} USD | Minimum Profit: 5% | Slippage: {SLIPPAGE_PERCENTAGE}%[/dim]\n")

        for i, opp in enumerate(opportunities, 1):
            # Create table untuk setiap opportunity
            table = Table(show_header=True, header_style="bold magenta", border_style="bright_blue")
            table.add_column("Detail", style="cyan", width=20)
            table.add_column("Value", style="white", width=30)

            # Add rows
            table.add_row("🪙 Trading Pair", f"[bold]{opp['symbol']}[/bold]")
            table.add_row("💰 Buy Exchange", f"[green]{opp['buy_exchange'].upper()}[/green] @ ${opp['buy_price']:.6f}")
            table.add_row("💸 Sell Exchange", f"[red]{opp['sell_exchange'].upper()}[/red] @ ${opp['sell_price']:.6f}")
            table.add_row("📈 Profit", f"[bold green]{opp['profit_percentage']:.2f}% (${opp['profit_usd']:.2f})[/bold green]")
            table.add_row("💳 Fees", f"Buy: {opp['buy_fee_percentage']:.2f}% | Sell: {opp['sell_fee_percentage']:.2f}%")
            table.add_row("⚡ Slippage Cost", f"[yellow]${opp['slippage_cost_usd']:.2f}[/yellow]")
            table.add_row("📊 Volume", f"{opp['volume']:,.0f}")
            table.add_row("🎯 Buy Amount", f"{opp['buy_amount']:.6f} {opp['symbol'].split('/')[0]}")

            # Panel dengan opportunity
            panel = Panel(
                table,
                title=f"[bold]Opportunity #{i}[/bold]",
                title_align="left",
                border_style="bright_green" if opp['profit_percentage'] >= 10 else "bright_yellow"
            )

            console.print(panel)

        # Footer dengan timestamp
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        console.print(f"\n[dim]Last updated: {current_time}[/dim]")
        console.print("[dim]💡 Tip: Periksa liquidity dan network fees sebelum execute![/dim]\n")

    async def stop(self):
        """Stop scanner"""
        self.running = False
        await self.exchange_manager.close_connections()
