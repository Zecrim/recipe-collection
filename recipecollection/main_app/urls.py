from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about', views.about, name='about'),
    path('recipes', views.recipe_index, name='recipe-index'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe-detail'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipe-create'),
    path('recipes/<int:pk>/update/', views.RecipeUpdate.as_view(), name='recipe-update'),
    path('recipes/<int:pk>/delete/', views.RecipeDelete.as_view(), name='recipe-delete'),
    # path('dlcs/create/', views.DlcCreate.as_view(), name='dlc-create'),
    # path('dlcs/<int:pk>/', views.DlcDetail.as_view(), name='dlc-detail'),
    # path('dlcs/', views.DlcList.as_view(), name='dlc-index'),
    # path('dlcs/<int:pk>/update/', views.DlcUpdate.as_view(), name='dlc-update'),
    # path('dlcs/<int:pk>/delete/', views.DlcDelete.as_view(), name='dlc-delete'),
    # path('games/<int:game_id>/associate-dlc/<int:dlc_id>/', views.associate_dlc, name='associate-dlc'),
    path('recipe-search/', views.recipe_search, name='recipe-search'),
    path('accounts/signup/', views.signup, name='signup')
]
