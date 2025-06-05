from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Enum as SAEnum
from pydantic import field_validator
from enum import Enum


class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: str = Field(
        default_factory=lambda: str(uuid4()), primary_key=True, nullable=False
    )
    size: int = Field(default=2000)
    max_risk_percentage: float = Field(default=2)
    max_active_trades: int = Field(default=3)
    open_trades: List["Trade"] = Relationship(back_populates="account")
    


class Timeframe(Enum):
    """Standard trading timeframes for chart intervals.
    
    - 1m: 1 minute
    - 5m: 5 minutes
    - 15m: 15 minutes
    - 30m: 30 minutes
    - 1h: 1 hour
    - 4h: 4 hours
    - 1d: 1 day
    - 1w: 1 week
    - 1mo: 1 month
    """
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"
    ONE_MONTH = "1mo"



class SetupType(str, Enum):
    BREAKOUT = "Breakout"
    RETEST = "Retest"
    FLAG = "Flag"
    TRIANGLE = "Triangle"
    PULLBACK = "Pullback"
    OTHER = "Other"

class VolumeAnalysis(str, Enum):
    INCREASING = "Increasing"
    DECREASING = "Decreasing"
    BREAKOUT = "Breakout volume"
    UNKNOWN = "Unknown"

class MAPosition(str, Enum):
    ABOVE_20MA = "Above 20MA"
    BELOW_20MA = "Below 20MA"
    ABOVE_50MA = "Above 50MA"
    BELOW_50MA = "Below 50MA"
    UNKNOWN = "Unknown"

class TrendDirection(str, Enum):
    UP = "Up"
    DOWN = "Down"
    SIDEWAYS = "Sideways"
    UNKNOWN = "Unknown"

class TradeStatus(str, Enum):
    WATCHING = "Watching"
    ENTERED = "Entered"
    EXITED = "Exited"

class Trade(SQLModel, table=True):
    """Represents a trade entry in the journal, including technical, execution, and risk details."""
    __tablename__ = "trade"
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)

    # Basic Info
    symbol: str = Field(nullable=False, description="Ticker symbol")
    date_identified: datetime = Field(default_factory=datetime.now, description="Date the setup was identified")
    current_price: Optional[float] = Field(default=None, description="Current price at time of analysis")
    setup_type: Optional[SetupType] = Field(default=None, description="Type of setup (Breakout, Retest, etc.)")
    timeframe: "Timeframe" = Field(sa_column=Column(SAEnum("Timeframe"), nullable=False), description="Chart timeframe")
    rating: int = Field(default=0, le=10, description="Overall rating out of 10")

    # Technical Analysis
    key_resistance: Optional[str] = Field(default=None, description="Key resistance level(s)")
    key_support: Optional[str] = Field(default=None, description="Key support level(s)")
    pattern_description: Optional[str] = Field(default=None, description="Pattern notes/description")
    volume_analysis: Optional[VolumeAnalysis] = Field(default=None, description="Volume analysis type")
    ma_position: Optional[MAPosition] = Field(default=None, description="MA position (above/below 20MA/50MA)")
    trend_direction: Optional[TrendDirection] = Field(default=None, description="Trend direction")

    # Execution Plan
    primary_entry_strategy: Optional[str] = Field(default=None, description="Primary entry strategy")
    entry_price_target: Optional[float] = Field(default=None, description="Target entry price")
    alternative_entry: Optional[str] = Field(default=None, description="Alternative entry plan")
    position_size: Optional[int] = Field(default=None, description="Position size in shares")

    # Risk Management
    stop_loss: Optional[float] = Field(default=None, description="Stop loss price")
    risk_reward_ratio: Optional[float] = Field(default=None, description="Risk/reward ratio")

    # Profit Strategy
    target1: Optional[float] = Field(default=None, description="Conservative profit target")
    target2: Optional[float] = Field(default=None, description="Extended profit target")
    trailing_stop_plan: Optional[str] = Field(default=None, description="Trailing stop plan")
    exit_strategy: Optional[str] = Field(default=None, description="Exit strategy (e.g., scale out 50/50)")

    # Trade Reasoning
    reasoning_1: Optional[str] = Field(default=None, description="First reason for this setup")
    reasoning_2: Optional[str] = Field(default=None, description="Second reason for this setup")
    reasoning_3: Optional[str] = Field(default=None, description="Third reason for this setup")
    what_could_go_wrong: Optional[str] = Field(default=None, description="Potential pitfalls of the setup")

    # Catalysts/News
    catalysts: Optional[str] = Field(default=None, description="Catalysts or news impacting the trade")

    # Trade Status
    status: TradeStatus = Field(default=TradeStatus.WATCHING, description="Trade status")
    entry_time: Optional[datetime] = Field(default=None, description="Date/time trade was entered")
    entry_price: Optional[float] = Field(default=None, description="Actual entry price")
    exit_time: Optional[datetime] = Field(default=None, description="Date/time trade was exited")
    exit_price: Optional[float] = Field(default=None, description="Actual exit price")
    pnl: Optional[float] = Field(default=None, description="Profit and Loss in $")
    lessons_learned: Optional[str] = Field(default=None, description="Lessons learned from this trade")

    # Relationships
    account_id: str = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="open_trades")

    @field_validator("rating")
    def rating_max_ten(cls, v):
        if v > 10:
            raise ValueError("rating must be less than or equal to 10")
        return v  


class MonthlyPerformanceSummary(SQLModel, table=True):
    """Summary of monthly trading performance, statistics, best/worst trades, lessons, and goals."""
    __tablename__ = "monthly_performance_summary"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, nullable=False)
    month: str = Field(nullable=False, description="Month in YYYY-MM format")

    # Statistics
    total_trades: int = Field(default=0, description="Total number of trades")
    winning_trades: int = Field(default=0, description="Number of winning trades")
    losing_trades: int = Field(default=0, description="Number of losing trades")
    win_rate: float = Field(default=0.0, description="Win rate as a percentage")
    total_pnl: float = Field(default=0.0, description="Total profit and loss in $")
    account_growth: float = Field(default=0.0, description="Account growth as a percentage")

    # Best Trade
    best_trade_symbol: Optional[str] = Field(default=None, description="Symbol of best trade")
    best_trade_pnl: Optional[float] = Field(default=None, description="P&L of best trade")
    best_trade_what_worked: Optional[str] = Field(default=None, description="What worked in best trade")

    # Worst Trade
    worst_trade_symbol: Optional[str] = Field(default=None, description="Symbol of worst trade")
    worst_trade_pnl: Optional[float] = Field(default=None, description="P&L of worst trade")
    worst_trade_what_went_wrong: Optional[str] = Field(default=None, description="What went wrong in worst trade")

    # Key Lessons Learned
    lessons: Optional[str] = Field(default=None, description="First key lesson learned")

    # Goals for Next Month
    goals: Optional[str] = Field(default=None, description="First goal for next month")

    # Relationships
    account_id: str = Field(foreign_key="account.id")
    account: "Account" = Relationship(back_populates="monthly_performance_summaries")

