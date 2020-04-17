from produce_bouquet import ProduceBouquet


class Assembly:
    def __init__(self):
        self.bouquet_designs = None
        self.flowers_list = None

    def start_line(self, path):
        """
        Load bouquet designs and stream of flowers
        """
        with open(path, 'r') as data:
            content = data.read().split('\n\n')

        self.bouquet_designs = content[0].split('\n')
        self.flowers_list = content[1].split('\n')

    def run(self, filepath):
        self.start_line(filepath)

        producer = ProduceBouquet(self.bouquet_designs)
        producered_bouquets, in_progress = producer.run(self.flowers_list)
        return producered_bouquets, in_progress
