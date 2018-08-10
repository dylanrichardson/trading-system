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

### Save new dependencies

```
pip freeze > requirements.txt
```

### Run tests

```
python tests.py
```

## Programs

### graph.py

```
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

Load a graph.

positional arguments:
  {data,optimal,neural}
                        data to graph

optional arguments:
  -h, --help            show this help message and exit
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbol(s)
  -y SCREENER, --screener SCREENER
                        name of Yahoo screener
  --percentages PERCENTAGES [PERCENTAGES ...]
                        relative size of each data part
  --training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]
                        symbol(s) to train with
  --training_screener TRAINING_SCREENER
                        name of Yahoo screener to train with
  --validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]
                        symbol(s) to validate with
  --validation_screener VALIDATION_SCREENER
                        name of Yahoo screener to validate with
  --evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]
                        symbol(s) to evaluate with
  --evaluation_screener EVALUATION_SCREENER
                        name of Yahoo screener to evaluate with
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  --start START         start date of data
  --end END             end date of data
  -o OPTIONS [OPTIONS ...], --options OPTIONS [OPTIONS ...]
                        indices of data_options in params.py to use
  -t TOLERANCE, --tolerance TOLERANCE
                        tolerance to use in optimal trades algorithm
  -d DAYS, --days DAYS  number of prior days of data to use as input per day
  -e EPOCHS, --epochs EPOCHS
                        number of epochs to train for
  -n NODES, --nodes NODES
                        number of nodes per layer
  -a {tanh}, --activation {tanh}
                        type of activation layer
  --loss {mean_squared_error}
                        type of loss function
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

Example

```
python graph.py data -s AAPL -o sma --start 2018-01-01 --end 2018-02-01 -p
```

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
                 [-t TOLERANCE] [-d DAYS] [-e EPOCHS] [-n NODES] [-a {tanh}]
                 [--loss {mean_squared_error}] [-p] [-v] [--path]

Create a neural network.

optional arguments:
  -h, --help            show this help message and exit
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbol(s)
  -y SCREENER, --screener SCREENER
                        name of Yahoo screener
  --percentages PERCENTAGES [PERCENTAGES ...]
                        relative size of each data part
  --training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]
                        symbol(s) to train with
  --training_screener TRAINING_SCREENER
                        name of Yahoo screener to train with
  --validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]
                        symbol(s) to validate with
  --validation_screener VALIDATION_SCREENER
                        name of Yahoo screener to validate with
  --evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]
                        symbol(s) to evaluate with
  --evaluation_screener EVALUATION_SCREENER
                        name of Yahoo screener to evaluate with
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  --start START         start date of data
  --end END             end date of data
  -o OPTIONS [OPTIONS ...], --options OPTIONS [OPTIONS ...]
                        indices of data_options in params.py to use
  -t TOLERANCE, --tolerance TOLERANCE
                        tolerance to use in optimal trades algorithm
  -d DAYS, --days DAYS  number of prior days of data to use as input per day
  -e EPOCHS, --epochs EPOCHS
                        number of epochs to train for
  -n NODES, --nodes NODES
                        number of nodes per layer
  -a {tanh}, --activation {tanh}
                        type of activation layer
  --loss {mean_squared_error}
                        type of loss function
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

Example

```
python neural.py -s AAPL -o sma --start 2018-01-01 --end 2018-02-01
```

### optimal.py

```
usage: optimal.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER] [-l LIMIT]
                  [--start START] [--end END] [-t TOLERANCE] [-p] [-v]
                  [--path]

Load optimal trades.

optional arguments:
  -h, --help            show this help message and exit
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbol(s)
  -y SCREENER, --screener SCREENER
                        name of Yahoo screener
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  --start START         start date of data
  --end END             end date of data
  -t TOLERANCE, --tolerance TOLERANCE
                        tolerance to use in algorithm
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

Example

```
python optimal.py -s AAPL
```

### preprocess.py

Usage

```
usage: preprocess.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER]
                     [--percentages PERCENTAGES [PERCENTAGES ...]]
                     [--training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]]
                     [--training_screener TRAINING_SCREENER]
                     [--validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]]
                     [--validation_screener VALIDATION_SCREENER]
                     [--evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]]
                     [--evaluation_screener EVALUATION_SCREENER] [-l LIMIT]
                     [--start START] [--end END] -o OPTIONS [OPTIONS ...]
                     [-t TOLERANCE] [-d DAYS] [-p] [-v] [--path]

Preprocess neural network data.

optional arguments:
  -h, --help            show this help message and exit
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbol(s)
  -y SCREENER, --screener SCREENER
                        name of Yahoo screener
  --percentages PERCENTAGES [PERCENTAGES ...]
                        relative size of each data part
  --training_symbols TRAINING_SYMBOLS [TRAINING_SYMBOLS ...]
                        symbol(s) to train with
  --training_screener TRAINING_SCREENER
                        name of Yahoo screener to train with
  --validation_symbols VALIDATION_SYMBOLS [VALIDATION_SYMBOLS ...]
                        symbol(s) to validate with
  --validation_screener VALIDATION_SCREENER
                        name of Yahoo screener to validate with
  --evaluation_symbols EVALUATION_SYMBOLS [EVALUATION_SYMBOLS ...]
                        symbol(s) to evaluate with
  --evaluation_screener EVALUATION_SCREENER
                        name of Yahoo screener to evaluate with
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  --start START         start date of data
  --end END             end date of data
  -o OPTIONS [OPTIONS ...], --options OPTIONS [OPTIONS ...]
                        indices of data_options in params.py to use
  -t TOLERANCE, --tolerance TOLERANCE
                        tolerance to use in optimal trades algorithm
  -d DAYS, --days DAYS  number of prior days of data to use as input per day
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

Example

```
python preprocess.py -s AAPL -o sma --start 2018-01-01 --end 2018-02-01
```

### screener.py

Usage

```
usage: screener.py [-h] [-l LIMIT] [-p] [-v] [--path] screener

Screen for symbols.

positional arguments:
  screener              name of Yahoo screener

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

Example

```
python screener.py -l 10
```

### symbol.py

Usage

```
usage: symbol.py [-h] [-s SYMBOLS [SYMBOLS ...]] [-y SCREENER] [-l LIMIT]
                 [--start START] [--end END] -o OPTIONS [OPTIONS ...] [-r]
                 [-p] [-v] [--path]

Load symbol data.

optional arguments:
  -h, --help            show this help message and exit
  -s SYMBOLS [SYMBOLS ...], --symbols SYMBOLS [SYMBOLS ...]
                        symbol(s)
  -y SCREENER, --screener SCREENER
                        name of Yahoo screener
  -l LIMIT, --limit LIMIT
                        take the first l symbols
  --start START         start date of data
  --end END             end date of data
  -o OPTIONS [OPTIONS ...], --options OPTIONS [OPTIONS ...]
                        indices of data_options in params.py
  -r, --refresh         refresh the data
  -p, --print           print the data
  -v, --verbose         enable logging
  --path                print the data path
```

| Indicators                                     |
| ---------------------------------------------- |
| daily()                                        |
| daily_adj()                                    |
| sma(period=30)                                 |
| ema(period=20)                                 |
| macd(fast=12, slow=26, signal=9)               |
| stoch(fastk=5, slowk=3, slowd=3, kma=0, dma=0) |
| rsi(period=14)                                 |
| adx(period=14)                                 |
| cci(period=14)                                 |
| aroon(period=14)                               |
| bbands(period=14, ndev=2, ma=0)                |
| ad()                                           |
| obv()                                          |

Example

```
python symbol.py -s AAPL -o sma
```
