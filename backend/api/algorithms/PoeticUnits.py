from anytree import Node

class PoeticUnits:
    def __init__(self, binary_string):
        self.binary_string = binary_string.strip()

        self.audio_units = self.defines_audio_units()

        self.tafeelat = self.defines_tafeelat()

    @staticmethod
    def defines_audio_units():
        return [
            # 0
            {'name': 'sabab_khafif_pattern',
             'pattern': '10'
             },

            # 1
            {'name': 'sabab_thaqil_pattern',
             'pattern': '11'
             },

            # 2
            {'name': 'watad_majmoua_pattern',
             'pattern': '110'
             },

            # 3
            {'name': 'watad_mafrooq_pattern',
             'pattern': '101'
             }
        ]

    def defines_tafeelat(self):
        return [
            # 0
            {
                # Sabab Khafif + Watad Majmoua (10 + 110)
                'pattern': '10110',
                'word': 'فاعلن',
                'main': None,
                'units': [self.audio_units[0], self.audio_units[2]]
            },

            # 1
            {
                # Watad Majmoua + Sabab Khafif (110 + 10)
                'pattern': '11010',
                'word': 'فعولن',
                'main': None,
                'units': [self.audio_units[2], self.audio_units[0]]
            },

            # 2
            {
                # Watad Majmoua + Two Sabab Khafif (110 + 10 + 10)
                'pattern': '1101010',
                'word': 'مفاعيلن',
                'main': None,
                'units': [self.audio_units[2], self.audio_units[0], self.audio_units[0]]
            },

            # 3
            {
                # Watad Majmoua + Sabab Thaqil + Sabab Khafif (110 + 11 + 10)
                'pattern': '1101110',
                'word': 'مفاعلتن',
                'main': None,
                'units': [self.audio_units[2], self.audio_units[1], self.audio_units[0]]
            },

            # 4
            {
                # Two Sabab Khafif + Watad Majmoua (10 + 10 + 110)
                'pattern': '1010110',
                'word': 'مستفعلن',
                'main': None,
                'units': [self.audio_units[0], self.audio_units[0], self.audio_units[2]]
            },

            # 5
            {
                # Sabab Thaqil + Sabab Khafif + Watad Majmoua (11 + 10 + 110)
                'pattern': '1110110',
                'word': 'متفاعلن',
                'main': None,
                'units': [self.audio_units[1], self.audio_units[0], self.audio_units[2]]
            },

            # 6
            {
                # Sabab Khafif + Watad Majmoua + Sabab Khafif (10 + 110 + 10)
                'pattern': '1011010',
                'word': 'فاعلاتن',
                'main': None,
                'units': [self.audio_units[0], self.audio_units[2], self.audio_units[0]]
            },

            # 7
            {
                # Two Sabab Khafif + Watad Mafrooq (10 + 10 + 101)
                'pattern': '1010101',
                'word': 'مفعولات',
                'main': None,
                'units': [self.audio_units[0], self.audio_units[0], self.audio_units[3]]
            },

            # 8
            {
                # Sabab Khafif + Watad Majmoua + Sabab Khafif (10 + 101 + 10)
                'pattern': '1010110',
                'word': 'مستفعلن',
                'main': None,
                'units': [self.audio_units[0], self.audio_units[3], self.audio_units[0]]
            },

            # 9
            {
                # Watad Mafrooq + Two Sabab Khafif (101 + 10 + 10)
                'pattern': '1011010',
                'word': 'فاعلاتن',
                'main': None,
                'units': [self.audio_units[3], self.audio_units[0], self.audio_units[0]]
            }
        ]

    def dfs(self, node, path=None, paths=None):
        if path is None:
            path = []
        if paths is None:
            paths = []

        path = path + [node.name]

        if not node.children:
            paths.append(path)
        else:
            for child in node.children:
                self.dfs(child, path, paths)

        return paths

    def compare(self, see):
        comparisons = {}

        for root in see:
            for pattern in self.dfs(root):
                pattern_tuple = tuple(
                    (t['pattern'], t['word'], t['change'], t['main']) for t in pattern)

                index = 0
                results = []
                for t in pattern:
                    result = []

                    length_t = len(t['pattern'])

                    t_list = list(t['pattern'])
                    binary_list = list(self.binary_string)[index: index + length_t]

                    if length_t > len(binary_list):
                        length_t = len(binary_list)

                    for i in range(length_t):
                        if t_list[i] == binary_list[i]:
                            result.append(t_list[i])  # Keep the matching element
                        else:
                            result.append('#')  # Replace mismatch with '#'

                    result.extend(['#' for _ in range(len(t_list) - len(binary_list))])

                    index += length_t

                    results.append(result)

                comparisons[pattern_tuple] = results

        return comparisons

    def result(self, comparisons):
        results = {}

        for key, value in comparisons.items():
            error = 0
            for t in value:
                for match in t:
                    if match == '#':
                        error += 1

            total_length = sum(len(inner_list) for inner_list in value)

            if total_length < len(self.binary_string):
                error += len(self.binary_string) - total_length

            if total_length > 0:
                percentage = (total_length - error) / total_length * 100
            else:
                percentage = 0

            results[key] = percentage

        return results

    def taweel_see(self):

        self.tafeelat[1]['change'] = None
        hashow = [
            self.tafeelat[1],
            {
                'pattern': '1101',
                'word': 'فعول',
                'change': 'قبض',
                'main': self.tafeelat[1]['word'],
                'units': self.tafeelat[1]['units'],
            },
        ]

        self.tafeelat[2]['change'] = None
        arood_darb = [
            self.tafeelat[2],
            {
                'pattern': '110110',
                'word': 'مفاعلن',
                'change': 'قبض',
                'main': self.tafeelat[2]['word'],
                'units': self.tafeelat[2]['units'],
            },
            {
                'pattern': '11010',
                'word': 'مفاعل',
                'change': 'حذف',
                'main': self.tafeelat[2]['word'],
                'units': self.tafeelat[2]['units'],
            },
        ]

        roots = []
        nodes = []  # To keep track of all created nodes

        for t1 in hashow:
            node_t1 = Node(t1)  # Create the first level node
            roots.append(node_t1)
            nodes.append(node_t1)

            for t2 in arood_darb:
                node_t2 = Node(t2, parent=node_t1)  # Create the second level node
                nodes.append(node_t2)

                for t3 in hashow:
                    node_t3 = Node(t3, parent=node_t2)  # Create the third level node
                    nodes.append(node_t3)

                    for t4 in arood_darb:
                        node_t4 = Node(t4, parent=node_t3)  # Create the fourth level node
                        nodes.append(node_t4)

        # for root in roots:
        #     for path in self.dfs(root):
        #         for t in path:
        #             print(t['word'], end=" ")
        #         print()

        # # Render the tree
        # for root in roots:
        #     for pre, fill, node in RenderTree(root):
        #         print(f"{pre}{node.name['pattern']}")

        return roots

    @staticmethod
    def get_match(results):
        best_match = max(results.values())
        key = next((k for k, v in results.items() if v == best_match), None)
        return [key, best_match]

    @staticmethod
    def print_whole_results(results):
        for key, percentage in results.items():
            print(f'{key}: {percentage:.2f}%')
