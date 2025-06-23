# mm-bots 🧠📈

For this project, I built three different market-making bots, each one simulating how pricing behavior changes depending on what the bot knows.

I built this to explore how different kinds of information (or lack of it) affect market behavior. It’s a fun way to model the types of players you’d actually find in event-driven markets like sports, politics, or early-stage AMMs.

---

### 🏀 SportsArbBot (Fully Informed)

- Simulates a sports market (e.g. NBA game) right as it ends.
- Pulls mocked odds from DraftKings and FanDuel.
- Represents an **arbitrageur** who prices confidently around known outcomes.
- Good for modeling price convergence and fast arbitrage behavior.

---

### 🗳️ PoliticsBot (Partially Informed)

- Simulates a prediction market on **"Will Democrats win the House in 2026?"**
- Scrapes poll data (Quantus, Cygnal) and mixes it with prediction market odds (Polymarket, PredictIt).
- Final implied prob: **2/3 market data + 1/3 polling data**
- Represents someone trading off market wisdom and noisy polling — like a hedge fund analyst, but more chaotic.

---

### 💧 SeedBot (Uninformed)

- Has no clue what’s going on — just quotes and fills to create liquidity.
- Doesn’t care about the outcome, just uses order flow to adjust quotes.
- Meant to simulate a platform-seeded AMM or early-stage bootstrapping bot.

---
