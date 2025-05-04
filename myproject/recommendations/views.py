from django.shortcuts import render
import pandas as pd
import numpy as np
import joblib
from django.shortcuts import render
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessing import preprocess_text  
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Load assets once at server startup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'recommendations/vectorizer.pkl'))
X = joblib.load(os.path.join(BASE_DIR, 'recommendations/X.pkl'))
df_original = pd.read_csv(os.path.join(BASE_DIR, 'recommendations/shl_catalog_full.csv'), encoding='ISO-8859-1')

def get_recommendations(user_input, vectorizer, X, top_n=10, min_similarity=0.1):
    processed_input = preprocess_text(user_input)
    user_vec = vectorizer.transform([processed_input])
    similarities = cosine_similarity(user_vec, X).flatten()
    sorted_indices = np.argsort(similarities)[::-1]
    filtered_indices = [i for i in sorted_indices if similarities[i] >= min_similarity]
    if not filtered_indices:
        filtered_indices = [sorted_indices[0]]
    top_indices = filtered_indices[:top_n]
    return top_indices

def home(request):
    results = None
    if request.method == 'POST':
        user_input = request.POST.get('description')
        indices = get_recommendations(user_input, vectorizer, X)
        columns = [
    'Title',
    'Category',
    'Remote Testing',
    'Adaptive/IRT',
    'Test Types',
    'Link',
    'Job Levels',
    'Languages',
    'Assessment Length (Minutes)'
]
        results = df_original.iloc[indices][columns].to_dict(orient='records')

    return render(request, 'home.html', {'results': results})

@csrf_exempt
def api_recommend(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            user_input = body.get('description', '')
            indices = get_recommendations(user_input, vectorizer, X)
            columns = [
                'Title',
                'Category',
                'Remote Testing',
                'Adaptive/IRT',
                'Test Types',
                'Link',
                'Job Levels',
                'Languages',
                'Assessment Length (Minutes)'
            ]
            results = df_original.iloc[indices][columns].to_dict(orient='records')
            return JsonResponse({'results': results}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POST request required'}, status=400)
