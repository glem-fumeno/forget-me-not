import os
from api.agent import Agent
from api.logging import logger


class Method:
    def __init__(self, agent: Agent):
        self.logger = logger
        self.agent = agent
        self.config = os.environ
