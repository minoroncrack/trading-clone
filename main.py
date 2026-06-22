import os
import sys

# ---------------------------------------------------------------------------
# Mode selection:
#   RULE_BASED=true  → no LLM, no credits, runs immediately
#   RULE_BASED=false → full LLM-powered analyst team (requires API credits)
# Default: rule-based when no LLM credits are detected
# ---------------------------------------------------------------------------

RULE_BASED = os.environ.get("RULE_BASED", "true").lower() != "false"
TICKER = os.environ.get("ANALYSIS_TICKER", "NVDA")
DATE = os.environ.get("ANALYSIS_DATE", None)

if RULE_BASED:
    from tradingagents.agents.analysts.rule_based_analyst import run_analysis

    print(f"\n[TradingAgents] Rule-based mode — no LLM credits required")
    print(f"[TradingAgents] Analysing {TICKER}...\n")

    result = run_analysis(TICKER, DATE)
    print(result["report"])
    print(f"\nDecision: {result['decision']}  |  Score: {result['score']:+d}")

else:
    from tradingagents.default_config import DEFAULT_CONFIG
    from tradingagents.graph.trading_graph import TradingAgentsGraph

    config = DEFAULT_CONFIG.copy()
    ta = TradingAgentsGraph(debug=True, config=config)
    _, decision = ta.propagate(TICKER, DATE or "2024-05-10")
    print(decision)
