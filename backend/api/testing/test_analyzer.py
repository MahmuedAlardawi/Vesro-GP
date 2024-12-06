from api.algorithms.PoemAnalyzer import PoemAnalyzer


poem1 = """
يَا مَدِينَةُ المنُورَةِ، يَا نُورُ اللَّهِ فِي الأَرْض

"""
analyzer = PoemAnalyzer(poem1)
result1 = analyzer.result

analyzer.display_result(result1)
# analyzer.save_result_to_json_file(result1)