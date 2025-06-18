"""
Chart Session - Handles chart-specific functionality for TradingView API
"""

import json
import logging
from typing import Dict, List, Callable, Any, Optional
from collections import OrderedDict

from .utils import gen_session_id
from .types import (
    TimeFrame, MarketSymbol, ChartOptions, ChartType, ChartInputs,
    PricePeriod, MarketInfos, CHART_TYPES
)


class ChartSession:
    """
    Chart session for handling market data and chart operations
    """
    
    def __init__(self, client):
        """
        Initialize chart session
        
        Args:
            client: TradingView client instance
        """
        self.client = client
        self.chart_session_id = gen_session_id('cs')
        
        # Data storage
        self.periods: Dict[int, PricePeriod] = {}
        self.infos: MarketInfos = {}
        self.series_created = False
        self.current_series = 0
        
        # Event callbacks
        self.callbacks = {
            'seriesLoaded': [],
            'symbolLoaded': [],
            'update': [],
            'event': [],
            'error': []
        }
        
        self.logger = logging.getLogger(__name__)
        if not client.debug:
            self.logger.disabled = True
        
        # Register session with client
        self._register_sessions()
    
    @property
    def periods_list(self) -> List[PricePeriod]:
        """Get sorted list of periods"""
        return sorted(self.periods.values(), key=lambda x: x['time'], reverse=True)
    
    def _register_sessions(self) -> None:
        """Register chart session with the client"""
        
        # Chart session
        self.client.sessions[self.chart_session_id] = {
            'type': 'chart',
            'onData': self._handle_chart_data
        }
        
        # Create chart session
        self.client.send('chart_create_session', [self.chart_session_id])
    
    def _handle_chart_data(self, packet: Dict[str, Any]) -> None:
        """Handle chart session data"""
        if self.client.debug:
            self.logger.debug(f"CHART SESSION DATA: {packet}")
        
        packet_type = packet.get('type')
        data = packet.get('data', [])
        
        if packet_type == 'symbol_resolved':
            self.infos = {
                'series_id': data[1],
                **data[2]
            }
            self._handle_event('symbolLoaded')
            return
        
        if packet_type in ['timescale_update', 'du']:
            changes = []
            
            for key, value in data[1].items():
                changes.append(key)
                
                if key == '$prices':
                    periods = value
                    if not periods or 's' not in periods:
                        continue
                    
                    for period_data in periods['s']:
                        # period_data.v contains: [time, open, high, low, close, volume]
                        # Handle both dict and list formats
                        if isinstance(period_data, dict) and 'v' in period_data:
                            v = period_data['v']
                        elif isinstance(period_data, list):
                            v = period_data
                        else:
                            continue
                            
                        if len(v) >= 6:
                            period = {
                                'time': v[0],
                                'open': v[1],
                                'close': v[4],
                                'max': v[2],
                                'min': v[3],
                                'volume': round(v[5] * 100) / 100
                            }
                            self.periods[period['time']] = period
                    continue
            
            # Pass both changes and the updated periods data
            update_data = {
                'changes': changes,
                'periods': self.periods_list.copy(),  # Create a copy of the periods list
                'latest_period': self.periods_list[0] if self.periods_list else None,
                'market_info': self.infos
            }
            self._handle_event('update', update_data)
            return
        
        if packet_type == 'symbol_error':
            self._handle_error(f"({data[1]}) Symbol error:", data[2])
            return
        
        if packet_type == 'series_error':
            self._handle_error('Series error:', data[3])
            return
        
        if packet_type == 'critical_error':
            self._handle_error('Critical error:', data[1], data[2])
    
    def _handle_replay_data(self, packet: Dict[str, Any]) -> None:
        """Handle replay session data - REMOVED"""
        pass
    
    def _handle_event(self, event: str, *data: Any) -> None:
        """Handle internal events"""
        for callback in self.callbacks[event]:
            try:
                callback(*data)
            except Exception as e:
                self.logger.error(f"Error in {event} callback: {e}")
        
        # Also call general event callbacks
        for callback in self.callbacks['event']:
            try:
                callback(event, *data)
            except Exception as e:
                self.logger.error(f"Error in event callback: {e}")
    
    def _handle_error(self, *messages: str) -> None:
        """Handle errors"""
        if not self.callbacks['error']:
            self.logger.error(*messages)
        else:
            self._handle_event('error', *messages)
    
    def set_series(self, timeframe: TimeFrame = '240', range_count: int = 100, reference: Optional[int] = None) -> None:
        """
        Set the chart series
        
        Args:
            timeframe: Chart timeframe
            range_count: Number of periods to load
            reference: Reference timestamp
        """
        if not self.current_series:
            self._handle_error('Please set the market before setting series')
            return
        
        self.periods = {}
        
        calc_range = range_count if reference is None else ['bar_count', reference, range_count]
        
        self.client.send(
            f"{'modify' if self.series_created else 'create'}_series",
            [
                self.chart_session_id,
                '$prices',
                's1',
                f"ser_{self.current_series}",
                timeframe,
                '' if self.series_created else calc_range
            ]
        )
        
        self.series_created = True
    
    def set_market(self, symbol: MarketSymbol, options: ChartOptions = None) -> None:
        """
        Set the chart market
        
        Args:
            symbol: Market symbol (e.g., 'BINANCE:BTCEUR')
            options: Chart options
        """
        if options is None:
            options = {}
        
        self.periods = {}
        
        # Prepare symbol initialization
        symbol_init = {
            'symbol': symbol or 'BTCEUR',
            'adjustment': options.get('adjustment', 'splits')
        }
        
        if options.get('backadjustment'):
            symbol_init['backadjustment'] = 'default'
        if options.get('session'):
            symbol_init['session'] = options['session']
        if options.get('currency'):
            symbol_init['currency-id'] = options['currency']
        
        # Determine if we need complex chart handling (custom chart types)
        has_custom_type = options.get('type')
        
        # Initialize chart configuration
        if has_custom_type:
            chart_init = {}
            chart_init['symbol'] = symbol_init
            
            # Handle custom chart types
            chart_init['type'] = CHART_TYPES.get(options['type'], options['type'])
            # Always include inputs for custom chart types, even if empty
            chart_init['inputs'] = options.get('inputs', {})
        else:
            # Simple chart - use symbol_init directly
            chart_init = symbol_init
        
        self.current_series += 1
        
        # Resolve symbol with the prepared chart configuration
        self.client.send('resolve_symbol', [
            self.chart_session_id,
            f"ser_{self.current_series}",
            f"={json.dumps(chart_init)}"
        ])
        
        # Set series with proper range handling
        self.set_series(
            options.get('timeframe', '240'),
            options.get('range', 100),  # Default to 100 candles
            options.get('to')
        )
    
    def set_timezone(self, timezone: str) -> None:
        """Set chart timezone"""
        self.client.send('set_timezone', [self.chart_session_id, timezone])
    
    def subscribe(self, symbol: str, timeframe: str = '240', range_count: int = 100) -> None:
        """
        Subscribe to a symbol (alias for set_market for compatibility)
        
        Args:
            symbol: Market symbol (e.g., 'NASDAQ:AAPL')
            timeframe: Chart timeframe (default: '240' for 4-hour)
            range_count: Number of periods to load (default: 100)
        """
        self.set_market(symbol, {
            'timeframe': timeframe,
            'range': range_count
        })
    
    def unsubscribe(self, symbol: str = None) -> None:
        """
        Unsubscribe from current symbol (clear the chart)
        
        Args:
            symbol: Symbol to unsubscribe from (optional, clears current symbol)
        """
        # Clear current data
        self.periods = {}
        self.infos = {}
        self.series_created = False
        self.current_series = 0
        
        # Reset chart session
        self.client.send('chart_create_session', [self.chart_session_id])
    
    def fetch_more(self, number: int = 1) -> None:
        """Fetch more historical data"""
        self.client.send('request_more_data', [self.chart_session_id, number])
    
    # Event handlers
    def on_symbol_loaded(self, callback: Callable[[], None]) -> None:
        """Register callback for symbol loaded event"""
        self.callbacks['symbolLoaded'].append(callback)
    
    def on_update(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register callback for update event"""
        self.callbacks['update'].append(callback)
    
    def on_error(self, callback: Callable[[str, None], None]) -> None:
        """Register callback for error event"""
        self.callbacks['error'].append(callback)
    
    def delete(self) -> None:
        """Delete the chart session"""
        self.client.remove_session(self.chart_session_id)