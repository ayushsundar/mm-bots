from src.utils.market_env import MarketMakingBot

sports_params = {
    'initialization_params': {'default_initialization_pb': 0.98},
}

if __name__ == "__main__":
    bot = MarketMakingBot(sports_params)
    bot.submit_orders()  # just places confident final bid/ask
