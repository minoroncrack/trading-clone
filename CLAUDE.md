# CLAUDE.md — Session Briefing

## Who I Am

I'm building at the intersection of AI and finance. My primary project is a multi-agent trading framework (this repo — `trading-clone`) built on TradingAgents, a LangGraph-powered system that deploys specialized LLM agents to analyze markets like a real trading firm would. I move fast, think in systems, and care about decisions being explainable — not just correct.

---

## Repository Roles

### `trading-clone` — The Brain (Read-Only Reference)
This is the intelligence layer. It contains a full multi-agent trading framework:
- **Analysts**: Fundamentals, Sentiment, News, Technical, Rule-Based
- **Researchers**: Bull and Bear researchers who debate each other
- **Trader Agent**: Synthesizes analyst reports into trade decisions
- **Risk Management**: Conservative, Neutral, and Aggressive debators
- **Portfolio Manager**: Final approver of trade proposals
- **Data vendors**: yfinance, Alpha Vantage, FRED, Polymarket, StockTwits, Reddit

**Rule:** Do not modify this repo unless explicitly told to. Read it to understand business logic, data structures, agent behavior, and decision-making patterns. Use it to inform everything built in the active repo.

### Active Repo (Website / Product being built)
This is where all new code gets written. Every feature, page, and component built here should be consistent with the logic, data models, and decisions that live in `trading-clone`.

---

## How Claude Should Think

Before writing any code, ask:
1. Does `trading-clone` already handle this logic? If yes, mirror it — don't reinvent.
2. What data does TradingAgents produce, and how should the UI/product surface it?
3. Does this decision align with how the agent team (Analyst → Researcher → Trader → Risk → Portfolio Manager) reaches a conclusion?

When in doubt, check the source:
- Agent logic lives in `tradingagents/agents/`
- Data fetching lives in `tradingagents/dataflows/`
- Configuration lives in `tradingagents/default_config.py`
- State/memory lives in `tradingagents/agents/utils/`

---

## Tech Context

- **Framework**: TradingAgents v0.3.0, built on LangGraph
- **LLM Providers supported**: OpenAI, Anthropic, Google, xAI, DeepSeek, Qwen, GLM, MiniMax, OpenRouter, Ollama, Azure, Bedrock, any OpenAI-compatible endpoint
- **Data sources**: yfinance (OHLCV, fundamentals), Alpha Vantage (news), FRED (macro), Polymarket (prediction markets), StockTwits + Reddit (sentiment)
- **Markets**: US stocks, HK, Tokyo, London, India, Canada, Australia, China A-shares, Crypto
- **Memory**: Decision log at `~/.tradingagents/memory/trading_memory.md`, checkpoint resume via SQLite

---

## Coding Standards

- No unnecessary comments — well-named code speaks for itself
- No speculative features — build what's needed now
- No error handling for impossible cases — trust the framework
- Prefer editing existing files over creating new ones
- Keep it tight: three similar lines beats a premature abstraction

---

## Decision Hierarchy

When there's a conflict between what seems intuitive and what the trading framework does — trust the framework. It was designed deliberately: analysts debate, researchers push back, risk management stress-tests, and the portfolio manager decides. That chain of reasoning should be reflected in any product built on top of it.

---

## What to Always Do

- Check `trading-clone` before implementing any financial logic
- Match data field names and structures to what TradingAgents already produces
- Keep the agent pipeline (Analyst → Researcher → Trader → Risk → Portfolio Manager) visible in the product — users should feel the intelligence behind decisions
- Surface confidence, not just conclusions — show the bull/bear debate, show the risk score, show what drove the decision

---

## What to Never Do

- Don't hardcode financial logic that TradingAgents already computes dynamically
- Don't modify `trading-clone` without explicit instruction
- Don't build generic UIs — everything should feel purpose-built for trading intelligence
- Don't hide the AI — this product's value is the multi-agent reasoning; make it visible
