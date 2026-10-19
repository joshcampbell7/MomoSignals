import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")
MARKET_ORDER = {"moneyline": 0, "child_moneyline": 1, "totals": 2}
TRADABLE_SPREAD = 0.05
SPORTS = {
    "valorant": {"valorant", "val"},
}


class LinkError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


def build_market_body(url: str) -> dict:
    slug = slug_from_polymarket_url(url)
    event = fetch_event(slug)
    sport = sport_slug(event)
    ensure_valorant(sport)
    markets = event.get("markets") or []
    metadata = event.get("eventMetadata") or {}

    return {
        "polymarketUrl": url.strip(),
        "slug": event.get("slug") or slug,
        "sport": sport,
        "title": event.get("title"),
        "startTime": event.get("startTime"),
        "teams": [team_body(team) for team in event.get("teams") or []],
        "match": {
            "league": metadata.get("league"),
            "series": metadata.get("serie"),
            "tournament": metadata.get("tournament"),
            "pandascoreMatchId": metadata.get("pandascoreMatchId"),
        },
        "markets": [market_body(market) for market in sorted_markets(markets)],
    }


def slug_from_polymarket_url(url: str) -> str:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    parts = [part for part in parsed.path.split("/") if part]

    if parsed.scheme not in {"http", "https"} or host != "polymarket.com" or not parts:
        raise LinkError("Paste a Polymarket link.")

    slug = parts[-1].lower()
    if not SLUG_PATTERN.fullmatch(slug):
        raise LinkError("Paste a Polymarket link.")
    return slug


def ensure_valorant(sport: str | None) -> None:
    if sport == "valorant":
        return
    raise LinkError("That Polymarket link is not a Valorant market.")


def sport_slug(event: dict) -> str | None:
    labels = set()
    for tag in event.get("tags") or []:
        labels.add(str(tag.get("slug") or "").lower())
        labels.add(str(tag.get("label") or "").lower())
    for series in event.get("series") or []:
        labels.add(str(series.get("slug") or "").lower())

    sport = event.get("sport") or {}
    if isinstance(sport, dict):
        labels.add(str(sport.get("sport") or "").lower())
        labels.add(str(sport.get("name") or "").lower())

    for name, aliases in SPORTS.items():
        if labels & aliases:
            return name
    return None


def fetch_event(slug: str) -> dict:
    endpoint = f"https://gamma-api.polymarket.com/events/slug/{slug}"
    request = Request(endpoint, headers={"User-Agent": "MomoSignals/0.1"})
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise LinkError("No Polymarket event found for that link.", 404) from error
        raise LinkError("Polymarket did not return this event.", 502) from error
    except URLError as error:
        raise LinkError("Could not reach Polymarket.", 502) from error
    except json.JSONDecodeError as error:
        raise LinkError("Polymarket returned an unreadable event.", 502) from error


def sorted_markets(markets: list) -> list:
    ranked = sorted(
        enumerate(markets),
        key=lambda item: (MARKET_ORDER.get(item[1].get("sportsMarketType"), 9), item[0]),
    )
    return [market for _, market in ranked]


def market_body(market: dict) -> dict:
    outcomes = parse_list(market.get("outcomes"))
    prices = parse_list(market.get("outcomePrices"))
    best_bid = as_float(market.get("bestBid"))
    best_ask = as_float(market.get("bestAsk"))
    spread = as_float(market.get("spread"))
    volume = as_amount(market.get("volumeNum", market.get("volume")))

    return {
        "marketName": market.get("groupItemTitle") or market.get("question"),
        "type": market.get("sportsMarketType"),
        "line": as_float(market.get("line")),
        "outcome1": outcome_body(outcomes, prices, 0, best_bid, best_ask),
        "outcome2": outcome_body(outcomes, prices, 1, complement(best_ask), complement(best_bid)),
        "spread": spread,
        "volume": volume,
        "liquidity": as_amount(market.get("liquidityNum", market.get("liquidity"))),
        "tradable": spread is not None and spread <= TRADABLE_SPREAD and volume > 0,
    }


def outcome_body(outcomes: list, prices: list, index: int, best_bid, best_ask) -> dict:
    return {
        "name": outcomes[index] if index < len(outcomes) else None,
        "price": as_float(prices[index]) if index < len(prices) else None,
        "bestBid": best_bid,
        "bestAsk": best_ask,
    }


def team_body(team: dict) -> dict:
    return {
        "name": team.get("name"),
        "abbreviation": team.get("abbreviation"),
        "side": team.get("ordering"),
    }


def parse_list(value) -> list:
    if isinstance(value, list):
        return value
    if not value:
        return []
    parsed = json.loads(value)
    return parsed if isinstance(parsed, list) else []


def as_float(value):
    if value is None or value == "":
        return None
    return round(float(value), 4)


def as_amount(value) -> float:
    number = as_float(value)
    return 0 if number is None else number


def complement(price):
    if price is None:
        return None
    return round(1 - price, 4)
