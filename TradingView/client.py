"""
TradingView Client - Main WebSocket client for TradingView API
"""

import asyncio
import json
import logging
from typing import Dict, List, Callable, Any, Optional
import websockets

from .protocol import Protocol
from .utils import gen_session_id
from .types import MarketInfos


class Client:
    """
    Main TradingView client for WebSocket communication
    """
    
    def __init__(self, debug: bool = False, server: str = "data"):
        """
        Initialize TradingView client
        
        Args:
            debug: Enable debug logging
            server: TradingView server (data, prodata, widgetdata)
        """
        self.debug = debug
        self.server = server
        self.websocket = None
        self.logged = False
        self.connected = False  # Track connection state manually
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.send_queue: List[str] = []
        
        # Event callbacks
        self.callbacks = {
            'connected': [],
            'disconnected': [],
            'logged': [],
            'ping': [],
            'data': [],
            'error': [],
            'event': []
        }
        
        # Setup logging only if debug is enabled
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            # Disable logging for non-debug mode
            self.logger.disabled = True
    
    @property
    def is_open(self) -> bool:
        """Check if WebSocket connection is open"""
        return self.websocket is not None and self.connected
    
    def on_connected(self, callback: Callable[[], None]) -> None:
        """Register callback for connection event"""
        self.callbacks['connected'].append(callback)
    
    def on_disconnected(self, callback: Callable[[], None]) -> None:
        """Register callback for disconnection event"""
        self.callbacks['disconnected'].append(callback)
    
    def on_logged(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register callback for login event"""
        self.callbacks['logged'].append(callback)
    
    def on_ping(self, callback: Callable[[int], None]) -> None:
        """Register callback for ping event"""
        self.callbacks['ping'].append(callback)
    
    def on_data(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register callback for data event"""
        self.callbacks['data'].append(callback)
    
    def on_error(self, callback: Callable[[str, ...], None]) -> None:
        """Register callback for error event"""
        self.callbacks['error'].append(callback)
    
    def on_event(self, callback: Callable[[str, ...], None]) -> None:
        """Register callback for any event"""
        self.callbacks['event'].append(callback)
    
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
    
    def _parse_packet(self, data: str) -> None:
        """Parse incoming WebSocket packets"""
        if not self.is_open:
            return
        
        packets = Protocol.parse_ws_packet(data)
        
        for packet in packets:
            if self.debug:
                self.logger.debug(f"CLIENT PACKET: {packet}")
            
            # Handle ping packets
            if isinstance(packet, int):
                try:
                    asyncio.create_task(self.websocket.send(Protocol.format_ws_packet(f"~h~{packet}")))
                    self._handle_event('ping', packet)
                except Exception as e:
                    self.logger.error(f"Error sending ping response: {e}")
                continue
            
            # Handle protocol errors
            if isinstance(packet, dict) and packet.get('m') == 'protocol_error':
                self._handle_error('Client critical error:', packet.get('p', ''))
                try:
                    asyncio.create_task(self.websocket.close())
                except Exception as e:
                    self.logger.error(f"Error closing connection: {e}")
                return
            
            # Handle normal packets with session routing
            if isinstance(packet, dict) and 'm' in packet and 'p' in packet:
                parsed = {
                    'type': packet['m'],
                    'data': packet['p']
                }
                
                session = packet['p'][0] if packet['p'] else None
                if session and session in self.sessions:
                    self.sessions[session]['onData'](parsed)
                    continue
            
            # Handle initial session data (login response) - this is the key fix
            if not self.logged:
                # The first packet after connection contains session info
                # Check if it's session data (has session_id field)
                if isinstance(packet, dict) and 'session_id' in packet:
                    self.logged = True  # Set logged to True when we get session response
                    self._handle_event('logged', packet)
                    continue
                else:
                    # For other initial packets, still treat as logged
                    self.logged = True
                    self._handle_event('logged', packet)
                    continue
            
            # Handle other data
            self._handle_event('data', packet)
    
    def send(self, packet_type: str, data: List[Any] = None) -> None:
        """Send a packet to TradingView"""
        if data is None:
            data = []
        
        packet = Protocol.format_ws_packet({
            'm': packet_type,
            'p': data
        })
        
        self.send_queue.append(packet)
        self._send_queue()
    
    def _send_queue(self) -> None:
        """Send all queued packets"""
        while self.is_open and self.logged and self.send_queue:
            packet = self.send_queue.pop(0)
            try:
                asyncio.create_task(self.websocket.send(packet))
                if self.debug:
                    self.logger.debug(f"SENT: {packet}")
            except Exception as e:
                self.logger.error(f"Error sending packet: {e}")
                break
    
    async def connect(self) -> None:
        """Connect to TradingView WebSocket"""
        try:
            # Create WebSocket connection
            uri = f"wss://{self.server}.tradingview.com/socket.io/websocket?type=chart"
            
            # Try different approaches for headers based on websockets version
            try:
                # Method 1: additional_headers (newer versions)
                self.websocket = await websockets.connect(
                    uri, 
                    additional_headers=[('Origin', 'https://www.tradingview.com')]
                )
            except TypeError:
                try:
                    # Method 2: extra_headers (older versions)
                    self.websocket = await websockets.connect(
                        uri, 
                        extra_headers={'Origin': 'https://www.tradingview.com'}
                    )
                except TypeError:
                    # Method 3: No headers (fallback)
                    self.websocket = await websockets.connect(uri)
            
            # Set connection state
            self.connected = True
            
            # Send authentication (anonymous)
            self.send_queue.insert(0, Protocol.format_ws_packet({
                'm': 'set_auth_token',
                'p': ['unauthorized_user_token']
            }))
            # Don't set logged to True yet - wait for session response
            
            self._handle_event('connected')
            self._send_queue()
            
            # Start listening for messages in the background
            asyncio.create_task(self._listen_for_messages())
                
        except Exception as e:
            self._handle_error(f"WebSocket error: {e}")
            self.connected = False
            raise
    
    async def _listen_for_messages(self) -> None:
        """Listen for WebSocket messages in the background"""
        try:
            async for message in self.websocket:
                self._parse_packet(message)
        except Exception as e:
            self._handle_error(f"Message listening error: {e}")
            self.connected = False
    
    def disconnect(self) -> None:
        """Disconnect from TradingView WebSocket"""
        if self.websocket:
            try:
                asyncio.create_task(self.websocket.close())
            except Exception as e:
                self.logger.error(f"Error closing connection: {e}")
            self.connected = False
            self.logged = False
            self._handle_event('disconnected')
    
    def create_session(self, session_type: str, on_data: Callable[[Dict[str, Any]], None]) -> str:
        """
        Create a new session
        
        Args:
            session_type: Type of session ('chart', 'quote', etc.)
            on_data: Callback for session data
            
        Returns:
            Session ID
        """
        session_id = gen_session_id(session_type[:2])
        self.sessions[session_id] = {
            'type': session_type,
            'onData': on_data
        }
        return session_id
    
    def remove_session(self, session_id: str) -> None:
        """Remove a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    # Session namespace
    class Session:
        """Session namespace for creating different session types"""
        
        def __init__(self, client: 'Client'):
            self.client = client
        
        @property
        def Chart(self):
            """Get Chart session class"""
            from .chart_session import ChartSession 