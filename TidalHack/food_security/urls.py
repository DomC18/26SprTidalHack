from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for API viewsets
router = DefaultRouter()
router.register(r'food-deserts', views.FoodDesertAreaViewSet)
router.register(r'analysis-results', views.AnalysisResultViewSet)
router.register(r'recommendations', views.RecommendationViewSet)

app_name = 'food_security'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/quick-analysis/', views.QuickAnalysisView.as_view(), name='quick-analysis'),
    
    # Web views
    path('', views.index, name='index'),
    path('areas/', views.FoodDesertListView.as_view(), name='area-list'),
    path('areas/new/', views.FoodDesertCreateView.as_view(), name='area-create'),
    path('areas/<int:pk>/', views.FoodDesertDetailView.as_view(), name='area-detail'),
    path('areas/<int:pk>/edit/', views.FoodDesertUpdateView.as_view(), name='area-update'),
    path('areas/<int:pk>/analysis/', views.analysis_dashboard, name='analysis-dashboard'),
]
