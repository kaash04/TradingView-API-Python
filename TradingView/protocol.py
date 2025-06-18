"""
Protocol handling for TradingView WebSocket packets
"""

import json
import re
from typing import List, Dict, Any, Union


class Protocol:
    """Handles TradingView's custom WebSocket packet format"""
    
    # Regex patterns for packet parsing
    CLEANER_REGEX = re.compile(r'~h~')
    SPLITTER_REGEX = re.compile(r'~m~[0-9]{1,}~m~')
    
    @staticmethod
    def parse_ws_packet(data: str) -> List[Dict[str, Any]]:
        """
        Parse WebSocket packet data
        
        Args:
            data: Raw WebSocket data string
            
        Returns:
            List of parsed TradingView packets
        """
        # Remove ping packets and split by packet markers
        cleaned_data = Protocol.CLEANER_REGEX.sub('', data)
        packets = Protocol.SPLITTER_REGEX.split(cleaned_data)
        
        parsed_packets = []
        for packet in packets:
            if not packet:
                continue
            try:
                parsed = json.loads(packet)
                parsed_packets.append(parsed)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse packet: {packet}")
                continue
                
        return parsed_packets
    
    @staticmethod
    def format_ws_packet(packet: Union[Dict[str, Any], str]) -> str:
        """
        Format packet for WebSocket transmission
        
        Args:
            packet: Packet data (dict or string)
            
        Returns:
            Formatted WebSocket packet string
        """
        if isinstance(packet, dict):
            msg = json.dumps(packet)
        else:
            msg = str(packet)
        
        return f"~m~{len(msg)}~m~{msg}" 