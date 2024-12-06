from django.urls import path
from .views import (
    generate_analysis,
    generate_explanation_colab,
    generate_poem_colab,
    generate_diacritization_colab,
    test_colab_api,
)

urlpatterns = [
    path('generate_analysis/', generate_analysis, name='generate_analysis'),  # Endpoint for receiving data
    path('generate_explanation_colab/', generate_explanation_colab, name='generate_explanation_colab'),  # Endpoint for receiving data
    path('generate_poem_colab/', generate_poem_colab, name='generate_poem_colab'),  # Endpoint for receiving data
    path('generate_diacritization_colab/', generate_diacritization_colab, name='generate_diacritization_colab'), # Endpoint for receiving data
    path('test_colab_api/', test_colab_api, name='test_colab_api'),  # Endpoint for receiving data

]
