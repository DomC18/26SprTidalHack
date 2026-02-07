from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FoodDesertArea(models.Model):
    """Model to store food desert area data"""
    
    # Location information
    area_name = models.CharField(max_length=255, help_text="Name of the food desert area")
    latitude = models.FloatField(help_text="Latitude coordinate")
    longitude = models.FloatField(help_text="Longitude coordinate")
    address = models.CharField(max_length=500, blank=True, help_text="Full address of the area")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    
    # Demographics and population statistics
    population = models.IntegerField(validators=[MinValueValidator(0)], help_text="Total population")
    poverty_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of population in poverty"
    )
    median_income = models.FloatField(validators=[MinValueValidator(0)], help_text="Median household income")
    
    # Food access metrics
    distance_to_grocery = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text="Average distance to nearest grocery store in miles"
    )
    grocery_store_count = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of grocery stores within service area"
    )
    
    # Infrastructure and transportation
    has_public_transit = models.BooleanField(default=False, help_text="Has public transportation")
    vehicle_ownership_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of households with vehicle access"
    )
    
    # Food retail diversity
    farmers_market_count = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of farmers markets"
    )
    food_assistance_programs = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Number of SNAP/WIC and other assistance programs"
    )
    
    # Community characteristics
    unemployment_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Unemployment rate percentage"
    )
    food_insecurity_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of population with food insecurity"
    )
    health_problems_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage with nutrition-related health problems"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_year = models.IntegerField(default=2024, help_text="Year of the data")
    
    class Meta:
        verbose_name = "Food Desert Area"
        verbose_name_plural = "Food Desert Areas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.area_name} ({self.city}, {self.state})"


class AnalysisResult(models.Model):
    """Model to store analysis results and recommendations"""
    
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('severe', 'Severe'),
        ('moderate', 'Moderate'),
        ('mild', 'Mild'),
    ]
    
    food_desert = models.OneToOneField(
        FoodDesertArea,
        on_delete=models.CASCADE,
        related_name='analysis'
    )
    
    # Analysis metrics
    severity_level = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        help_text="Severity level of food insecurity"
    )
    food_insecurity_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Overall food insecurity score (0-100)"
    )
    accessibility_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Food accessibility score (0-100)"
    )
    income_adequacy_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Income adequacy score (0-100)"
    )
    infrastructure_score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Infrastructure and transit score (0-100)"
    )
    
    # Analysis details
    key_challenges = models.TextField(help_text="Major challenges identified")
    recommendations = models.TextField(help_text="Detailed recommendations")
    short_term_actions = models.TextField(help_text="Actions to take in next 6 months")
    long_term_actions = models.TextField(help_text="Long-term strategies (1-3+ years)")
    
    # Recommended solutions
    priority_solutions = models.JSONField(
        default=list,
        help_text="List of priority solutions with details"
    )
    
    # Financial and resource estimates
    estimated_investment = models.CharField(
        max_length=50,
        help_text="Estimated investment needed (e.g., '$500K-$1M')"
    )
    implementation_timeline = models.CharField(
        max_length=100,
        help_text="Expected timeline for implementation"
    )
    
    # Analysis metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    analysis_version = models.IntegerField(default=1, help_text="Version of analysis algorithm used")
    
    class Meta:
        verbose_name = "Analysis Result"
        verbose_name_plural = "Analysis Results"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analysis: {self.food_desert.area_name} ({self.severity_level})"


class Recommendation(models.Model):
    """Individual recommendations for addressing food desert issues"""
    
    CATEGORY_CHOICES = [
        ('retail', 'Retail & Store Development'),
        ('transportation', 'Transportation & Access'),
        ('income', 'Income Support & Jobs'),
        ('education', 'Education & Literacy'),
        ('assistance', 'Food Assistance Programs'),
        ('community', 'Community Development'),
        ('policy', 'Policy & Advocacy'),
        ('technology', 'Technology & Innovation'),
    ]
    
    analysis = models.ForeignKey(
        AnalysisResult,
        on_delete=models.CASCADE,
        related_name='detailed_recommendations'
    )
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rationale = models.TextField(help_text="Why this recommendation is important")
    expected_impact = models.TextField(help_text="Expected outcomes and KPIs")
    implementation_steps = models.JSONField(default=list, help_text="Step-by-step implementation plan")
    required_resources = models.TextField(help_text="Required resources and partners")
    success_metrics = models.JSONField(default=list, help_text="Metrics to measure success")
    
    # Priority and feasibility
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="Priority level (1=highest, 5=lowest)"
    )
    feasibility = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text="Feasibility level (1=very difficult, 5=very easy)"
    )
    estimated_cost = models.CharField(max_length=50, help_text="Estimated cost range")
    timeline_months = models.IntegerField(help_text="Timeline in months")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', '-feasibility']
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
    
    def __str__(self):
        return f"{self.title} ({self.category})"
