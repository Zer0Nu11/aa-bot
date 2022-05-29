from aaEnv import AntiAirEnv
from stable_baselines3.common.env_checker import check_env

env = AntiAirEnv()

check_env(env)