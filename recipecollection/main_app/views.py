from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe

def about(req):
    return render(req, 'about.html')

def add_checkbox_to_lines(text):
    lines = text.splitlines()
    checkbox_html = '<input type="checkbox">'
    lines = [checkbox_html + line for line in lines]
    return "\n".join(lines)


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