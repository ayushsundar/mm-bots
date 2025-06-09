
# mm-bots 🧠📈

A simulation project exploring how market-making bots behave under different levels of information access. Each bot represents a distinct role commonly found in prediction or event-driven markets—ranging from fully informed arbitrage to liquidity bootstrapping.

## 🧪 Overview

This repo includes three market-making bots, each designed to explore strategy and pricing behavior in real-world-inspired scenarios:

### 1. SportsArbBot (Fully Informed – Sports Market 🏀)
- Simulates a bot operating in a sports market (e.g., NBA game) where the outcome becomes known shortly after the event ends.
- Represents a **fully informed arbitrageur** who aggressively prices around the true value once it's known.
- Useful for modeling price convergence and fast arbitrage behavior as resolution approaches.

### 2. ElectionTrackerBot (Partially Informed – Live Vote Market 🗳️)
- Simulates a bot trading in a **real-time election market** (e.g., Virginia’s June 2025 primary) where vote counts arrive gradually from precincts over time.
- Represents a **partially informed trader** who updates beliefs based on noisy or delayed voting data.
- Adjusts pricing cautiously early on, increasing confidence as more vote data rolls in.
- Useful for modeling real-time belief formation in high-stakes political prediction markets.

### 3. SeedBot (Uninformed – Liquidity Bootstrapping 💧)
- Designed to **seed liquidity and encourage trading activity**, rather than to maximize profit.
- Operates with **no information** about the true outcome and uses fill-based signals to adapt bid/ask spreads and order sizes.
- Models early-stage market makers or AMMs deployed to jumpstart market activity and improve price discovery.
