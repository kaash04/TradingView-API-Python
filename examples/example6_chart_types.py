#!/usr/bin/env python3
"""
Example 6: HeikinAshi Chart Type
Demonstrates how to use HeikinAshi chart type for smoother price action analysis.
"""

import asyncio
from TradingView import Client, ChartSession

async def main():
    print("=== Example 6: HeikinAshi Chart Type ===")
    
    # Create client
    client = Client(debug=False)
    
    # Set up event handlers
    def on_connect():
        print("✅ Connected to TradingView WebSocket")
    
    def on_login(data):
        print("✅ Successfully logged in")
    
    def on_error(error):
        print(f"❌ Error: {error}")
    
    def on_close():
        print("🔌 Connection closed")
    
    # Register event handlers
    client.on_connected(on_connect)
    client.on_logged(on_login)
    client.on_error(on_error)
    client.on_disconnected(on_close)
    
    # Connect to TradingView
    print("🔗 Connecting to TradingView...")
    await client.connect()
    
    # Wait a moment for connection to establish
    await asyncio.sleep(2)
    
    print("✅ Ready to create chart sessions")
    
    # Example 1: Regular Candlestick Chart (baseline)
    print("\n📊 Creating regular candlestick chart for BTCUSD...")
    session1 = ChartSession(client)
    
    def on_candlestick_update(data):
        if 'periods' in data and data['periods']:
            latest = data['periods'][0]
            print(f"Regular Candlestick - Time: {latest['time']}, Open: {latest['open']}, Close: {latest['close']}, High: {latest['max']}, Low: {latest['min']}")
    
    def on_candlestick_error(*args):
        print(f"❌ Candlestick error: {args}")
    
    session1.on_update(on_candlestick_update)
    session1.on_error(on_candlestick_error)
    
    # Regular candlestick chart
    session1.set_market("BINANCE:BTCUSD", {
        'timeframe': '5',  # 5-minute candles
        'range': 5
    })
    
    # Wait for initial data
    await asyncio.sleep(3)
    
    # Example 2: HeikinAshi Chart
    print("\n📊 Creating HeikinAshi chart for BTCUSD...")
    session2 = ChartSession(client)
    
    def on_heikinashi_update(data):
        if 'periods' in data and data['periods']:
            latest = data['periods'][0]
            print(f"HeikinAshi - Time: {latest['time']}, Open: {latest['open']}, Close: {latest['close']}, High: {latest['max']}, Low: {latest['min']}")
    
    def on_heikinashi_error(*args):
        print(f"❌ HeikinAshi error: {args}")
    
    session2.on_update(on_heikinashi_update)
    session2.on_error(on_heikinashi_error)
    
    # HeikinAshi chart type
    session2.set_market("BINANCE:BTCUSD", {
        'timeframe': '5',  # 5-minute
        'range': 5,
        'type': 'HeikinAshi'
    })
    
    # Wait for initial data
    await asyncio.sleep(3)
    
    # Example 3: HeikinAshi Chart with Different Symbol
    print("\n📊 Creating HeikinAshi chart for ETHUSD...")
    session3 = ChartSession(client)
    
    def on_eth_heikinashi_update(data):
        if 'periods' in data and data['periods']:
            latest = data['periods'][0]
            print(f"ETH HeikinAshi - Time: {latest['time']}, Open: {latest['open']}, Close: {latest['close']}, High: {latest['max']}, Low: {latest['min']}")
    
    def on_eth_heikinashi_error(*args):
        print(f"❌ ETH HeikinAshi error: {args}")
    
    session3.on_update(on_eth_heikinashi_update)
    session3.on_error(on_eth_heikinashi_error)
    
    # HeikinAshi chart for ETH
    session3.set_market("BINANCE:ETHUSD", {
        'timeframe': '15',  # 15-minute
        'range': 3,
        'type': 'HeikinAshi'
    })
    
    # Wait for initial data
    await asyncio.sleep(3)
    
    # Keep sessions alive to receive data
    print("\n⏳ Receiving data from different chart types...")
    print("   Compare regular candlesticks vs HeikinAshi smoothed data")
    print("   Press Ctrl+C to stop...")
    
    try:
        # Run for a reasonable time to see differences
        for i in range(30):  # Run for about 1 minute
            await asyncio.sleep(2)
            if i % 10 == 0:
                print(f"\n--- {i//10 + 1}/3: Still monitoring chart types ---")
    except KeyboardInterrupt:
        print("\n🛑 Stopping data reception...")
    
    # Cleanup
    print("\n🔔 Unsubscribing from all chart sessions...")
    session1.unsubscribe()
    session2.unsubscribe()
    session3.unsubscribe()
    
    print("🔌 Disconnecting...")
    client.disconnect()
    
    print("✅ HeikinAshi chart example completed!")
    print("\n📝 Summary:")
    print("   - Regular candlesticks show raw OHLC data")
    print("   - HeikinAshi smooths price action using modified OHLC calculations:")
    print("     • HA Close = (Open + High + Low + Close) / 4")
    print("     • HA Open = (Previous HA Open + Previous HA Close) / 2")
    print("     • HA High = Max(High, HA Open, HA Close)")
    print("     • HA Low = Min(Low, HA Open, HA Close)")
    print("   - HeikinAshi helps identify trends and reduces market noise")

if __name__ == "__main__":
    asyncio.run(main())