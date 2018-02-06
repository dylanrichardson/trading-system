import pickle
from argparse import ArgumentParser
from data import Data
from symbol import SymbolData
from optimal import OptimalTrades
from utility import *
from params import PARAMS


class NeuralNetwork(Data):

    def __init__(self, training, validation, testing):
        self.training = training
        self.validation = validation
        self.testing = testing
        super().__init__()


class NeuralNetworkData(Data):

    def __init__(self, symbol, options_list, days, start, end, tolerance):
        self.symbol = symbol
        self.options_list = options_list
        self.days = days
        self.start = start
        self.end = end
        self.tolerance = tolerance
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol,
            'options_list': self.options_list,
            'days': self.days,
            'start': self.start,
            'end': self.end,
            'tolerance': self.tolerance
        }


    def get_folder(self):
        return 'ann'


    def get_extension(self):
        return 'pkl'


    def read_data(self):
        try:
            with open(self.get_path(), 'rb') as fh:
                data = pickle.loads(fh.read())
                return data['in'], data['out']
        except (FileNotFoundError, EOFError) as e:
            return


    def write_data(self):
        with open(self.get_path(), 'wb') as fh:
            matrix_in, matrix_out = self.get_data()
            fh.write(pickle.dumps({'in': matrix_in, 'out': matrix_out}))


    def get_new_data(self):
        symbol_data = SymbolData(self.symbol, self.options_list).get_data()
        trades = OptimalTrades(self.symbol, self.start, self.end, self.tolerance).get_data()
        data_in, data_out = filter_incomplete(symbol_data, trades)
        data_in = add_prior_days(data_in, self.days, symbol_data)
        matrix_in = json_to_matrix(data_in)
        matrix_out = json_to_matrix(data_out)
        return matrix_in, matrix_out


def add_prior_days(data, days, full_data):
    new_data = {}
    date_list = list(enumerate(sorted(data)))
    full_data_sorted = sorted(full_data)
    full_date_list = list(enumerate(full_data_sorted))
    start_date = full_data_sorted.index(date_list[0][1])
    end_date = full_data_sorted.index(date_list[-1][1])
    for current, date in full_date_list[start_date:end_date + 1]:
        new_data[date] = {}
        for prior in range(days + 1):
            prior_data = full_data[full_date_list[current - prior][1]]
            for col in list(prior_data):
                new_data[date][str(col) + str(prior)] = prior_data[col]
    return new_data


def parse_args():
    parser = ArgumentParser(description='Load a neural network.')
    parser.add_argument('-s', '--train_symbols', type=str, nargs='+',
                        help='symbol(s) to train with')
    parser.add_argument('-y', '--train_screener', type=str,
                        help='name of Yahoo screener to train with')
    parser.add_argument('--validate_symbols', type=str, nargs='+',
                        help='symbol(s) to validate with')
    parser.add_argument('--validate_screener', type=str,
                        help='name of Yahoo screener to validate with')
    parser.add_argument('--test_symbols', type=str, nargs='+',
                        help='symbol(s) to train with')
    parser.add_argument('--test_screener', type=str,
                        help='name of Yahoo screener to train with')
    parser.add_argument('-l', '--limit', type=int, help='take the first l symbols')
    parser.add_argument('-o', '--options', type=int, nargs='+', required=True,
                        help='indices of data_options in params.py to use')
    parser.add_argument('--start', type=str, help='start date of data')
    parser.add_argument('--end', type=str, help='end date of data')
    parser.add_argument('-t', '--tolerance', type=int,
                        help='tolerance to use in optimal trades algorithm')
    parser.add_argument('-b', '--buckets', type=int,
                        help='stratify data into b buckets')
    parser.add_argument('-p', '--print', action='store_true', help='print the data')
    parser.add_argument('-v', '--verbose', action='store_true', help='log debug messages')

    args = parser.parse_args()

    PARAMS['verbose'] = args.verbose

    if not args.symbols and not args.screener:
        parser.error('At least one of --train_symbols or --train_screener is required')

    return args


def get_neural_network(symbols, screener, options_indices, limit, start, end, tolerance):
    symbols = get_symbols(symbols, screener, limit)
    options_list = get_options_list(options_indices)
    NeuralNetwork(symbols, options_list, days, start, end, tolerance)


def main():
    args = parse_args()
    data = get_neural_network(args.symbols, args.screener, args.options, args.limit,
        args.start, args.end, args.tolerance)
    if args.print:
        print(data)


if __name__ == '__main__':
    main()
