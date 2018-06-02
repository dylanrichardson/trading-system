import logging
from subprocess import call
from kur.loggers import BinaryLogger
from kur import Kurfile
from kur.engine import JinjaEngine
from kur.utils import DisableLogging

import preprocess
from analysis import get_accuracy, get_average_distance
from utility import *
from data import Data


class NeuralNetwork(Data):

    def __init__(self, **params):
        self.training = params['training']
        self.validation = params['validation']
        self.evaluation = params['evaluation']
        self.options_list = params['options_list']
        self.days = params.get('days', 0)
        self.tolerance = params.get('tolerance', 0.01)
        self.epochs = params.get('epochs', 10)
        self.nodes = params.get('nodes', 128)
        self.activation = params.get('activation', 'tanh')
        self.loss = params.get('loss', 'mean_squared_error')
        self.part_data = None
        super().__init__(**params)

    def get_folder(self):
        return 'neural'

    def read_data(self):
        return read_pickle(self.get_data_path())

    def write_data(self):
        write_pickle(self.get_data_path(), self.get_data())

    def get_data_path(self):
        return self.get_path('data.pkl')

    def get_model_path(self):
        return self.get_path('model.yml')

    def get_new_data(self):
        log('Training neural network...')
        self.make_model()
        return train_neural_network(self.get_path())

    def make_model(self):
        make_path(self.get_model_path())
        with open(self.get_model_path(), 'w') as fh:
            fh.write(self.get_model())

    def get_part_data(self):
        if not self.part_data:
            self.part_data = preprocess.NeuralNetworkData(training=self.training, validation=self.validation,
                                                          evaluation=self.evaluation, options_list=self.options_list,
                                                          days=self.days, tolerance=self.tolerance)
        return self.part_data

    def get_model(self):
        folder = self.get_path()
        part_data = self.get_part_data()
        training = part_data.get_part_path('training')
        validation = part_data.get_part_path('validation')
        evaluation = part_data.get_part_path('evaluation')
        return make_model(training, validation, evaluation, folder, self.epochs,
                          self.nodes, self.activation, self.loss, part_data.get_shape())

    def predict(self, data):
        kurfile = Kurfile(self.get_model_path(), JinjaEngine())
        kurfile.parse()
        model = kurfile.get_model()
        with DisableLogging(logging.WARNING):
            model.backend.compile(model)
        model.restore(self.get_path('weights'))
        pdf, metrics = model.backend.evaluate(model, data={'in': np.array([data])})
        prediction = pdf['out'][0][0]
        return prediction


def make_model(training, validation, evaluation, folder, epochs, nodes, activation, loss, shape):
    with open('model.yml', 'r') as fh:
        model = fh.read()
        model = model.replace('TRAINING', training)
        model = model.replace('VALIDATION', validation)
        model = model.replace('EVALUATION', evaluation)
        model = model.replace('WEIGHTS', os.path.join(folder, 'weights'))
        model = model.replace('LOG', os.path.join(folder, 'log'))
        model = model.replace('OUTPUT', os.path.join(folder, 'output.pkl'))
        model = model.replace('EPOCHS', str(epochs))
        model = model.replace('NODES', str(nodes))
        model = model.replace('ACTIVATION', activation)
        model = model.replace('LOSS', loss)
        model = model.replace('SHAPE', str(shape))
        return model


def train_neural_network(folder):
    model_path = os.path.join(folder, 'model.yml')
    log_path = os.path.join(folder, 'log')
    output_path = os.path.join(folder, 'output.pkl')
    std_out = None if PARAMS['verbose'] else 'out'
    call(['kur', 'train', model_path], stdout=stdout)
    call(['kur', 'evaluate', model_path], stdout=stdout)
    output = read_pickle(output_path)
    return {
        'training_loss': get_loss(log_path, 'training_loss_total'),
        'validation_loss': get_loss(log_path, 'validation_loss_total'),
        'output': output,
        'accuracy': get_accuracy(output),
        'average_distance': get_average_distance(output)
    }


def get_loss(log_path, path):
    return BinaryLogger.load_column(log_path, path)


def add_args(parser):
    preprocess.add_args(parser)
    parser.add_argument('-e', '--epochs', type=int, default=50,
                        help='number of epochs to train for')
    parser.add_argument('-n', '--nodes', type=int, default=128,
                        help='number of nodes per layer')
    parser.add_argument('-a', '--activation', type=str, default='tanh', choices=['tanh'],
                        help='type of activation layer')
    parser.add_argument('--loss', type=str, default='mean_squared_error',
                        help='type of loss function', choices=['mean_squared_error'])


def handle_args(args, parser):
    preprocess.handle_args(args, parser)


def main():
    args = parse_args('Create a neural network.', add_args, handle_args)
    data = NeuralNetwork(**args.parts, options_list=args.options_list, days=args.days,
                         tolerance=args.tolerance, epochs=args.epochs, nodes=args.nodes,
                         activation=args.activation, loss=args.loss)
    log(data.get_data(), force=args.print)
    if args.path:
        log(data.get_path(), force=args.print)


if __name__ == '__main__':
    main()
