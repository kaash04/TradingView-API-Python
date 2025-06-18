#!/usr/bin/env python3
"""
Example 4: Chart Session with Market Data
Demonstrates how to create a chart session and subscribe to real-time market data.
"""

import asyncio
from TradingView import Client, ChartSession

async def main():
    print("=== Example 4: Chart Session with Market Data ===")
    
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
    
    print("✅ Ready to create chart session")
    
    # Create chart session
    print("📊 Creating chart session...")
    session = ChartSession(client)
    
    # Set up chart session event handlers
    def on_session_update(data):
        print(f"📈 Chart update: {data['periods']}")
    
    def on_session_error(error):
        print(f"❌ Session error: {error}")
    
    session.on_update(on_session_update)
    session.on_error(on_session_error)
    
    # Subscribe to market data
    print("🔔 Subscribing to market data...")
    session.subscribe("BINANCE:BTCUSD", timeframe='1', range_count=2)
    
    # Keep session alive indefinitely to receive data
    print("⏳ Receiving market data continuously (press Ctrl+C to stop)...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping data reception...")
    
    # Unsubscribe and disconnect
    print("🔔 Unsubscribing from market data...")
    session.unsubscribe()
    
    print("🔌 Disconnecting...")
    client.disconnect()
    
    print("✅ Chart session example completed!")

if __name__ == "__main__":
    asyncio.run(main()) 