"""Pytest configuration file for agent_things tests"""

import os
import sys

# Add the src directory to Python path for test discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
