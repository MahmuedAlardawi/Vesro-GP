import re
from datetime import datetime
import json
import os

from api.algorithms.PoemTokenizer import PoemTokenizer
from api.algorithms.PoeticUnits import PoeticUnits

class PoemAnalyzer:
    def __init__(self, poem):
        self.poem = poem.strip()
        self.result = self.define_result()

    def analyze(self):

        final_result = None
        poem_tokenizer = PoemTokenizer(self.poem)
        tokenized_poem = poem_tokenizer.tokenized_poem

        best_match = 0
        for key, value in tokenized_poem.items():
            poetic_units = PoeticUnits(value)

            comparison = poetic_units.compare(poetic_units.taweel_see())
            results = poetic_units.result(comparison)
            result = poetic_units.get_match(results)

            if best_match < result[1]:
                best_match = result[1]
                final_result = [" ".join(poem_tokenizer.poem_list), key, value, result[0], best_match]

        return final_result

    @staticmethod
    def describe(result):
        description = {}

        discretized_poem = result[0]
        normalized_poem = result[1]
        tokenized_poem = result[2]
        meter = result[3]
        percentage = result[4]

        description['discretized_poem'] = discretized_poem
        description['normalized_poem'] = normalized_poem
        description['binary_poem'] = tokenized_poem
        description['meter'] =' '.join(tafeela[1] for tafeela in meter)
        description['matching_percentage'] = f'{percentage:.2f}%'
        description['words'] = []

        poem_no_space = ''.join(normalized_poem.split())

        index = 0
        for i in range(len(meter)):
            tokenized_tafeela = meter[i][0]
            tafeela = meter[i][1]

            change = {
                'قبض': 'القبض هو حذف الحرف الساكن الخامس من التفعيلة',
                'حذف': 'الحذف هو حذف الحرف المتحرك من آخر التفعيلة',
                None: None,
            }

            change = change[meter[i][2]]
            orginal_tafeela = meter[i][3]

            word = poem_no_space[index * 2 : index * 2  + len(tokenized_tafeela)*2]
            tokenized_word = ''
            for diacritic in word:
                if re.match(r'[َُِ]', diacritic):
                    tokenized_word += '1'
                elif re.match(r'ْ', diacritic):
                    tokenized_word += '0'

            comp = []
            for j in range(len(tokenized_word)):
                if tokenized_word[j] == tokenized_tafeela[j]:
                    comp.append(tokenized_word[j])  # Keep the matching element
                else:
                    comp.append('#')  # Replace mismatch with '#'

            comp.extend(['#' for _ in range(len(tokenized_tafeela) - len(tokenized_word))])
            comp = ''.join(comp)

            counter = 0
            for j in comp:
                if j != '#':
                    counter += 1

            word_percentage = counter/len(tokenized_tafeela) * 100

            index += len(tokenized_tafeela)

            description['words'].append({'normalized_word': word,
                                'binary_word': tokenized_word,
                                'tafeela': tafeela,
                                'binary_tafeela': tokenized_tafeela,
                                'binary_match': comp,
                                'matching_percentage': f'{word_percentage:.2f}%',
                                'change': change,
                                'original_tafeela': orginal_tafeela
                                })

        return description

    def define_result(self):
        result = self.analyze()

        describe = self.describe(result)

        return describe

    @staticmethod
    def display_result(result):
        # Display only the generated text for readability
        print("\n--- Structured Response ---")
        for key, value in result.items():
            print(f"{key}: {value}")

    @staticmethod
    def save_result_to_json_file(result):
        os.makedirs("ALLaM_output", exist_ok=True)

        # Save JSON data to a timestamped file
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_path = f"Analysis_output/result_{timestamp}.json"

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)

        print(f"\nResponse saved to {file_path}")

    @staticmethod
    def transfer_result_to_json_file(result):
        if result:
            return json.dumps(result, ensure_ascii=False, indent=4)
