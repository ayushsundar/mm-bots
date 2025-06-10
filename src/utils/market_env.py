import time
import numpy as np

class MarketMakingBot:
    def __init__(self, params):
        self.params = params
        self.true_value = params['initialization_params']['default_initialization_pb']
        self.edge = params['edge_params']['base_edge_pb']
        self.size = params['size_params']['base_size_dollars']
        self.last_fill_time = time.time()
        self.net_position = 0

    def update_true_value(self, fill_size, resting_order_size):
        # Compute fill size fraction
        filled_size_frac = fill_size / resting_order_size
        
        # Find movement multiplier from size schedule
        movement_mult = self._get_schedule_value(
            self.params['fill_reaction_params']['size_schedule'], 
            'filled_size_frac', filled_size_frac, 'movement_mult')

        # Find mark edge multiplier
        mark_edge_mult = self._get_schedule_value(
            self.params['fill_reaction_params']['mark_edge_schedule'], 
            'mark_edge_pb', self.edge, 'movement_mult')

        # Calculate total movement
        delta = self.params['fill_reaction_params']['base_movement_pb'] * movement_mult * mark_edge_mult
        
        # Adjust true value based on aggressor direction (simplified: always move towards fill)
        self.true_value += delta if fill_size > 0 else -delta
        
    def update_edge(self):
        # Decay edge based on time since last fill
        elapsed = time.time() - self.last_fill_time
        decay = np.exp(-elapsed / self.params['edge_params']['decaying_edge_params']['decay_halflife_seconds'])
        
        # Adjust edge based on decay schedule
        decay_size = abs(self.net_position)
        additional_edge = self._get_schedule_value(
            self.params['edge_params']['decaying_edge_params']['decay_size_schedule'], 
            'decaying_size', decay_size, 'additional_edge_pb')
        
        self.edge = self.params['edge_params']['base_edge_pb'] + additional_edge * decay

    def update_size(self):
        # Decay size similarly to edge
        elapsed = time.time() - self.last_fill_time
        decay = np.exp(-elapsed / self.params['size_params']['decaying_edge_params']['decay_halflife_seconds'])
        
        # Adjust size based on decay schedule
        decay_size = abs(self.net_position)
        size_mult = self._get_schedule_value(
            self.params['size_params']['decaying_edge_params']['decay_size_schedule'], 
            'decaying_size', decay_size, 'size_mult')
        
        # Adjust based on net position schedule
        net_size_mult = self._get_schedule_value(
            self.params['size_params']['net_position_schedule'], 
            'net_position_dollars', abs(self.net_position), 'size_mult')
        
        self.size = self.params['size_params']['base_size_dollars'] * size_mult * net_size_mult * decay
    
    def _get_schedule_value(self, schedule, key_name, input_val, output_name):
        """
        Finds the appropriate multiplier in a piecewise linear schedule.
        """
        for i in range(len(schedule)-1):
            if schedule[i][key_name] <= input_val < schedule[i+1][key_name]:
                return schedule[i][output_name]
        return schedule[-1][output_name]
    
    def log_status(self):
        print(f"True Value: {self.true_value:.4f}, Edge: {self.edge:.4f}, Size: {self.size:.2f}, Net Position: {self.net_position}")

    # Placeholder for how you might submit orders to Polymarket's API
    def submit_orders(self):
        bid = self.true_value - self.edge
        ask = self.true_value + self.edge
        size_bid = self.size
        size_ask = self.size
        print(f"Submitting bid: {bid:.4f}, ask: {ask:.4f}")
        # In real implementation, connect to Polymarket API here

    # For testing logic
    def simulate_fill(self, fill_size, resting_order_size):
        self.update_true_value(fill_size, resting_order_size)
        self.update_edge()
        self.update_size()
        self.last_fill_time = time.time()
        self.net_position += fill_size

        self.log_status()