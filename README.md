# AA-bot

Simple Anti-Air game with RL-agent


![alt text](src/assets/myAAgun.jpg)

![alt text](src/assets/AAgun.GIF)

## Requirements
```
pip install -r requirements.txt
```

## Training
set variables TIMESTEPS, EPOCHS in src/train_PPO.py
```
python3 src/train_PPO.py
```
see training results in tensorboard
```
tensorboard --logdir=logs
```

## Usage
Play game:
```
python3 src/play.py
```

Test agent:
set variable TIMESTEPS in src/test_PPO.py
```
python3 src/test_PPO.py
```

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- Documentation
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.

------------

