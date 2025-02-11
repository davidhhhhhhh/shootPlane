from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from plane_battle_env import PlaneBattleEnv

# Create vectorized environment
env = make_vec_env(PlaneBattleEnv, n_envs=1)

# Define and train DQN agent
model = DQN("MlpPolicy", env, verbose=1, learning_rate=0.0005, buffer_size=10000)
model.learn(total_timesteps=50000)

# Save the trained model
model.save("plane_battle_dqn")

print("Training complete. Model saved as 'plane_battle_dqn'.")