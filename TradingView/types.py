"""
Type definitions and constants for TradingView API
"""

from typing import TypedDict, List, Optional, Union, Literal

# TimeFrame type definition
TimeFrame = Literal[
    '1', '3', '5', '15', '30', '45', '60', '120', '180', '240',
    '1D', '1W', '1M', 'D', 'W', 'M'
]

# Market symbol type
MarketSymbol = str

# Chart types
ChartType = Literal['HeikinAshi', 'Renko', 'LineBreak', 'Kagi', 'PointAndFigure', 'Range']

# Chart type mappings
CHART_TYPES = {
    'HeikinAshi': 'BarSetHeikenAshi@tv-basicstudies-60!'
}

# Price period structure
class PricePeriod(TypedDict):
    time: int
    open: float
    close: float
    max: float
    min: float
    volume: float

# Subsession structure
class Subsession(TypedDict):
    id: str
    description: str
    private: bool
    session: str
    session_correction: str
    session_display: str

# Market information structure
class MarketInfos(TypedDict):
    series_id: str
    base_currency: str
    base_currency_id: str
    name: str
    full_name: str
    pro_name: str
    description: str
    short_description: str
    exchange: str
    listed_exchange: str
    provider_id: str
    currency_id: str
    currency_code: str
    variable_tick_size: str
    pricescale: int
    pointvalue: int
    session: str
    session_display: str
    type: str
    has_intraday: bool
    fractional: bool
    is_tradable: bool
    minmov: int
    minmove2: int
    timezone: str
    is_replayable: bool
    has_adjustment: bool
    has_extended_hours: bool
    bar_source: str
    bar_transform: str
    bar_fillgaps: bool
    allowed_adjustment: str
    subsession_id: str
    pro_perm: str
    base_name: List[str]
    legs: List[str]
    subsessions: List[Subsession]
    typespecs: List
    resolutions: List
    aliases: List
    alternatives: List

# Chart inputs for custom chart types
class ChartInputs(TypedDict, total=False):
    atrLength: Optional[int]
    source: Optional[Literal['open', 'high', 'low', 'close', 'hl2', 'hlc3', 'ohlc4']]
    style: Optional[Union[Literal['ATR'], str]]
    boxSize: Optional[int]
    reversalAmount: Optional[int]
    sources: Optional[Literal['Close']]
    wicks: Optional[bool]
    lb: Optional[int]
    oneStepBackBuilding: Optional[bool]
    phantomBars: Optional[bool]
    range: Optional[int]

# Chart options
class ChartOptions(TypedDict, total=False):
    timeframe: Optional[TimeFrame]
    range: Optional[int]
    to: Optional[int]
    adjustment: Optional[Literal['splits', 'dividends']]
    backadjustment: Optional[bool]
    session: Optional[Literal['regular', 'extended']]
    currency: Optional[str]
    type: Optional[ChartType]
    inputs: Optional[ChartInputs]
    replay: Optional[int] 