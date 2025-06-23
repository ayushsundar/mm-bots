from datetime import datetime
from src.utils.market_env import MarketMakingBot

# Mocked odds for public sharing
def mock_pulling_odds():
    return {
        "draftkings": +120,
        "fanduel": +105,
    }

# Convert the odds to implied probabilities
def convert_to_prob(odds):
    if odds > 0:
        return 100 / (odds + 100)
    return -odds / (-odds + 100)
 
# DraftKings weighted more since they're bigger and are usually more accurate
SPORTSBOOK_WEIGHTS = {
    "draftkings": .6,
    "fanduel": .4 
}

# Getting the weighted implied probability based on book odds
def get_weighted_true_val():
    odds = mock_pulling_odds()
    weighted_prob = []
    for bk, price in odds.items():
        if bk in SPORTSBOOK_WEIGHTS:
            weighted_prob.append(convert_to_prob(price) * SPORTSBOOK_WEIGHTS[bk])
    return sum(weighted_prob)

def build_params(weighted_prob):
    return {
         # Start at the weighted implied probability from both sportsbooks
        'initialization_params': {'default_initialization_pb': weighted_prob},

        'fill_reaction_params': {
            # Always move my market slightly on fills
            'base_movement_pb': 0.002,

            # Move more for large fill sizes
            'size_schedule': [
                {'filled_size_frac': 0.0, 'movement_mult': 0},
                {'filled_size_frac': 0.5, 'movement_mult': 0.15},
                {'filled_size_frac': 1.0, 'movement_mult': 0.30},
            ],
            # If my edge is higher, increase my movement
            'mark_edge_schedule': [
                {'mark_edge_pb': 0.000, 'movement_mult': 1},
                {'mark_edge_pb': 0.010, 'movement_mult': 1.1},
                {'mark_edge_pb': 0.020, 'movement_mult': 1.3},
            ],
        },

        'edge_params': {
            # 5 cent spread on each side (10 cents total)
            'base_edge_pb': 0.005,
            'decaying_edge_params': {
                'decay_halflife_seconds': 15,
                # Grow edge when inventory grows, then decay it quickly
                'decay_size_schedule': [
                    {'decaying_size': 0,     'additional_edge_pb': 0},
                    {'decaying_size': 1000,  'additional_edge_pb': 0.005},
                    {'decaying_size': 5000,  'additional_edge_pb': 0.010},
                ],
            },
        },

        'size_params': {
            'base_size_dollars': 500,

            # If we’ve traded a bunch in one direction in the last 20 s, size down
            'decaying_edge_params': {
                'decay_halflife_seconds': 20,
                'decay_size_schedule': [
                    {'decaying_size': 0,     'size_mult': 1},
                    {'decaying_size': 2500,  'size_mult': 0.7},
                    {'decaying_size': 7500,  'size_mult': 0.4},
                ],
            },

            # Cap the trade size as net inventory grows
            'net_position_schedule': [
                {'net_position_dollars': 0,     'size_mult': 1},
                {'net_position_dollars': 10000, 'size_mult': 0.6},
                {'net_position_dollars': 20000, 'size_mult': 0.3},
            ],
        },
    }

if __name__ == "__main__":
    weighted_val = get_weighted_true_val()

    print(f"[{datetime.utcnow():%Y-%m-%d %H:%M:%S}] Weighted implied probability: {weighted_val:.5f}")

    sports_params = build_params(weighted_val)
    bot = MarketMakingBot(sports_params)
    bot.submit_orders()