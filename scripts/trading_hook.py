#!/usr/bin/env python3
"""
UserPromptSubmit hook — detects stock/trading mentions and boots TradingAgents.
Reads Claude Code hook JSON from stdin, checks for finance keywords,
extracts a ticker if present, then launches the analysis in the background.
"""

import json
import os
import re
import subprocess
import sys

STOCK_KEYWORDS = re.compile(
    r"\b(stock|stocks|share|shares|ticker|equity|equities|"
    r"market cap|NYSE|NASDAQ|trading|portfolio|dividend|dividends|"
    r"earnings|bull|bear|IPO|ETF|hedge fund|S&P|Dow Jones|"
    r"index fund|options|futures|securities|investment|invest|"
    r"price target|analyst|valuation|P/E|EPS|revenue|market)\b",
    re.IGNORECASE,
)

# Common ticker pattern: 1–5 uppercase letters, optionally preceded by $ sign
TICKER_RE = re.compile(r"\$([A-Z]{1,5})\b|(?<!\w)([A-Z]{2,5})(?!\w)")

# Well-known tickers to help avoid false positives on all-caps words
COMPANY_TO_TICKER = {
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL", "alphabet": "GOOGL",
    "amazon": "AMZN", "nvidia": "NVDA", "meta": "META", "facebook": "META",
    "tesla": "TSLA", "netflix": "NFLX", "spotify": "SPOT", "uber": "UBER",
    "airbnb": "ABNB", "coinbase": "COIN", "palantir": "PLTR", "snowflake": "SNOW",
    "shopify": "SHOP", "square": "SQ", "paypal": "PYPL", "visa": "V",
    "mastercard": "MA", "jpmorgan": "JPM", "goldman": "GS", "morgan stanley": "MS",
    "berkshire": "BRK", "walmart": "WMT", "disney": "DIS", "boeing": "BA",
}

KNOWN_TICKERS = {
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA",
    "BRK", "JPM", "V", "UNH", "JNJ", "XOM", "PG", "MA", "HD", "CVX",
    "MRK", "ABBV", "LLY", "PEP", "KO", "AVGO", "COST", "MCD", "TMO",
    "ACN", "NKE", "DHR", "TXN", "PM", "AMD", "QCOM", "INTC", "BA",
    "GS", "MS", "BAC", "WFC", "C", "BLK", "SPY", "QQQ", "DIA", "IWM",
    "BTC", "ETH", "SOL", "ADA",
}

NOISE_WORDS = {
    "I", "A", "AN", "THE", "BE", "IS", "IT", "IN", "ON", "AT", "TO",
    "DO", "IF", "OR", "AS", "OF", "BY", "UP", "SO", "GO", "NO", "MY",
    "WE", "HE", "ME", "US", "HI", "OK", "AI", "ML", "API", "UI", "UX",
    "ID", "IP", "DB", "OS", "CD", "TV", "VPN", "PDF", "URL", "CSS",
    "HTML", "JSON", "SQL", "CLI", "SDK", "IDE", "CPU", "GPU", "RAM",
}


def extract_ticker(prompt: str) -> str:
    """Return the best ticker guess from the prompt, or empty string."""
    # Priority 1: $TICKER notation
    dollar = re.findall(r"\$([A-Z]{1,5})\b", prompt)
    if dollar:
        return dollar[0]

    # Priority 2: known ticker in message
    words = re.findall(r"\b[A-Z]{1,5}\b", prompt)
    for w in words:
        if w in KNOWN_TICKERS:
            return w

    # Priority 3: company name mention
    prompt_lower = prompt.lower()
    for company, ticker in COMPANY_TO_TICKER.items():
        if company in prompt_lower:
            return ticker

    return ""


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = payload.get("prompt", "") or payload.get("message", "") or ""
    if not prompt:
        sys.exit(0)

    if not STOCK_KEYWORDS.search(prompt):
        sys.exit(0)

    ticker = extract_ticker(prompt) or "NVDA"  # default to NVDA if none found

    repo = "/home/user/trading-clone"
    log_file = f"{repo}/logs/analysis_{ticker}.log"
    os.makedirs(f"{repo}/logs", exist_ok=True)

    # Launch analysis in background (non-blocking)
    cmd = (
        f"cd {repo} && "
        f"ANALYSIS_TICKER={ticker} python -c \""
        f"import sys; sys.path.insert(0, '.'); "
        f"from tradingagents.default_config import DEFAULT_CONFIG; "
        f"from tradingagents.graph.trading_graph import TradingAgentsGraph; "
        f"import os; "
        f"ticker = os.environ.get('ANALYSIS_TICKER', 'NVDA'); "
        f"ta = TradingAgentsGraph(debug=False, config=DEFAULT_CONFIG.copy()); "
        f"_, decision = ta.propagate(ticker, None); "
        f"print(decision)\" "
        f">> {log_file} 2>&1"
    )

    subprocess.Popen(cmd, shell=True, start_new_session=True)

    # Inject a system message back to Claude so it knows the team is working
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"[TradingAgents] Wall Street research team activated for ticker: {ticker}. "
                f"Analysts (fundamentals, news, sentiment, technical, social) are running a full debate. "
                f"Results will be written to {log_file}. "
                f"You can mention 'show trading results' to read the latest analysis."
            ),
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
