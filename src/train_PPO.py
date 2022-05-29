import gym
from stable_baselines3 import PPO
import os
from aaEnv import AntiAirEnv

TIMESTEPS = 10000 # steps per save
EPOCHS = 5

models_dir = "models/PPO"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)
if not os.path.exists(logdir):
    os.makedirs(logdir)

# env = gym.make('LunarLander-v2')
env = AntiAirEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)

for i in range(EPOCHS):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")