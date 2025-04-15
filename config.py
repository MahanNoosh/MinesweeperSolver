"""Configuration settings for the Minesweeper solver."""

from typing import Dict, Any
import os

# File paths
TEMPLATE_DIR = "template"
STATE_IMAGE = os.path.join(TEMPLATE_DIR, "state.png")
DEFAULT_TILE1 = os.path.join(TEMPLATE_DIR, "default_tile1.png")
DEFAULT_TILE2 = os.path.join(TEMPLATE_DIR, "default_tile2.png")
INTERSECTION1 = os.path.join(TEMPLATE_DIR, "intersection1.png")
INTERSECTION2 = os.path.join(TEMPLATE_DIR, "intersection2.png")

# Game settings
MAX_ITERATIONS = 100
MOVE_DELAY = 1.0  # seconds to wait between moves
SETUP_DELAY = 3.0  # seconds to wait during setup

# Image processing settings
SIMILARITY_THRESHOLD = 0.8  # threshold for image matching
TILE_MARGIN = 2  # pixels to exclude from tile edges

# Solver settings
class SolverConfig:
    """Configuration for the Minesweeper solver."""
    
    def __init__(self):
        self.debug_mode = False
        self.save_screenshots = True
        self.max_iterations = MAX_ITERATIONS
        self.move_delay = MOVE_DELAY
        self.setup_delay = SETUP_DELAY
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'debug_mode': self.debug_mode,
            'save_screenshots': self.save_screenshots,
            'max_iterations': self.max_iterations,
            'move_delay': self.move_delay,
            'setup_delay': self.setup_delay
        }
        
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'SolverConfig':
        """Create configuration from dictionary."""
        config = cls()
        for key, value in config_dict.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config

# Logging settings
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'minesweeper.log',
            'mode': 'a',
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
} 