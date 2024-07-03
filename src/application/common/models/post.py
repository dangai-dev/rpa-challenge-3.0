from dataclasses import dataclass


@dataclass
class Post:
    title: str
    description: str
    date: str
    image: str | None
    search_text_total: int
    has_money: bool
