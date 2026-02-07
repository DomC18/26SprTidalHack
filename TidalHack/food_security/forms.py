from django import forms
from .models import FoodDesertArea, AnalysisResult, Recommendation


class FoodDesertAreaForm(forms.ModelForm):
    """Form for creating and editing FoodDesertArea"""
    
    class Meta:
        model = FoodDesertArea
        fields = [
            'area_name', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code',
            'population', 'poverty_rate', 'median_income', 'distance_to_grocery',
            'grocery_store_count', 'has_public_transit', 'vehicle_ownership_rate',
            'farmers_market_count', 'food_assistance_programs', 'unemployment_rate',
            'food_insecurity_rate', 'health_problems_rate', 'data_year'
        ]
        
        widgets = {
            'area_name': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'population': forms.NumberInput(attrs={'class': 'form-control'}),
            'poverty_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'median_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'distance_to_grocery': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'grocery_store_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'has_public_transit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vehicle_ownership_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'farmers_market_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'food_assistance_programs': forms.NumberInput(attrs={'class': 'form-control'}),
            'unemployment_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'food_insecurity_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'health_problems_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'data_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        help_texts = {
            'poverty_rate': 'Percentage of population in poverty (0-100)',
            'vehicle_ownership_rate': 'Percentage of households with vehicle (0-100)',
            'unemployment_rate': 'Percentage unemployed (0-100)',
            'food_insecurity_rate': 'Percentage experiencing food insecurity (0-100)',
            'health_problems_rate': 'Percentage with nutrition-related health issues (0-100)',
        }
