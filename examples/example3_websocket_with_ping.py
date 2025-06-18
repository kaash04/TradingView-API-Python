#!/usr/bin/env python3
"""
Example 3: WebSocket with Ping/Pong
Demonstrates WebSocket connection and ping/pong handling with TradingView.
"""

import asyncio
from TradingView import Client

async def main():
    print("=== Example 3: WebSocket with Ping/Pong ===")
    client = Client()

    def on_connect():
        print("✅ Connected to TradingView WebSocket")

    def on_ping(ping):
        print(f"🏓 Ping received: {ping}")

    def on_close():
        print("🔌 Connection closed")

    client.on_connected(on_connect)
    client.on_ping(on_ping)
    client.on_disconnected(on_close)

    print("🔗 Connecting to TradingView...")
    await client.connect()

    print("⏳ Keeping connection alive for 10 seconds with ping/pong...")
    await asyncio.sleep(10)

    print("🔌 Disconnecting...")
    client.disconnect()
    print("✅ WebSocket with ping/pong example completed!")

if __name__ == "__main__":
    asyncio.run(main()) 