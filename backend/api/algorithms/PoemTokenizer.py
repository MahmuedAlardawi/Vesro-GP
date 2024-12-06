import re
from itertools import product

class PoemTokenizer:
    def __init__(self, poem):
        self.poem = poem.strip()
        self.tokens = self.define_tokens()

        self.poem_list = self.define_poem_list()

        self.normalized_poem = self.define_normalized_poem()

        self.normalized_poem_combinations = self.define_normalized_poem_combinations()

        self.tokenized_poem = self.define_tokenized_poem()

    @staticmethod
    def define_tokens():
        return {
            'letters_pattern': r'[ء-ي]',
            'all_harakat_pattern': r"[ًٌٍَُِّْ]",
            'harakat_pattern': r'[َُِ]',
            'tanween_pattern': r'[ًٌٍ]',
            'qamariya_letters': r'[أبجحخعغفقكمهوي]',
            'shamseya_letters': r'[تثدذرزسشصضطظللن]',
            'madd_pattern': r"[اويى]",
            'asmaa_eshara_pattern': r'(هذا|هذه|هذان|هذين|هؤلاء|ذلك|أولئك|أولو|أولاء|أولات|ذليكما|ذلكم|هكذا|ههنا|هذي)',
            'special_cases_pattern': r'(مائة|مائتان|الله|الرحمن|إله|لكن|طه|إبرهيم|إسمعيل|يس|طاوس|داود)',
            'madd_to_haraka': {
            'ا': 'َ',  # Fatha
            'ى': 'َ',  # Fatha
            'و': 'ُ',  # Damma
            'ي': 'ِ'  # Kasra
            },
            'haraka_to_madd': {
                'َ': 'ا',  # Fatha
                'ُ': 'و',  # Damma
                'ِ': 'ي'  # Kasra
            }
        }

    def define_poem_list(self):
        poem_list = self.poem.split()

        for i in range(len(poem_list)):
            cleaned_word = re.sub(r'[^\u0621-\u064A\u064B-\u0652]', '', poem_list[i])

            word = re.sub(r'[^\u0621-\u064A]', '', cleaned_word)
            if (
                    re.match(self.tokens['asmaa_eshara_pattern'], word)
                    or re.match(self.tokens['special_cases_pattern'], word)
            ):
                cleaned_word = self.apply_special(word)

            letter_list = []
            j = 0
            while j < len(cleaned_word):
                if re.match(self.tokens['letters_pattern'], cleaned_word[j]):

                    if (j < len(cleaned_word) - 4 and re.match('ا', cleaned_word[j])
                            and re.match('ل', cleaned_word[j + 1])
                            and re.match(self.tokens['shamseya_letters'], cleaned_word[j + 2])
                            and re.match(self.tokens['harakat_pattern'], cleaned_word[j + 3])):
                        letter_list.append(cleaned_word[j] + 'ْ' + cleaned_word[j + 1] + 'ْ' +
                                           cleaned_word[j + 2] + 'ّ' + cleaned_word[j + 3])
                        j += 4

                    if (j < len(cleaned_word) - 2 and
                            not re.match(self.tokens['letters_pattern'], cleaned_word[j + 1])):
                        if j + 2 < len(cleaned_word) and re.match('ّ', cleaned_word[j + 2]):
                            letter_list.append(cleaned_word[j] + cleaned_word[j + 2] + cleaned_word[j + 1])
                            j += 3

                    if j < len(cleaned_word) - 1:
                        if re.match('ّ', cleaned_word[j + 1]):
                            if (re.match(self.tokens['madd_pattern'], cleaned_word[j + 2])
                                    and j < len(cleaned_word) - 3
                                    and re.match('ً', cleaned_word[j + 3])):
                                letter_list.append(cleaned_word[j] + 'ّ' + 'ً' + 'ا')
                                j += 3

                            elif re.match(self.tokens['madd_pattern'], cleaned_word[j + 2]):
                                letter_list.append(cleaned_word[j] + cleaned_word[j + 1] +
                                                   self.tokens['madd_to_haraka'][cleaned_word[j + 2]])

                            else:
                                letter_list.append(cleaned_word[j] + cleaned_word[j + 1] + cleaned_word[j + 2])

                        elif re.match(self.tokens['madd_pattern'], cleaned_word[j + 1]):
                            if (i == len(poem_list) - 1 and re.match('ا', cleaned_word[j + 1]) and
                                    re.match('ً', cleaned_word[j + 2])):
                                letter_list.append(cleaned_word[j] + 'ً' + cleaned_word[j + 1])
                                j += 1

                            else:
                                letter_list.append(cleaned_word[j] + self.tokens['madd_to_haraka'][cleaned_word[j + 1]])

                        elif re.match(self.tokens['all_harakat_pattern'], cleaned_word[j + 1]):
                            letter_list.append(cleaned_word[j] + cleaned_word[j + 1])

                        else:
                            letter_list.append(cleaned_word[j] + 'ْ')

                    elif j == len(cleaned_word) - 1 and re.match(self.tokens['letters_pattern'], cleaned_word[j]):
                        letter_list.append(cleaned_word[j] + 'ْ')
                j += 1

            poem_list[i] = ''.join(letter_list)
        return poem_list

    def define_normalized_poem(self):
        normalized_poem = []
        for i in range(len(self.poem_list)):
            normalized_poem.append([])

            j = 0
            while j < len(self.poem_list[i]) - 1:
                if j == 0:
                    v = self.normalize_1(i, j, normalized_poem)
                    normalized_poem[i].extend(v[0])
                    j += v[1]

                elif j <= len(self.poem_list[i]) - 3:
                    v = self.normalize_2(i, j)
                    normalized_poem[i].extend(v[0])
                    j += v[1]

                else:
                    v = self.normalize_3(i, j, normalized_poem)
                    if v == 'delete':
                        normalized_poem[i] = normalized_poem[i][:-2]
                        break

                    else:
                        normalized_poem[i].extend(v[0])
                        j += v[1]

        return self.create_variations(normalized_poem)

    def define_normalized_poem_combinations(self):
        # Extract the lists of variations in the correct order based on the index
        variations_lists = [self.normalized_poem[i] for i in sorted(self.normalized_poem.keys())]

        # Use itertools.product to find all possible combinations
        all_combinations = list(product(*variations_lists))

        # Format each combination as a sentence
        all_sentences = [' '.join(combo) for combo in all_combinations]

        return all_sentences

    def define_tokenized_poem(self):
        binary_list = {}

        for sentence in self.normalized_poem_combinations:
            word = ''

            for diacritics in sentence:
                if re.match(self.tokens['harakat_pattern'], diacritics):
                    word += '1'
                elif re.match('ْ', diacritics):
                    word += '0'

            binary_list[sentence] = word

        return binary_list

    def create_variations(self, word_list):
        def collect_word(word):
            return ''.join(word)

        words_dict = {}

        for i in range(len(word_list)):
            words_dict[i] = [collect_word(word_list[i])]

            if (re.match('ْ', word_list[i][-1]) and re.match(self.tokens['madd_pattern'], word_list[i][-2])
                    and re.match(self.tokens['madd_to_haraka'][word_list[i][-2]], word_list[i][-3])):

                words_dict[i].append(collect_word(word_list[i][:-2]))
                if i == len(word_list) - 1:
                    words_dict[i].pop(1)

            elif re.match(self.tokens['harakat_pattern'], word_list[i][-1]):
                if i < len(word_list) - 1 and not re.match('ْ', word_list[i + 1][1]):
                    words_dict[i].append(collect_word(word_list[i]) +
                                         self.tokens['haraka_to_madd'][word_list[i][-1]] + 'ْ')
                if i == len(word_list) - 1:
                    words_dict[i].pop(0)


        return words_dict

    def normalize_1(self, i, j, normalized_poem):
        if i == 0 or re.match('ْ', normalized_poem[i - 1][-1]):
            if self.is_al(i, j):
                return self.apply_al(i, j, 'first')
            else:
                return self.normalize_2(i, j)
        else:
            if self.is_al(i, j):
                return self.apply_al(i, j, 'none')
            elif re.match('ا', self.poem_list[i][j]):
                return [[], 2]
            else:
                return self.normalize_2(i, j)

    def normalize_2(self, i, j):
        if j < len(self.poem[i]) - 2 and 1 < j < 3 and self.is_al(i, j) and not re.match(self.tokens['harakat_pattern'], self.poem_list[i][j + 2]):
            return self.apply_al(i, j, 'none')

        elif j + 2 < len(self.poem_list[i]) and re.match('ّ', self.poem_list[i][j + 2]):
            output = [self.poem_list[i][j], 'ْ', self.poem_list[i][j], self.poem_list[i][j + 1]]
            return [output, 3]

        elif re.match(self.tokens['harakat_pattern'], self.poem_list[i][j + 1]):
            return [[self.poem_list[i][j], self.poem_list[i][j + 1]], 2]

        elif re.match(self.tokens['tanween_pattern'], self.poem_list[i][j + 1]):
            output = [self.poem_list[i][j]]

            if re.match('ً', self.poem_list[i][j + 1]):
                output.append('َ')

            elif re.match('ٌ', self.poem_list[i][j + 1]):
                output.append('ُ')

            else:
                output.append('ِ')
            output.extend(['ن', 'ْ'])
            return [output, 4]

        elif re.match('ّ', self.poem_list[i][j + 1]):
            if re.match(self.tokens['tanween_pattern'], self.poem_list[i][j + 2]):
                output = [self.poem_list[i][j], 'ْ', self.poem_list[i][j]]

                if re.match('ً', self.poem_list[i][j + 2]):
                    output.append('َ')

                elif re.match('ٌ', self.poem_list[i][j + 2]):
                    output.append('ُ')

                else:
                    output.append('ِ')

                output.extend(['ن', 'ْ'])

            else:
                output = [self.poem_list[i][j], 'ْ', self.poem_list[i][j], self.poem_list[i][j + 2]]

            return [output, 3]

        else:
            if re.match('ْ', self.poem_list[i][j + 1]):
                return [[self.poem_list[i][j], self.poem_list[i][j + 1]], 2]

            else:
                return [[self.poem_list[i][j], 'ْ'], 1]

    def normalize_3(self, i, j, normalized_poem):
        if self.is_delete_1(i, j, normalized_poem):
            if self.is_delete_2(i, j, normalized_poem, 'connect'):
                return 'delete'
            else:
                return [[], 2]
        elif self.is_delete_2(i, j, normalized_poem, 'disconnect'):
            return [[], 2]
        elif (i != len(self.poem_list) - 1 and re.match('ه', self.poem_list[i][j])
              and re.match(self.tokens['harakat_pattern'], self.poem_list[i][j + 1])
              and re.match(self.tokens['letters_pattern'], self.poem_list[i + 1][0])
              and re.match(self.tokens['harakat_pattern'], self.poem_list[i + 1][1])):
            return self.apply_add(i, j)
        elif i == len(self.poem_list) - 1 and re.match(self.tokens['harakat_pattern'], self.poem_list[i][j + 1]):
            return self.apply_add(i, j)
        else:
            return self.normalize_2(i, j)

    def is_al(self, i, j):
        return (re.match('ا', self.poem_list[i][j]) and re.match('ْ', self.poem_list[i][j + 1]) and
                re.match('ل', self.poem_list[i][j + 2]) and re.match('ْ', self.poem_list[i][j + 3]))

    def apply_al(self, i, j, op):
        if re.match('ّ', self.poem_list[i][j + 5]):
            if op == 'first':
                return [[self.poem_list[i][j], 'َ', self.poem_list[i][j + 4], 'ْ', self.poem_list[i][j + 4],
                         self.poem_list[i][j + 6]], 7]
            else:
                return [[self.poem_list[i][j + 4], 'ْ', self.poem_list[i][j + 4], self.poem_list[i][j + 6]], 7]
        else:
            if re.match(self.tokens['qamariya_letters'], self.poem_list[i][j + 4]):
                if op == 'first':
                    print(self.poem_list[i])
                    return [[self.poem_list[i][j], 'َ', self.poem_list[i][j + 2], 'ْ'], 4]
                else:
                    return [[self.poem_list[i][j + 2], 'ْ'], 4]
            else:
                if op == 'first':
                    return [[self.poem_list[i][j], 'َ'], 2]
                else:
                    return [[], 2]

    def is_delete_1(self, i, j, normalized_poem):
        return (
            re.match('ا', self.poem_list[i][j])
            and re.match('ْ', normalized_poem[i][-1])
            and re.match('و', normalized_poem[i][-2])
        )

    def is_delete_2(self, i, j, normalized_poem, op):
        if i != len(self.poem_list) - 1 and re.match('ا', self.poem_list[i + 1][0]):
            if op == 'connect':
                return (
                    re.match('و', normalized_poem[i][-2]) and re.match('ُ', normalized_poem[i][-3])
                )
            else:
                return (
                    re.match('ا', self.poem_list[i][j]) and re.match('َ', normalized_poem[i][-1])
                    or re.match('ى', self.poem_list[i][j]) and re.match('َ', normalized_poem[i][-1])
                    or re.match('و', self.poem_list[i][j]) and re.match('ُ', normalized_poem[i][-1])
                    or re.match('ي', self.poem_list[i][j]) and re.match('ِ', normalized_poem[i][-1])
                )

    def apply_add(self, i, j):
        output = [self.poem_list[i][j], self.poem_list[i][j + 1]]
        if re.match('َ', self.poem_list[i][j + 1]):
            output.append('ا')
        elif re.match('ُ', self.poem_list[i][j + 1]):
            output.append('و')
        else:
            output.append('ي')
        output.append('ْ')
        return [output, 2]

    @staticmethod
    def apply_special(word):
        if word == 'هذا':
            word.insert(2, 'ا')
        elif word == 'هذه':
            word.insert(2, 'ا')
        elif word == 'هذان':
            word.insert(2, 'ا')
        elif word == 'هذين':
            word.insert(2, 'ا')
        elif word == 'هؤلاء':
            word.insert(2, 'ا')
        elif word == 'ذلك':
            word.insert(2, 'ا')
        elif word == 'أولئك':
            word.insert(5, 'ا')
            del word[2]
        elif word == 'أولو':
            del word[2]
        elif word == 'أولاء':
            del word[2]
        elif word == 'أولات':
            del word[2]
        elif word == 'ذليكما':
            word.insert(2, 'ا')
        elif word == 'ذلكم':
            word.insert(2, 'ا')
        elif word == 'هكذا':
            word.insert(2, 'ا')
        elif word == 'ههنا':
            word.insert(2, 'ا')
        elif word == 'هذي':
            word.insert(2, 'ا')
        elif word == 'مائة':
            del word[2]
        elif word == 'مائتان':
            del word[2]
        elif word == 'الله':
            word = 'اَلْلَاه'
        elif word == 'الرحمن':
            word.insert(9, 'ا')
        elif word == 'إله':
            word.insert(3, 'ا')
        elif word == 'لكن':
            word.insert(2, 'ا')
        elif word == 'طه':
            word.insert(1, 'ا')
        elif word == 'إبرهيم':
            word.insert(4, 'ا')
        elif word == 'إسمعيل':
            word.insert(4, 'ا')
        elif word == 'يس':
            word.insert(1, 'ا')
            word.extend(['ي', 'ن'])
        elif word == 'طاوس':
            word.insert(5, 'و')
        elif word == 'داود':
            word.insert(5, 'و')
        return word

    def show_poem_process(self):
        print("Original Poem:")
        print(self.poem)
        print("\nListed Poem:")
        print(self.poem_list)
        print("\nNormalized Poem:")
        print(self.normalized_poem)
        print("\nTokenized Poem:")
        for i, j in self.tokenized_poem.items():
            print(f'{i} --> {j}')
