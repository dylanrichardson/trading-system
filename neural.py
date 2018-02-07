from argparse import ArgumentParser
from subprocess import call
from kur.loggers import BinaryLogger
import pickle
import preprocess
from utility import *
from data import Data


class NeuralNetwork(Data):

    def __init__(self, training, validation, testing, evaluation,
                 options_list, days, tolerance, epochs):
        self.training = training
        self.validation = validation
        self.testing = testing
        self.evaluation = evaluation
        self.options_list = options_list
        self.days = days
        self.tolerance = tolerance
        self.epochs = epochs
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
        return {
            'training_loss': self.get_loss('training_loss_total'),
            'validation_loss': self.get_loss('validation_loss_total'),
            'output': self.get_output()
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
        return make_model(training, validation, testing, evaluation, folder, self.epochs)


def make_model(training, validation, testing, evaluation, folder, epochs):
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
        return model


def parse_args():
    parser = ArgumentParser(description='Create a neural network.')
    parser.add_argument('-e', '--epochs', default=50,
                        help='number of epochs to train for')
    preprocess.add_parser_args(parser)
    args = parser.parse_args()
    set_verbosity(args.verbose)
    preprocess.handle_args(args, parser)
    return args


def main():
    args = parse_args()
    data = NeuralNetwork(*args.parts, args.options_list, args.days, args.tolerance, args.epochs).get_data()
    log(data, force=args.print)


if __name__ == '__main__':
    main()
