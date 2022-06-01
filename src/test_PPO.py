import gym
from sb3_contrib import RecurrentPPO
from aaEnv import AntiAirEnv
from matplotlib import pyplot as plt

models_dir = "models/PPO"
TIMESTEPS = 0

# env = gym.make('LunarLander-v2')  # continuous: LunarLanderContinuous-v2
env = AntiAirEnv()
env.reset()

model_path = f"{models_dir}/{TIMESTEPS}"
model = RecurrentPPO.load(model_path, env=env)

episodes = 10

rwrds = []

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        rwrds.append((rewards))

print("================")
print(sum(rwrds)/len(rwrds))
print(min(rwrds), max(rwrds))

plt.plot(rwrds)
plt.show()
print(rwrds)
rwrds.sort()
print("================")
print(rwrds[len(rwrds)//2])
print(rwrds)