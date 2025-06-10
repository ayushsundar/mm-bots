from src.utils.market_env import MarketMakingBot

"""
    Import current weightages for whatever market I'm making from places like Fanduel, Draftkings, and Prizepicks, 
    and weight them all iaccordingly to give me my starting point for this market 
"""
sports_params = {
    'initialization_params': {'default_initialization_pb': 0.5},

}

if __name__ == "__main__":
    bot = MarketMakingBot(sports_params)
    bot.submit_orders()
