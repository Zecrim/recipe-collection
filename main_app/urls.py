from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about', views.about, name='about'),
    path('recipes', views.recipe_index, name='recipe-index'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe-detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
    path('recipe-search/', views.recipe_search, name='recipe-search'),
    path('recipe-search/', views.recipe_search, name='recipe-search'),
    path('accounts/signup/', views.signup, name='signup')
]
