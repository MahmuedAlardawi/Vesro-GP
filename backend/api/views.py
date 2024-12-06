from django.shortcuts import render

import json
from django.http import JsonResponse
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

import requests

from api.algorithms.PoemAnalyzer import PoemAnalyzer

colab_url = "https://8e51-35-240-182-192.ngrok-free.app/" # Change according to the generated url

def home(request):
    return HttpResponse("<h1>Welcome to the Django Backend!</h1>")

@csrf_exempt  # Disable CSRF for simplicity; use proper tokens in production
def generate_analysis(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            verse = data.get('verse')


            # Optional: Add logic to save to the database or process the data
            analyzer = PoemAnalyzer(verse)
            result = analyzer.result
            result_json = analyzer.transfer_result_to_json_file(result)

            # Return a success response
            return JsonResponse({
                'analysis': result_json,
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt  # Disable CSRF for simplicity; use proper tokens in production
def generate_explanation_colab(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            poem = data.get('poem')
            topic = data.get('topic')

            # Flatten the nested list into a single string for processing
            poem = "\n".join(
                " ".join(line.strip() for line in pair if isinstance(line, str)) for pair in poem)
            print(poem)

            # Ensure required data is provided
            if not topic or not poem:
                return JsonResponse({"error": "Missing topic or poem in the request"}, status=400)

            # Define all input types
            input_types = ["generate_general", "generate_detailed", "generate_story", "generate_images_description"]

            # Store responses from each input type
            responses = {}

            for input_type in input_types:
                # Construct the full Colab URL
                final_colab_url = f"{colab_url}{input_type}/"
                colab_data = {
                    'poem': poem,
                    'topic': topic,
                }

                # Send POST request to Colab for each input type
                response = requests.post(final_colab_url, json=colab_data)
                print(response.json())

                # Process the response from Colab
                if response.status_code == 200:
                    responses[input_type] = response.json()
                else:
                    responses[input_type] = {
                        "error": "Failed to connect to Colab",
                        "details": response.text
                    }

            # responses = {
            #     "generate_general": """
            #     القصيدة تحتفي بشخصية سلما كرمز للأمل والتقدم في مجال العلم. تُصور ذكاء سلما كضوء يضيء الدروب للآخرين، مانحًا إياهم الإلهام والطموح. تعكس الأبيات اجتهاد سلما في السعي نحو التفوق العلمي، ورؤيته لبناء إرث دائم في عالم المعرفة. الرحلة التي يخوضها سلما تتسم بالإصرار والعزيمة، مع تطلع دائم نحو النجوم، التي ترمز إلى الطموحات العالية والأحلام اللامتناهية.
            #     """,
            #     "generate_detailed": [
            #         "سلما أَتَى بِالمَزَايَا إِلَى العِلْمِ: البيت يُبرز سلما كشخصية تحمل صفات مميزة وتقدم إسهامات عظيمة في مجال العلم، مما يجعلها مصدرًا للتميز في هذا المجال.",
            #         "ذَكَاءٌ يُضِيءُ الدُّرُوبَ لَنَا أَمَلًا: يُشبه ذكاء سلما بضوء يُنير الطرق، مما يمنح الأمل والإلهام للآخرين في مسيرتهم العلمية.",
            #         "يُنَافِسُ فِي سَاحَةِ العِلْمِ جَاهِدًا: يعكس البيت اجتهاد سلما وروحه التنافسية في السعي لتحقيق إنجازات علمية مميزة.",
            #         "وَيَبْنِي لَنَا فِي المَعَارِفِ مَنْزِلًا: يُظهر دور سلما في بناء أساس متين في عالم المعرفة لصالح الأجيال القادمة.",
            #         "يَرَى فِي طَرِيقِ النُّجُومِ طُمُوحَهُ: الطموح هنا مرتبط بالنجوم، كإشارة إلى السعي وراء أهداف سامية وأحلام كبيرة.",
            #         "وَيَسْعَى إِلَى كُلِّ فَوْزٍ وَمُشْتَهى: البيت يختتم بالتأكيد على عزم سلما لتحقيق كل نجاح وبلوغ كل ما يطمح إليه."
            #     ],
            #     "generate_story": """
            #     في أحد الأيام، برز شخص يُدعى سلما في مجال العلم، ليصبح مصدر إلهام لكل من حوله. بذكاء خارق وطموح لا حدود له، شق طريقه بين النجوم، باحثًا عن حلول للتحديات العلمية الكبرى. اجتهد ليلًا ونهارًا، متفانيًا في خدمة المعرفة، وبنى معارف عميقة استندت عليها أجيال من العلماء بعده. أصبح اسمه مرتبطًا بالابتكار والتقدم، ورمزًا للأمل لكل من يسعى لتحقيق المستحيل.
            #     """,
            #     "generate_image_descriptions": [
            #         "1. سماء مليئة بالنجوم تتلألأ فوق عالم شغوف بالعلم، مع إشعاع ضوء يشبه الأمل ينبعث من الأرض.",
            #         "2. شخصية تقف على قمة جبل تحت سماء مرصعة بالنجوم، تعكس طموحًا نحو الإنجازات العلمية.",
            #         "3. مكتبة واسعة تحتوي على كتب مفتوحة، بينما يضيء شعاع من الضوء الصفحات كما لو كان يحمل المعرفة.",
            #         "4. مسار طويل يمر عبر الغابات والمحيطات، ينتهي بنجوم مضيئة في الأفق البعيد.",
            #         "5. يد تمسك بنجمة مشعة، ترمز إلى طموحات الإنسان التي تمتد إلى السماء.",
            #         "6. مدينة حديثة مع أبنية ذات تصميم علمي، تحتها شخصية تنظر إلى السماء بتفاؤل.",
            #         "7. مختبر علمي مضاء بإشعاعات خافتة، مليء بأدوات وتجارب تعكس سعي الإنسان للمعرفة.",
            #         "8. سماء مرسومة بألوان زاهية تشير إلى الأمل والطموح، مع طيور تحلق عالياً فوقها.",
            #         "9. لوحة تظهر شخصًا يكتب على ورقة تحت الضوء الخافت، مع تلميحات إلى الأفكار العلمية.",
            #         "10. شجرة كبيرة جذورها متعمقة في الكتب، وأوراقها تحمل رموزًا علمية تعكس المعرفة والنمو."
            #     ]
            # }

            # Return all responses
            return JsonResponse({
                'poem': poem,
                'topic': topic,
                'responses': responses
            })

        except Exception as e:
            return JsonResponse({"error": "An error occurred", "details": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt  # Disable CSRF for simplicity; use proper tokens in production
def generate_poem_colab(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            topic = data.get('topic')
            meter = data.get('meter')
            verse_count = data.get('verseCount')

            # Ensure required data is provided
            if not topic or not meter or not verse_count:
                return JsonResponse({"error": "Missing topic or meter or verses count in the request"}, status=400)

            input_type = 'generate_poem'

            # Construct the full Colab URL
            final_colab_url = f"{colab_url}{input_type}/"
            colab_data = {
                'topic': topic,
                'meter': meter,
                'verse_count': verse_count * 2,
                'input_type': input_type,
            }

            # # Send POST request to Colab
            # response = requests.post(final_colab_url, json=colab_data)
            #
            # # Process the response from Colab
            # if response.status_code == 200:
            #     colab_response = response.json()
            #     return JsonResponse({
            #         'topic': topic,
            #         'meter': meter,
            #         'verse_count': verse_count,
            #         'input_type': input_type,
            #         'response': colab_response,
            #     })
            # else:
            #     return JsonResponse({"error": "Failed to connect to Colab", "details": response.text},
            #                         status=response.status_code)

            return JsonResponse({
                'topic': topic,
                'meter': meter,
                'verse_count': verse_count,
                'input_type': input_type,
                'response': [
                    "سِلما أَتَى بِالمَزَايَا إِلَى العِلْمِ",
                    "ذَكَاءٌ يُضِيءُ الدُّرُوبَ لَنَا أَمَلًا",
                    "يُنَافِسُ فِي سَاحَةِ العِلْمِ جَاهِدًا",
                    "وَيَبْنِي لَنَا فِي المَعَارِفِ مَنْزِلًا",
                    "يَرَى فِي طَرِيقِ النُّجُومِ طُمُوحَهُ",
                    "وَيَسْعَى إِلَى كُلِّ فَوْزٍ وَمُشْتَهى"
                ]
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt  # Disable CSRF for simplicity; use proper tokens in production
def generate_diacritization_colab(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            poem = data.get('poem')

            # Ensure required data is provided
            if not poem:
                return JsonResponse({"error": "Missing poem in the request"}, status=400)

            input_type = 'generate_diacritization'

            # Construct the full Colab URL
            final_colab_url = f"{colab_url}{input_type}/"
            colab_data = {
                'poem': poem,
            }

            # Send POST request to Colab
            response = requests.post(final_colab_url, json=colab_data)

            # Process the response from Colab
            if response.status_code == 200:
                colab_response = response.json()
                return JsonResponse({
                    'poem': poem,
                    'input_type': input_type,
                    'response': colab_response,
                    # 'response': f"{poem} (تم التشكيل) "
                })
            else:
                return JsonResponse({"error": "Failed to connect to Colab", "details": response.text},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt  # Disable CSRF for simplicity; use proper tokens in production
def test_colab_api(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            message = data.get('message')

            # Ensure required data is provided
            if not message:
                return JsonResponse({"error": "Missing message in the request"}, status=400)

            input_type = 'test'

            # Construct the full Colab URL
            final_colab_url = f"{colab_url}{input_type}/"
            colab_data = {
                'message': message,
            }

            # Send POST request to Colab
            response = requests.post(final_colab_url, json=colab_data)

            # Process the response from Colab
            if response.status_code == 200:
                colab_response = response.json()
                return JsonResponse({
                    'message': message,
                    'response': colab_response
                })
            else:
                return JsonResponse({"error": "Failed to connect to Colab", "details": response.text},
                                    status=response.status_code)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
