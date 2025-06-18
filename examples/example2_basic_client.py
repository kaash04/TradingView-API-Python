#!/usr/bin/env python3
"""
Example 2: Basic WebSocket Client
Demonstrates basic WebSocket connection and authentication with TradingView.
"""

import asyncio
from TradingView import Client

async def main():
    print("=== Example 2: Basic WebSocket Client ===")
    
    # Create client with debug mode
    client = Client(debug=False)
    
    # Set up event handlers
    def on_connect():
        print("✅ Connected to TradingView WebSocket")
    
    def on_login(data):
        print("✅ Successfully logged in")
        print(f"   Login data: {data}")
    
    def on_data(data):
        print(f"📊 Received data: {data}")
    
    def on_error(error):
        print(f"❌ Error: {error}")
    
    def on_close():
        print("🔌 Connection closed")
    
    # Register event handlers using proper methods
    client.on_connected(on_connect)
    client.on_logged(on_login)
    client.on_data(on_data)
    client.on_error(on_error)
    client.on_disconnected(on_close)
    
    # Connect to TradingView
    print("🔗 Connecting to TradingView...")
    await client.connect()
    
    # Wait a bit to see if login happens
    print("⏳ Waiting for login response...")
    await asyncio.sleep(2)
    
    # Disconnect
    print("🔌 Disconnecting...")
    client.disconnect()
    
    print("✅ Basic client example completed!")

if __name__ == "__main__":
    asyncio.run(main()) 