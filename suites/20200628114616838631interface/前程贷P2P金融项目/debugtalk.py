#debugtalk.py
import random

def get_us():
    user_agents = ["Mozilla/5.0 BenBen", "Mozilla/5.0 MaZai", "Mozilla/5.0 icon"]
    print(random.choice(user_agents))
    return random.choice(user_agents)