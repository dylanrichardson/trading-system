from subprocess import call
from kur.loggers import BinaryLogger
import preprocess
from analysis import get_accuracy, get_average_distance
from utility import *
from data import Data


class NeuralNetwork(Data):

    def __init__(self, training, validation, testing, evaluation, options_list, days,
                 tolerance, epochs=10, nodes=128, activation='tanh', loss='mean_squared_error'):
        self.training = training
        self.validation = validation
        self.testing = testing
        self.evaluation = evaluation
        self.options_list = options_list
        self.days = days
        self.tolerance = tolerance
        self.epochs = epochs
        self.nodes= nodes
        self.activation = activation
        self.loss = loss
        self.part_data = None
        super().__init__()

    def get_params(self):
        return {
            'training': self.training,
            'validation': self.validation,
            'testing': self.testing,
            'evaluation': self.evaluation,
            'options_list': self.options_list,
            'days': self.days,
            'tolerance': self.tolerance,
            'epochs': self.epochs
        }

    def get_folder(self):
        return 'neural'

    def get_extension(self):
        return ''

    def get_path(self):
        return super().get_path()[:-1]

    def read_data(self):
        try:
            with open(self.get_data_path(), 'rb') as fh:
                return pickle.loads(fh.read())
        except (FileNotFoundError, EOFError):
            return

    def write_data(self):
        with open(self.get_data_path(), 'wb') as fh:
            fh.write(pickle.dumps(self.get_data()))

    def get_data_path(self):
        return os.path.join(self.get_path(), 'data.pkl')

    def get_new_data(self):
        log('Training neural network...')
        self.make_model()
        call(['kur', 'train', self.get_model_path()])
        # call(['kur', 'test', self.get_model_path()])
        call(['kur', 'evaluate', self.get_model_path()])
        output = self.get_output()
        return {
            'training_loss': self.get_loss('training_loss_total'),
            'validation_loss': self.get_loss('validation_loss_total'),
            'output': output,
            'accuracy': get_accuracy(output),
            'average_distance': get_average_distance(output)
        }

    def get_loss(self, path):
        return BinaryLogger.load_column(self.get_log_path(), path)

    def get_log_path(self):
        return os.path.join(self.get_path(), 'log')

    def get_output(self):
        path = os.path.join(self.get_path(), 'output.pkl')
        with open(path, 'rb') as fh:
            return pickle.loads(fh.read())

    def get_model_path(self):
        return os.path.join(self.get_path(), 'model.yml')

    def make_model(self):
        make_path(self.get_model_path())
        with open(self.get_model_path(), 'w') as fh:
            fh.write(self.get_model())

    def get_part_data(self):
        if not self.part_data:
            self.part_data = preprocess.NeuralNetworkData(self.training, self.validation,
                            self.testing, self.evaluation, self.options_list, self.days, self.tolerance)
        return self.part_data

    def get_model(self):
        folder = self.get_path()
        part_data = self.get_part_data()
        training = part_data.get_part_path('training')
        validation = part_data.get_part_path('validation')
        testing = part_data.get_part_path('testing')
        evaluation = part_data.get_part_path('evaluation')
        return make_model(training, validation, testing, evaluation, folder,
                          self.epochs, self.nodes, self.activation, self.loss)


def make_model(training, validation, testing, evaluation, folder, epochs, nodes, activation, loss):
    with open('model.yml', 'r') as fh:
        model = fh.read()
        model = model.replace('TRAINING', training)
        model = model.replace('VALIDATION', validation)
        model = model.replace('TESTING', testing)
        model = model.replace('EVALUATION', evaluation)
        model = model.replace('WEIGHTS', os.path.join(folder, 'weights'))
        model = model.replace('LOG', os.path.join(folder, 'log'))
        model = model.replace('OUTPUT', os.path.join(folder, 'output.pkl'))
        model = model.replace('EPOCHS', str(epochs))
        model = model.replace('NODES', str(nodes))
        model = model.replace('ACTIVATION', activation)
        model = model.replace('LOSS', loss)
        return model


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
    data = NeuralNetwork(*args.parts, args.options_list, args.days, args.tolerance,
                         args.epochs, args.nodes, args.activation, args.loss).get_data()
    log(data, force=args.print)
    if args.path:
        log(data.get_path(), force=args.print)


if __name__ == '__main__':
    main()
