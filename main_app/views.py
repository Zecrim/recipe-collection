from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .models import Recipe
from .forms import RecipeSearchForm



def about(req):
    return render(req, 'about.html')

def get_api_data(query):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': '6067e86c3d544cb199cd62ec110d3463',
        'query': query,
        'number': 10,
        'addRecipeInformation': True,
        'fillIngredients': True,
        'addRecipeInstructions': True,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    return data

@login_required
def recipe_search(request):
    form = RecipeSearchForm()
    recipes = []
    if request.method == 'POST':
        if 'search-button' in request.POST:
            form = RecipeSearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = get_api_data(query)
                if 'error' not in results and results.get('results'):
                    recipes = results['results']
                    # Save the recipes to the session
                    request.session['recipes'] = recipes
        elif 'add-button' in request.POST:
            recipe_id = request.POST.get('recipe_id')
            recipes = request.session.get('recipes', [])
            for recipe_data in recipes:
                if str(recipe_data['id']) == recipe_id:
                    name = recipe_data.get('title', 'No Title')
                    cuisine = recipe_data.get('cuisines', [''])[0]
                    ingredients = '\n'.join([ingredient['original'] for ingredient in recipe_data.get('extendedIngredients', [])])
                    instructions = '\n'.join([f"{i+1}. {step['step']}" for i, step in enumerate([step for instruction in recipe_data.get('analyzedInstructions', []) for step in instruction.get('steps', [])])])
                    image = recipe_data.get('image', '')
                    user = request.user

                    Recipe.objects.create(
                        name=name,
                        cuisine=cuisine,
                        ingredients=ingredients,
                        instructions=instructions,
                        image=image,
                        user=user
                    )

                    return redirect('recipe-index')

    return render(request, 'main_app/recipe_search.html', {'form': form, 'recipes': recipes})

@login_required
def recipe_index(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes/index.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
    })


def signup(request):
    # Handle the POST request
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe-index')
        else:
            error_message = 'Invalid sign up - try again'
    # Handle the GET request (render the form)
    form = UserCreationForm()
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'cuisine', 'ingredients', 'instructions']
    success_url = '/recipes'


class RecipeUpdate(LoginRequiredMixin,UpdateView):
    model = Recipe
    fields = ['name', 'cuisine', 'ingredients', 'instructions']

class RecipeDelete(LoginRequiredMixin,DeleteView):
    model = Recipe
    success_url = '/recipes'

class Home(LoginView):
    template_name = 'home.html'