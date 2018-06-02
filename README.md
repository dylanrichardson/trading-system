# trading-system
Automatic trading system using machine learning

## Setup


### Clone

```
git clone git@github.com:drich14/trading-system.git
```


### PyEnv (optional)

Activate
```
pyenv activate venv
```

Deactivate
```
pyenv deactivate
```


### Install dependencies

```
pip install -r requirements.txt
```


### Run tests

```
python tests.py
```


## Programs


### graph.py

usage: graph.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER]
                [--percentages PERCENTAGES [PERCENTAGES ...]]
                [--training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]]
                [--training_screener TRAINING_SCREENER]
                [--validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]]
                [--validation_screener VALIDATION_SCREENER]
                [--evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]]
                [--evaluation_screener EVALUATION_SCREENER] [-l LIMIT]
                [--start START] [--end END] -o OPTIONS [OPTIONS ...]
                [-t TOLERANCE] [-d DAYS] [-e EPOCHS] [-n NODES] [-a {tanh}]
                [--loss {mean_squared_error}] [-p] [-v] [--path]
                {data,optimal,neural}


### neural.py

```
usage: neural.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER]
                 [--percentages PERCENTAGES [PERCENTAGES ...]]
                 [--training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]]
                 [--training_screener TRAINING_SCREENER]
                 [--validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]]
                 [--validation_screener VALIDATION_SCREENER]
                 [--evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]]
                 [--evaluation_screener EVALUATION_SCREENER] [-l LIMIT]
                 [--start START] [--end END] -o OPTIONS [OPTIONS ...]
                 [-t TOLERANCE] [-d DAYS] [-e EPOCHS] [-n NODES] [-a{tanh}]
                 [--loss {mean_squared_error}] [-p] [-v] [--path]
```


### optimal.py

```
usage: optimal.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER] [-l LIMIT]
                  [--start START] [--end END] [-t TOLERANCE] [-p] [-v]
                  [--path]
```


### preprocess.py

```
usage: preprocess.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER]
                     [--percentages PERCENTAGES [PERCENTAGES ...]]
                     [--training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]]
                     [--training_screener TRAINING_SCREENER]
                     [--validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]]
                     [--validation_screener VALIDATION_SCREENER]
                     [--evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]]
                     [--evaluation_screener EVALUATION_SCREENER] [-lLIMIT]
                     [--start START] [--end END] -o OPTIONS [OPTIONS...]
                     [-t TOLERANCE] [-d DAYS] [-p] [-v] [--path]
```


### screener.py

```
usage: screener.py [-h] [-l LIMIT] [-p] [-v] [--path] screener
```


### symbol.py

```
usage: symbol.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER] [-l LIMIT]
                 [--start START] [--end END] -o OPTIONS [OPTIONS ...] [-r]
                 [-p] [-v] [--path]
```

