from argparse import ArgumentParser
from subprocess import call


PROGRAMS = ['graph', 'neural', 'optimal', 'preprocess', 'screener', 'symbol', 'tests']


def main():
    parser = ArgumentParser(description='Automated trading system using machine learning.')
    parser.add_argument('program', type=str, choices=PROGRAMS)
    args, sub_args = parser.parse_known_args()
    call(['python', args.program + '.py'] + sub_args)


if __name__ == '__main__':
    main()