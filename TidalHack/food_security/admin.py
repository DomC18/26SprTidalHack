from django.contrib import admin
from .models import FoodDesertArea, AnalysisResult, Recommendation


@admin.register(FoodDesertArea)
class FoodDesertAreaAdmin(admin.ModelAdmin):
    list_display = (
        'area_name', 'city', 'state', 'population', 'poverty_rate',
        'distance_to_grocery', 'food_insecurity_rate', 'created_at'
    )
    list_filter = ('state', 'has_public_transit', 'data_year', 'created_at')
    search_fields = ('area_name', 'city', 'state', 'zip_code', 'address')
    
    fieldsets = (
        ('Location Information', {
            'fields': ('area_name', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code')
        }),
        ('Demographics & Population', {
            'fields': ('population', 'poverty_rate', 'median_income', 'unemployment_rate')
        }),
        ('Food Access Metrics', {
            'fields': ('distance_to_grocery', 'grocery_store_count', 'farmers_market_count', 'food_assistance_programs')
        }),
        ('Transportation & Infrastructure', {
            'fields': ('has_public_transit', 'vehicle_ownership_rate')
        }),
        ('Health & Food Security', {
            'fields': ('food_insecurity_rate', 'health_problems_rate')
        }),
        ('Metadata', {
            'fields': ('data_year', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        'food_desert', 'severity_level', 'food_insecurity_score',
        'accessibility_score', 'created_at'
    )
    list_filter = ('severity_level', 'created_at', 'analysis_version')
    search_fields = ('food_desert__area_name', 'food_desert__city')
    readonly_fields = (
        'food_desert', 'severity_level', 'food_insecurity_score',
        'accessibility_score', 'income_adequacy_score', 'infrastructure_score',
        'key_challenges', 'recommendations', 'short_term_actions',
        'long_term_actions', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Area Information', {
            'fields': ('food_desert',)
        }),
        ('Severity & Scores', {
            'fields': ('severity_level', 'food_insecurity_score', 'accessibility_score',
                      'income_adequacy_score', 'infrastructure_score')
        }),
        ('Analysis & Recommendations', {
            'fields': ('key_challenges', 'recommendations', 'short_term_actions', 'long_term_actions')
        }),
        ('Solutions & Timeline', {
            'fields': ('priority_solutions', 'estimated_investment', 'implementation_timeline')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'analysis_version'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'priority', 'feasibility',
        'estimated_cost', 'timeline_months', 'created_at'
    )
    list_filter = ('category', 'priority', 'feasibility', 'created_at')
    search_fields = ('title', 'description', 'analysis__food_desert__area_name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('analysis', 'category', 'title')
        }),
        ('Description & Rationale', {
            'fields': ('description', 'rationale', 'expected_impact')
        }),
        ('Implementation', {
            'fields': ('implementation_steps', 'required_resources', 'success_metrics')
        }),
        ('Assessment', {
            'fields': ('priority', 'feasibility', 'estimated_cost', 'timeline_months')
        }),
    )
    
    ordering = ('analysis', 'priority')
