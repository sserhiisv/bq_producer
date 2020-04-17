import re

from copy import deepcopy
from random import choice
from collections import Counter


class ProduceBouquet:
    def __init__(self, bouquet_designs):
        self.bouquet_designs = self._agg_bouquet_design(bouquet_designs)

        # All bouquets in progres are divided by size
        self.in_progress = {
            'S': [],
            'L': []
        }
        self.finished = []      # produced bouquets

        self.flowers_count = 0

        self.flowers_not_handled = []

    def _agg_bouquet_design(self, bouquet_designs):
        """
        Init pattern structure of input bouquets designs for
        context data of bouquet progress to structure:
        {
            'AL10a15b5c30': {
                'free_space': 0,
                'made': 0,
                'max_count': 30,
                'size': 'L',
                'structure': {
                    'a': {
                        'added': 0,     # count already added
                        'count': 10,
                        'full': False
                    },
                    'b': {'added': 0, 'count': 15, 'full': False},
                    ...
                }
            },
            ...
        }
        :param bouquet_designs: list of designs for producing bouquets
        :return:
        """
        agg_bd = {}
        for design in bouquet_designs:
            flowers = re.findall(r'\d+[a-zA-Z]', design)
            total_count = int(re.findall(r'\d+$', design)[0])
            agg_bd[design] = {
                'made': 0,
                'size': design[1],
                'max_count': total_count,
                'free_space': total_count - sum([int(re.findall(r'\d+', el)[0]) for el in flowers]),
                'structure': {
                    re.findall(r'[a-zA-Z]', el)[0]: {
                        'count': int(re.findall(r'\d+', el)[0]),
                        'added': 0,
                        'full': False
                    }
                    for el in flowers
                }
            }
        return agg_bd

    def move_design_to_work(self, flower):
        # take bouquet_designs which have smallest count of finished bouquets
        to_add = {
            k: v['made']
            for k, v in self.bouquet_designs.items()
            if flower[0] in list(v['structure'].keys())
            and k[1] == flower[1]
        }

        while True:
            # take bouquet design to progress with condition
            # either design already in progress or not
            design_to_add = min(to_add, key=lambda k: to_add[k])

            if len(to_add) == 1:
                design_to_add = choice(list(
                    k for k, v in self.bouquet_designs.items()
                    if v['size'] == flower[1]
                ))
                break
            else:
                del to_add[design_to_add]

        self.in_progress[flower[1]].append({
            design_to_add: deepcopy(self.bouquet_designs[design_to_add])
        })

    def finish_bouquet(self, flower, design, bouquet, index):
        """
        check either all flower types are in bouquet, then move to bouquet finish
        """
        status = False
        not_full = [k for k, v in bouquet['structure'].items()
                      if not v['full']]
        if not not_full:
            bq = design[:2] + ''.join(
                [f'{v["added"]}{k}' for k, v in bouquet['structure'].items()])
            self.finished.append((design, bq))
            self.bouquet_designs[design]['made'] += 1
            del self.in_progress[design[1]][index]
            status = True

            print(f'Done >  design: "{design}"{" "*(15-len(design))} bouquet: "{bq}"')  # output finished bouquet

        return status

    def add_to_bouquet(self, flower, bq_inprogress):
        design = next(iter(bq_inprogress))
        bouquet = bq_inprogress[design]

        f_type = bouquet['structure'].get(flower[0])
        if not f_type and bouquet['free_space']:
            # check if we can add flower type to bouquet
            bouquet['structure'][flower[0]] = {
                'count': bouquet['free_space'],
                'added': 0,
                'full': False,
                'extra': True
            }

            f_type = bouquet['structure'].get(flower[0])

        if f_type['added'] < f_type['count']:
            bouquet['structure'][flower[0]]['added'] += 1
            if f_type['added'] == f_type['count']:
                # max count of flower type is reached -> check if bouquet is full
                bouquet['structure'][flower[0]]['full'] = True
                status = self.finish_bouquet(
                    flower, design, bouquet,
                    self.in_progress[flower[1]].index(bq_inprogress)
                )
            return True
        else:
            status = self.finish_bouquet(
                flower, design, bouquet,
                self.in_progress[flower[1]].index(bq_inprogress)
            )
            return False

    def handle_flower(self, flower):
        added = False

        for bq_inprogress in self.in_progress[flower[1]]:
            added = self.add_to_bouquet(flower, bq_inprogress)

        if not added:
            """
            there are no bouquets in progress where we can add current flower
            in this case just take new bouquet design to progress where we can 
            add current flower
            """
            self.move_design_to_work(flower)
            added = self.add_to_bouquet(flower, self.in_progress[flower[1]][-1])
        return added

    def handle_wip_bouquets(self):
        """
        Handle in progress bouquets in case when run out of flowers
        check if main flower types by design are full in bouquet
        """
        bouquets_finished = []
        bouquets_not_finished = []

        for size, struct in self.in_progress.items():
            for bq in struct:
                design = next(iter(bq))
                ready = True
                for k, v in bq[design]['structure'].items():
                    if not v.get('extra'):
                        if v.get('count') != v.get('added'):
                            ready = False

                bouquet = next(iter(bq))[:2] + ''.join([
                    f'{v["added"]}{k}' for k, v in
                    bq[design]['structure'].items()
                ])

                if ready:
                    bouquets_finished.append((design, bouquet))
                else:
                    bouquets_not_finished.append((design, bouquet))

        return bouquets_finished, bouquets_not_finished

    def run(self, flowers_list):
        for flower in flowers_list:
            self.flowers_count += 1
            if len(flower):
                if not self.in_progress[flower[1]]:
                    self.move_design_to_work(flower)

                handled = self.handle_flower(flower)
                if not handled:
                    self.flowers_not_handled.append(flower)

        bouquets_finished, bouquets_not_finished = self.handle_wip_bouquets()
        self.finished.extend(bouquets_finished)
        finished_stat = dict(Counter([x[0] for x in self.finished]))

        return finished_stat, bouquets_not_finished
