#!/usr/bin/env python3
"""
Example 5: Multiple Symbols Subscription
Demonstrates how to subscribe to multiple symbols simultaneously.
"""

import asyncio
from TradingView import Client, ChartSession

async def main():
    print("=== Example 5: Multiple Symbols Subscription ===")
    
    # Create client
    client = Client()
    
    # Set up event handlers
    def on_connect():
        print("✅ Connected to TradingView WebSocket")
    
    def on_login(data):
        print("✅ Successfully logged in")
    
    def on_error(error):
        print(f"❌ Error: {error}")
    
    def on_close():
        print("🔌 Connection closed")
    
    # Register event handlers using proper methods
    client.on_connected(on_connect)
    client.on_logged(on_login)
    client.on_error(on_error)
    client.on_disconnected(on_close)
    
    # Connect to TradingView
    print("🔗 Connecting to TradingView...")
    await client.connect()
    
    # Wait a moment for connection to establish
    await asyncio.sleep(1)
    
    print("✅ Ready to create chart sessions")
    
    # Create chart sessions for multiple symbols
    symbols = ["BINANCE:BTCUSD", "BINANCE:ETHUSD", "BINANCE:SOLUSD"]
    sessions = {}
    
    for symbol in symbols:
        print(f"📊 Creating chart session for {symbol}...")
        session = ChartSession(client)
        
        # Set up session event handlers
        def create_update_handler(sym):
            def on_update(data):
                print(f"📈 {sym} update: {data['periods']}")
            return on_update
        
        def create_error_handler(sym):
            def on_error(error):
                print(f"❌ {sym} error: {error}")
            return on_error
        
        session.on_update(create_update_handler(symbol))
        session.on_error(create_error_handler(symbol))
        
        sessions[symbol] = session
    
    # Subscribe to all symbols
    print("🔔 Subscribing to all symbols...")
    for symbol, session in sessions.items():
        print(f"  - Subscribing to {symbol}")
        session.subscribe(symbol, timeframe='1', range_count=2)
    
    # Keep sessions alive indefinitely to receive data
    print("⏳ Receiving market data continuously (press Ctrl+C to stop)...")
    try:
        while True:
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Stopping data reception...")
    
    # Unsubscribe from all symbols
    print("🔔 Unsubscribing from all symbols...")
    for symbol, session in sessions.items():
        print(f"  - Unsubscribing from {symbol}")
        session.unsubscribe()
    
    print("🔌 Disconnecting...")
    client.disconnect()
    
    print("✅ Multiple symbols example completed!")

if __name__ == "__main__":
    asyncio.run(main()) 