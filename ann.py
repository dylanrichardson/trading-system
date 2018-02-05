import pickle
from symbol import SymbolData
from optimal import OptimalTrades
from utility import *
from params import PARAMS


class NeuralNetwork(Data):
    pass # TODO


class NeuralNetworkData(Data):

    def __init__(self, symbol, options_list, days, start, end, tolerance, smoothed):
        self.symbol = symbol
        self.options_list = options_list
        self.days = days
        self.start = start
        self.end = end
        self.tolerance = tolerance
        self.smoothed = smoothed
        super().__init__()


    def get_params(self):
        return {
            'symbol': self.symbol,
            'options_list': self.options_list,
            'days': self.days,
            'start': self.start,
            'end': self.end,
            'tolerance': self.tolerance,
            'smoothed': self.smoothed
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
        trades = OptimalTrades(self.symbol, self.start, self.end, self.tolerance, self.smoothed).get_data()
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
