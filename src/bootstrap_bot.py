from src.utils.market_env import MarketMakingBot

bootstrap_params = {
    # Starting with a 50/50 market
      'initialization_params': {'default_initialization_pb': 0.5},

        'fill_reaction_params': {
            'base_movement_pb': 0.01,
            # Moving more based on the percentage filled
            'size_schedule': [
                {'filled_size_frac': 0, 'movement_mult': 0},
                {'filled_size_frac': 0.5, 'movement_mult': 0.3},
                {'filled_size_frac': 1, 'movement_mult': 1},
            ],
            # The more I believe that the current market is mispriced, the greater I'll move to capture it
            'mark_edge_schedule': [
                {'mark_edge_pb': 0, 'movement_mult': 1},
                {'mark_edge_pb': 0.02, 'movement_mult': 1.1},
                {'mark_edge_pb': 0.04, 'movement_mult': 1.2},
            ],
        },
        
        'edge_params': {
            'base_edge_pb': 0.02,
            'decaying_edge_params': {
                'decay_halflife_seconds': 30,

                # My edge increases with the size of my net position, and the additional edge decays oevr time(halves the impact every 30 seconds if no new fills occur)
                'decay_size_schedule': [
                    {'decaying_size': 100, 'additional_edge_pb': 0},
                    {'decaying_size': 500, 'additional_edge_pb': 0.01},
                    {'decaying_size': 5000, 'additional_edge_pb': 0.02},
                ],
            },
        },
        
        'size_params': {
            'base_size_dollars': 100,
            # The greater my position over the last 30 seconds or so, the less inclined I am to take on more risk, so reduce size_mult accordingly
            'decaying_edge_params': {
                'decay_halflife_seconds': 30,
                'decay_size_schedule': [
                    {'decaying_size': 100, 'size_mult': 1},
                    {'decaying_size': 500, 'size_mult': 0.8},
                    {'decaying_size': 5000, 'size_mult': 0.5},
                ],
            },
            
            # The more money I have on one side, the more risk averse I am so reduce my size_mult accordingly
            'net_position_schedule': [
                {'net_position_dollars': 0, 'size_mult': 1},
                {'net_position_dollars': 5000, 'size_mult': 0.8},
                {'net_position_dollars': 10000, 'size_mult': 0.5},
            ],
        },
}

if __name__ == "__main__":
    bot = MarketMakingBot(bootstrap_params)
    bot.log_status()

    # Simulate order fills
    bot.simulate_fill(fill_size=50, resting_order_size=100)
    bot.simulate_fill(fill_size=-30, resting_order_size=100)
