#!/usr/bin/env python3
"""
🚀 Crypto Arbitrage Scanner
Advanced arbitrage opportunity detector untuk multiple exchanges

Author: Crypto Arbitrage Team
Version: 2.0.0
"""

import asyncio
import signal
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from arbitrage.scanner import ArbitrageScanner

console = Console()

def display_banner():
    """Display aplikasi banner"""
    banner_text = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🚀 CRYPTO ARBITRAGE SCANNER v2.0                      ║
    ║                                                               ║
    ║        💰 Multi-Exchange Arbitrage Detector                   ║
    ║        📊 Real-time Price Analysis                            ║
    ║        🔍 Valid Opportunity Finder                            ║
    ║        ⚡ Advanced Validation System                          ║
    ║                                                               ║
    ║        Supported Exchanges:                                   ║
    ║        • Binance  • Bybit  • KuCoin  • OKX                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    
    panel = Panel(
        Align.center(Text(banner_text, style="bold cyan")),
        border_style="bright_blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()

def display_features():
    """Display fitur-fitur utama"""
    features = [
        "🔄 Real-time connection ke 4 major exchanges",
        "💎 Advanced arbitrage opportunity detection",
        "🛡️ Comprehensive validation system",
        "💰 Realistic profit calculation dengan fees & slippage",
        "🚫 Smart filtering untuk stablecoin pairs",
        "📊 Volume dan liquidity validation",
        "⚡ Deposit/withdrawal support checking",
        "🎯 Prioritized popular token analysis",
        "📈 Beautiful rich console interface",
        "🔒 Safe Ctrl+C handling"
    ]
    
    console.print("[bold yellow]🌟 Key Features:[/bold yellow]")
    for feature in features:
        console.print(f"  {feature}")
    console.print()

def display_config_info():
    """Display konfigurasi trading"""
    from config.settings import CAPITAL_USD, MIN_PROFIT_PERCENTAGE, SLIPPAGE_PERCENTAGE, MAX_PRICE_DIFFERENCE
    
    config_info = f"""
    [bold green]📋 Trading Configuration:[/bold green]
    
    💵 Capital: ${CAPITAL_USD} USD (~1.5 juta IDR)
    📈 Minimum Profit: {MIN_PROFIT_PERCENTAGE}%
    ⚡ Slippage: {SLIPPAGE_PERCENTAGE}%
    🚨 Max Price Diff: {MAX_PRICE_DIFFERENCE}%
    
    [dim]💡 Tip: Set API keys di .env file untuk akses penuh[/dim]
    """
    
    console.print(config_info)

async def main():
    """Main function"""
    # Display banner dan info
    display_banner()
    display_features()
    display_config_info()
    
    # Initialize scanner
    scanner = ArbitrageScanner()
    
    # Setup signal handler untuk graceful shutdown
    def signal_handler(signum, frame):
        console.print("\n[yellow]🛑 Received interrupt signal. Shutting down gracefully...[/yellow]")
        asyncio.create_task(scanner.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize connections
        console.print("[bold cyan]🔧 Initializing Crypto Arbitrage Scanner...[/bold cyan]")
        await scanner.initialize()
        
        # Start scanning
        await scanner.start_continuous_scan()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Program dihentikan oleh user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Fatal error: {str(e)}[/red]")
        console.print("[dim]Check your internet connection dan API credentials[/dim]")
    finally:
        console.print("[green]🔒 Cleanup completed. Goodbye![/green]")

if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Startup error: {str(e)}[/red]")
        sys.exit(1)
