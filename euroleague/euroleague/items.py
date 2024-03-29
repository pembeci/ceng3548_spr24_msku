# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Player:
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)
    stats: Dict[str, Any] = field(default_factory=lambda: {})

@dataclass
class Team:
    team_name: Optional[str] = field(default=None)
    team_code: Optional[str] = field(default=None)
    totals: Dict[str, Any] = field(default_factory=lambda: {})
    averages: Dict[str, Any] = field(default_factory=lambda: {})
