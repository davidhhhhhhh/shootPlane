import time
import pygame
from stable_baselines3 import DQN
from plane_battle_env import PlaneBattleEnv

# Load trained model
model = DQN.load("plane_battle_dqn")

# Create game environment
env = PlaneBattleEnv()
obs, _ = env.reset()
done = False

# Initialize Pygame display
env.render()

while not done:
    for event in pygame.event.get():  # Handle events to prevent freezing
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    action, _ = model.predict(obs)  # Get action from trained model
    obs, reward, done, _, _ = env.step(action)
    env.render()  # Render updated game state

    time.sleep(0.02)  # Small delay to reduce flickering

env.close()  # Properly close the environment
pygame.quit()  # Ensure Pygame shuts down