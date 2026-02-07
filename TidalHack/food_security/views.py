from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodDesertArea, AnalysisResult, Recommendation
from .serializers import (
    FoodDesertAreaSerializer,
    AnalysisResultSerializer,
    RecommendationSerializer
)
from .analysis import FoodDesertAnalyzer
import json


# ===== REST API ViewSets =====

class FoodDesertAreaViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for FoodDesertArea
    
    Provides CRUD operations for food desert data
    """
    queryset = FoodDesertArea.objects.all()
    serializer_class = FoodDesertAreaSerializer
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """
        Analyze a specific food desert area
        POST /api/food-deserts/{id}/analyze/
        """
        area = self.get_object()
        analyzer = FoodDesertAnalyzer()
        
        # Convert model to dictionary for analysis
        area_data = FoodDesertAreaSerializer(area).data
        
        # Run analysis
        analysis_data = analyzer.analyze_area(area_data)
        
        # Create or update analysis result
        result, created = AnalysisResult.objects.update_or_create(
            food_desert=area,
            defaults={
                'severity_level': analysis_data['severity_level'],
                'food_insecurity_score': analysis_data['food_insecurity_score'],
                'accessibility_score': analysis_data['accessibility_score'],
                'income_adequacy_score': analysis_data['income_adequacy_score'],
                'infrastructure_score': analysis_data['infrastructure_score'],
                'key_challenges': analysis_data['key_challenges'],
                'recommendations': json.dumps(analysis_data['recommendations']),
                'short_term_actions': analysis_data['short_term_actions'],
                'long_term_actions': analysis_data['long_term_actions'],
                'priority_solutions': analysis_data['priority_solutions'],
                'estimated_investment': analysis_data['estimated_investment'],
                'implementation_timeline': analysis_data['implementation_timeline'],
            }
        )
        
        serializer = AnalysisResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def critical_areas(self, request):
        """
        Get all critical food desert areas
        GET /api/food-deserts/critical_areas/
        """
        critical_areas = []
        for area in FoodDesertArea.objects.all():
            if hasattr(area, 'analysis') and area.analysis.severity_level == 'critical':
                critical_areas.append(area)
        
        serializer = self.get_serializer(critical_areas, many=True)
        return Response(serializer.data)


class AnalysisResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for AnalysisResult
    
    Provides read-only access to analysis results
    """
    queryset = AnalysisResult.objects.all().select_related('food_desert').prefetch_related('detailed_recommendations')
    serializer_class = AnalysisResultSerializer
    
    @action(detail=False, methods=['get'])
    def by_severity(self, request):
        """
        Filter analysis results by severity level
        GET /api/analysis-results/by_severity/?severity=critical
        """
        severity = request.query_params.get('severity', None)
        if severity:
            results = AnalysisResult.objects.filter(severity_level=severity)
        else:
            results = AnalysisResult.objects.all()
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for Recommendation
    
    Provides read-only access to recommendations
    """
    queryset = Recommendation.objects.all().select_related('analysis')
    serializer_class = RecommendationSerializer
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Filter recommendations by category
        GET /api/recommendations/by_category/?category=retail
        """
        category = request.query_params.get('category', None)
        if category:
            results = Recommendation.objects.filter(category=category)
        else:
            results = Recommendation.objects.all()
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


class QuickAnalysisView(APIView):
    """
    Quick analysis endpoint for rapid assessment
    POST /api/quick-analysis/
    """
    
    def post(self, request):
        """
        Run quick analysis on submitted data
        """
        try:
            analyzer = FoodDesertAnalyzer()
            analysis_data = analyzer.analyze_area(request.data)
            return Response(analysis_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ===== Web Views =====

class FoodDesertListView(ListView):
    """Display list of all food desert areas"""
    model = FoodDesertArea
    template_name = 'food_security/area_list.html'
    context_object_name = 'areas'
    paginate_by = 20


class FoodDesertDetailView(DetailView):
    """Display detailed information about a food desert area with analysis"""
    model = FoodDesertArea
    template_name = 'food_security/area_detail.html'
    context_object_name = 'area'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.get_object()
        
        # Get analysis if it exists
        if hasattr(area, 'analysis'):
            context['analysis'] = area.analysis
            context['recommendations'] = area.analysis.detailed_recommendations.all()
        
        return context


class FoodDesertCreateView(CreateView):
    """Create a new food desert area entry"""
    model = FoodDesertArea
    template_name = 'food_security/area_form.html'
    fields = [
        'area_name', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code',
        'population', 'poverty_rate', 'median_income', 'distance_to_grocery',
        'grocery_store_count', 'has_public_transit', 'vehicle_ownership_rate',
        'farmers_market_count', 'food_assistance_programs', 'unemployment_rate',
        'food_insecurity_rate', 'health_problems_rate', 'data_year'
    ]
    success_url = reverse_lazy('food_security:area-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Food desert area "{self.object.area_name}" created successfully!')
        return response


class FoodDesertUpdateView(UpdateView):
    """Update an existing food desert area entry"""
    model = FoodDesertArea
    template_name = 'food_security/area_form.html'
    fields = [
        'area_name', 'latitude', 'longitude', 'address', 'city', 'state', 'zip_code',
        'population', 'poverty_rate', 'median_income', 'distance_to_grocery',
        'grocery_store_count', 'has_public_transit', 'vehicle_ownership_rate',
        'farmers_market_count', 'food_assistance_programs', 'unemployment_rate',
        'food_insecurity_rate', 'health_problems_rate', 'data_year'
    ]
    success_url = reverse_lazy('food_security:area-list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Food desert area "{self.object.area_name}" updated successfully!')
        return response


def index(request):
    """Dashboard view showing overview of all food desert areas"""
    total_areas = FoodDesertArea.objects.count()
    critical_analyses = AnalysisResult.objects.filter(severity_level='critical').count()
    severe_analyses = AnalysisResult.objects.filter(severity_level='severe').count()
    total_population_at_risk = FoodDesertArea.objects.aggregate(
        total=sum('population')
    )['total'] or 0
    
    # Get recent analyses
    recent_analyses = AnalysisResult.objects.select_related('food_desert').order_by('-created_at')[:5]
    
    context = {
        'total_areas': total_areas,
        'critical_count': critical_analyses,
        'severe_count': severe_analyses,
        'total_population': total_population_at_risk,
        'recent_analyses': recent_analyses,
    }
    
    return render(request, 'food_security/index.html', context)


def analysis_dashboard(request, pk):
    """Display analysis results and recommendations for an area"""
    area = get_object_or_404(FoodDesertArea, pk=pk)
    analysis = get_object_or_404(AnalysisResult, food_desert=area)
    recommendations = analysis.detailed_recommendations.all()
    
    context = {
        'area': area,
        'analysis': analysis,
        'recommendations': recommendations,
    }
    
    return render(request, 'food_security/analysis_dashboard_enhanced.html', context)
