from typing import List, Dict, Any

from logger_config import logger

class Memory:
    def __init__(self):
        self.iteration = 0
        self.iteration_responses = []
        self.results = []
        self.max_iterations = 10
        logger.info("Memory layer initialized")
    
    def reset(self):
        """Reset memory state"""
        logger.info("Resetting memory state")
        self.iteration = 0
        self.iteration_responses = []
        self.powerpoint_opened = False
        self.last_result = None
        
    def update_state(self, state):
        """Update memory with new state"""
        logger.debug(f"Updating state with: {state}")
        if isinstance(state, dict):
            self.iteration_responses.append(state)
        else:
            self.iteration_responses.append({'command': state})
        self.iteration += 1
        logger.info(f"State updated, iteration: {self.iteration}")
        
    def store_result(self, result):
        """Store the result of the last action"""
        logger.debug(f"Storing result: {result}")
        self.last_result = result
        
    def get_last_result(self):
        """Get the result of the last action"""
        logger.debug("Retrieving last result")
        return self.last_result
        
    def should_continue(self) -> bool:
        """Check if iteration should continue"""
        should_continue = self.iteration < self.max_iterations
        logger.debug(f"Should continue check: {should_continue}")
        return should_continue