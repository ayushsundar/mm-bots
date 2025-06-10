from src.utils.market_env import MarketMakingBot

bootstrap_params = {
    # your full param dictionary from the notebook
}

if __name__ == "__main__":
    bot = MarketMakingBot(bootstrap_params)
    bot.log_status()

    # Simulate order fills
    bot.simulate_fill(fill_size=50, resting_order_size=100)
    bot.simulate_fill(fill_size=-30, resting_order_size=100)
