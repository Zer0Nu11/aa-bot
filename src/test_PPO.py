import gym
from stable_baselines3 import PPO
from aaEnv import AntiAirEnv
from matplotlib import pyplot as plt

models_dir = "models/PPO"
TIMESTEPS = 0

# env = gym.make('LunarLander-v2')  # continuous: LunarLanderContinuous-v2
env = AntiAirEnv()
env.reset()

model_path = f"{models_dir}/{TIMESTEPS}"
model = PPO.load(model_path, env=env)

episodes = 5

rwrds = []

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        rwrds.append((rewards))

plt.plot(rwrds)
plt.show()
rwrds.sort()
print(sum(rwrds)/len(rwrds))
print(min(rwrds), max(rwrds))
print(rwrds[len(rwrds)//2])