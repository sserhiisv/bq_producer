import argparse

from pprint import pprint

from assembly import Assembly


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--path', type=str, required=True, help='path to sample data')


def main(filepath):
    assembly = Assembly()
    producered_bouquets, bouquets_not_finished = assembly.run(filepath)

    print('-' * 20)
    print(f'Run out of flowers. But there are {len(bouquets_not_finished)} not finished bouquets:')
    pprint(bouquets_not_finished)

    print('-' * 20)
    print(f'Finished bouquets:')
    pprint(producered_bouquets)


if __name__ == '__main__':
    args = parser.parse_args()
    filepath = args.path
    print('Path to input data: ', filepath)
    main(filepath)
