from django import forms

class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Search for a dish', max_length=100)
