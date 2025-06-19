# TradingView Python API

A Python client for the TradingView WebSocket API, providing real-time market data and symbol search functionality.

## Features

- 🔍 **Symbol Search**: Search for trading symbols across exchanges
- 🔌 **WebSocket Connection**: Real-time connection to TradingView
- 📊 **Chart Sessions**: Subscribe to live market data for specific symbols
- 🔄 **Ping/Pong**: Automatic connection keep-alive
- 📈 **Multiple Symbols**: Subscribe to multiple symbols simultaneously

## Support

If you like this project, consider buying me a coffee 😊

[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/2k21akashx)

## Installation

```bash
pip install tradingview-api
```

## Quick Start

### Symbol Search

```python
from TradingView import SymbolSearch

# Create search client
search = SymbolSearch()

# Search for symbols
results = search.search_symbol("AAPL")
for result in results:
    print(f"{result['symbol']}: {result['description']}")
```

### WebSocket Connection

```python
from TradingView import TradingViewClient

# Create client
client = TradingViewClient()

# Set up event handlers
def on_connect():
    print("Connected!")

def on_login():
    print("Logged in!")

client.on_connect = on_connect
client.on_login = on_login

# Connect
client.connect()
```

### Chart Session

```python
from TradingView import TradingViewClient, ChartSession

# Create client and connect
client = TradingViewClient()
client.connect()

# Create chart session
session = ChartSession(client, "NASDAQ:AAPL")

# Subscribe to market data
session.subscribe()

# Handle updates
def on_update(data):
    print(f"Market data: {data}")

session.on_update = on_update
```

## Examples

The package includes comprehensive examples in the `examples/` folder:

### Individual Examples

```bash
# Run specific examples
python examples/example1_symbol_search.py
python examples/example2_basic_client.py
python examples/example3_websocket_with_ping.py
python examples/example4_chart_session.py
python examples/example5_multiple_symbols.py
python examples/example6_chart_types.py
```

### Example Descriptions

1. **Symbol Search** (`example1_symbol_search.py`): Demonstrates symbol search functionality
2. **Basic Client** (`example2_basic_client.py`): Basic WebSocket connection and authentication
3. **WebSocket with Ping** (`example3_websocket_with_ping.py`): Connection with automatic ping/pong
4. **Chart Session** (`example4_chart_session.py`): Real-time market data subscription
5. **Multiple Symbols** (`example5_multiple_symbols.py`): Subscribe to multiple symbols simultaneously

## API Reference

### SymbolSearch

#### `search_symbol(query: str) -> List[Dict]`

Search for trading symbols.

**Parameters:**
- `query` (str): Search query (e.g., "AAPL", "BTC")

**Returns:**
- List of dictionaries containing symbol information:
  - `symbol`: Symbol identifier
  - `description`: Symbol description
  - `exchange`: Exchange name
  - `type`: Symbol type
  - `currency`: Currency code

### TradingViewClient

#### `connect()`

Connect to TradingView WebSocket.

#### `disconnect()`

Disconnect from TradingView WebSocket.

#### `is_connected() -> bool`

Check if connected to TradingView.

#### Event Handlers

- `on_connect`: Called when connected
- `on_login`: Called when logged in
- `on_data`: Called when data is received
- `on_error`: Called when an error occurs
- `on_close`: Called when connection closes

### ChartSession

#### `__init__(client: TradingViewClient, symbol: str)`

Create a new chart session.

**Parameters:**
- `client`: TradingViewClient instance
- `symbol`: Symbol to subscribe to (e.g., "NASDAQ:AAPL")

#### `subscribe()`

Subscribe to market data for the symbol.

#### `unsubscribe()`

Unsubscribe from market data.

#### Event Handlers

- `on_update`: Called when market data is received
- `on_error`: Called when an error occurs

## Development

### Setup

```bash
git clone https://github.com/kaash04/TradingView-API-Python.git
cd TradingView-Python
pip install -e .
```

### Running Examples

```bash
# Run individual examples
python examples/example1_symbol_search.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 