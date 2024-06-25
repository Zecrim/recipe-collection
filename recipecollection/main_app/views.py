from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.http import JsonResponse
from .models import Recipe
from .forms import RecipeSearchForm



def about(req):
    return render(req, 'about.html')

def get_api_data(query):
    url = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': '6067e86c3d544cb199cd62ec110d3463',
        'query': query,
        'number': 1,
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


def recipe_search(request):
    form = RecipeSearchForm()
    if request.method == 'POST':
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = get_api_data(query)
            if 'error' not in results and results.get('results'):
                recipe_data = results['results'][0]  # Get the first recipe
                name = recipe_data.get('title', 'No Title')
                cuisine = recipe_data.get('cuisines', [])
                ingredients = '\n'.join([ingredient['original'] for ingredient in recipe_data.get('extendedIngredients', [])])
                instructions = '\n'.join([step['step'] for instruction in recipe_data.get('analyzedInstructions', []) for step in instruction.get('steps', [])])
                image = recipe_data.get('image', '')
                user = request.user

                # Create and save the Recipe instance
                Recipe.objects.create(
                    name=name,
                    cuisine=cuisine,
                    ingredients=ingredients,
                    instructions=instructions,
                    image=image,
                    user=user
                )

                return redirect('recipe-index')  # Redirect to a list of recipes or any other page

    return render(request, 'recipe_search.html', {'form': form})

@login_required
def recipe_index(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'recipes/index.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    # dlcs_game_doesnt_have = Dlc.objects.exclude(id__in = game.dlcs.all().values_list('id'))
    return render(request, 'recipes/detail.html', {
        'recipe': recipe,
        # 'dlcs': dlcs_game_doesnt_have
    })


# @login_required
# def associate_dlc(request, game_id, dlc_id):
#     Game.objects.get(id=game_id).dlcs.add(dlc_id)
#     return redirect('game-detail', game_id=game_id)

def signup(request):
    # Handle the POST request
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # STEP 1: Create a user in the databse from the UserCreationForm
            login(request, user) # STEP 2: Log in as the craeted user
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
    
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user
        form.instance.ingredients = add_checkbox_to_lines(form.cleaned_data['ingredients'])
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class RecipeUpdate(LoginRequiredMixin,UpdateView):
    model = Recipe
    fields = ['name', 'cuisine', 'ingredients', 'instructions']

class RecipeDelete(LoginRequiredMixin,DeleteView):
    model = Recipe
    success_url = '/recipes'

# class DlcCreate(LoginRequiredMixin,CreateView):
#     model = Dlc
#     fields = '__all__'

# class DlcList(LoginRequiredMixin,ListView):
#     model = Dlc

# class DlcDetail(LoginRequiredMixin,DetailView):
#     model = Dlc

# class DlcUpdate(LoginRequiredMixin,UpdateView):
#     model = Dlc
#     fields = ['name', 'color']

# class DlcDelete(LoginRequiredMixin,DeleteView):
#     model = Dlc
#     success_url = '/dlcs/'

class Home(LoginView):
    template_name = 'home.html'