from src.utils.market_env import MarketMakingBot
from src.politics.poll_scraper import get_quantus_cygnal_polls
from datetime import datetime, timezone

# Mocked prediction market data from Polymarket & PredictIt
def mock_market_data():
    return {
        "polymarket": 0.61,
        "predictit": 0.58,
    }

# Equal weights for polls
POLL_WEIGHTS = {
    "quantus": 0.5,
    "cygnal": 0.5,
}

# Equal weights for prediction markets
MARKET_WEIGHTS = {
    "polymarket": 0.5,
    "predictit": 0.5,
}

# Weighted average of values based on weight dict
def weighted_avg(data, weights):
    return sum(data[src] * weights[src] for src in data)
# Pull & parse poll data

def get_poll_data():
    polls = get_quantus_cygnal_polls()
    poll_dict = {}

    for poll in polls:
        pollster = poll["pollster"].lower()
        dem_support = poll["dem"]  # Using Dem vote share as proxy
        if pollster in POLL_WEIGHTS:
            poll_dict[pollster] = dem_support

    return poll_dict

# Get final weighted probability with 2/3 weight on markets
def get_weighted_true_val():
    polls = get_poll_data()
    markets = mock_market_data()

    poll_val = weighted_avg(polls, POLL_WEIGHTS)
    market_val = weighted_avg(markets, MARKET_WEIGHTS)

    return (2/3) * market_val + (1/3) * poll_val

def build_params(weighted_prob):
    return {
        # Start at the weighted implied probability
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

    print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}] Weighted implied probability: {weighted_val:.5f}")

    politics_params = build_params(weighted_val)
    bot = MarketMakingBot(politics_params)
    bot.submit_orders()