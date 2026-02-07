from rest_framework import serializers
from .models import FoodDesertArea, AnalysisResult, Recommendation


class FoodDesertAreaSerializer(serializers.ModelSerializer):
    """Serializer for FoodDesertArea model"""
    
    class Meta:
        model = FoodDesertArea
        fields = [
            'id', 'area_name', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code',
            'population', 'poverty_rate', 'median_income', 'distance_to_grocery',
            'grocery_store_count', 'has_public_transit', 'vehicle_ownership_rate',
            'farmers_market_count', 'food_assistance_programs', 'unemployment_rate',
            'food_insecurity_rate', 'health_problems_rate', 'created_at', 'updated_at', 'data_year'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RecommendationSerializer(serializers.ModelSerializer):
    """Serializer for Recommendation model"""
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'category', 'title', 'description', 'rationale', 'expected_impact',
            'implementation_steps', 'required_resources', 'success_metrics',
            'priority', 'feasibility', 'estimated_cost', 'timeline_months', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AnalysisResultSerializer(serializers.ModelSerializer):
    """Serializer for AnalysisResult model"""
    
    detailed_recommendations = RecommendationSerializer(many=True, read_only=True)
    food_desert = FoodDesertAreaSerializer(read_only=True)
    
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'food_desert', 'severity_level', 'food_insecurity_score',
            'accessibility_score', 'income_adequacy_score', 'infrastructure_score',
            'key_challenges', 'recommendations', 'short_term_actions', 'long_term_actions',
            'priority_solutions', 'estimated_investment', 'implementation_timeline',
            'detailed_recommendations', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'severity_level', 'food_insecurity_score', 'accessibility_score',
            'income_adequacy_score', 'infrastructure_score', 'key_challenges',
            'recommendations', 'short_term_actions', 'long_term_actions',
            'priority_solutions', 'estimated_investment', 'implementation_timeline',
            'created_at', 'updated_at'
        ]
