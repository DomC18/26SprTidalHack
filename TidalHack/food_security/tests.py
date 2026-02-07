from django.test import TestCase
from .models import FoodDesertArea, AnalysisResult
from .analysis import FoodDesertAnalyzer, SeverityLevel


class FoodDesertAnalyzerTestCase(TestCase):
    """Test cases for the FoodDesertAnalyzer"""
    
    def setUp(self):
        """Set up test data"""
        self.analyzer = FoodDesertAnalyzer()
        self.critical_area_data = {
            'area_name': 'Critical Test Area',
            'population': 5000,
            'poverty_rate': 35,
            'median_income': 25000,
            'distance_to_grocery': 5.5,
            'grocery_store_count': 0,
            'has_public_transit': False,
            'vehicle_ownership_rate': 40,
            'farmers_market_count': 0,
            'food_assistance_programs': 1,
            'unemployment_rate': 12,
            'food_insecurity_rate': 25,
            'health_problems_rate': 18,
        }
        
        self.mild_area_data = {
            'area_name': 'Mild Test Area',
            'population': 20000,
            'poverty_rate': 8,
            'median_income': 65000,
            'distance_to_grocery': 0.3,
            'grocery_store_count': 3,
            'has_public_transit': True,
            'vehicle_ownership_rate': 85,
            'farmers_market_count': 2,
            'food_assistance_programs': 3,
            'unemployment_rate': 4,
            'food_insecurity_rate': 5,
            'health_problems_rate': 2,
        }
    
    def test_critical_severity_calculation(self):
        """Test that critical areas are identified correctly"""
        result = self.analyzer.analyze_area(self.critical_area_data)
        self.assertEqual(result['severity_level'], 'critical')
        self.assertGreater(result['food_insecurity_score'], 75)
    
    def test_mild_severity_calculation(self):
        """Test that mild areas are identified correctly"""
        result = self.analyzer.analyze_area(self.mild_area_data)
        self.assertEqual(result['severity_level'], 'mild')
        self.assertLess(result['food_insecurity_score'], 20)
    
    def test_accessibility_score(self):
        """Test accessibility score calculation"""
        score = self.analyzer._calculate_accessibility_score(self.critical_area_data)
        self.assertLess(score, 40)  # Should be low due to poor accessibility
        
        score = self.analyzer._calculate_accessibility_score(self.mild_area_data)
        self.assertGreater(score, 80)  # Should be high due to good accessibility
    
    def test_income_score(self):
        """Test income adequacy score calculation"""
        score = self.analyzer._calculate_income_adequacy_score(self.critical_area_data)
        self.assertLess(score, 50)  # Low due to high poverty
        
        score = self.analyzer._calculate_income_adequacy_score(self.mild_area_data)
        self.assertGreater(score, 70)  # High due to low poverty
    
    def test_recommendations_generated(self):
        """Test that recommendations are generated"""
        result = self.analyzer.analyze_area(self.critical_area_data)
        self.assertTrue(len(result['recommendations']) > 0)
        self.assertIn('short_term_actions', result)
        self.assertIn('long_term_actions', result)
    
    def test_investment_estimate(self):
        """Test investment estimation for different severity levels"""
        critical_result = self.analyzer.analyze_area(self.critical_area_data)
        mild_result = self.analyzer.analyze_area(self.mild_area_data)
        
        self.assertIsNotNone(critical_result['estimated_investment'])
        self.assertIsNotNone(mild_result['estimated_investment'])


class FoodDesertAreaModelTest(TestCase):
    """Test cases for FoodDesertArea model"""
    
    def setUp(self):
        """Create test food desert area"""
        self.area = FoodDesertArea.objects.create(
            area_name='Test Community',
            latitude=40.7128,
            longitude=-74.0060,
            address='123 Main St',
            city='New York',
            state='NY',
            zip_code='10001',
            population=10000,
            poverty_rate=20.5,
            median_income=45000,
            distance_to_grocery=2.5,
            grocery_store_count=2,
            has_public_transit=True,
            vehicle_ownership_rate=65,
            farmers_market_count=1,
            food_assistance_programs=2,
            unemployment_rate=8,
            food_insecurity_rate=15,
            health_problems_rate=10,
        )
    
    def test_food_desert_creation(self):
        """Test FoodDesertArea creation"""
        self.assertEqual(self.area.area_name, 'Test Community')
        self.assertEqual(self.area.city, 'New York')
        self.assertEqual(self.area.population, 10000)
    
    def test_food_desert_string_representation(self):
        """Test string representation of FoodDesertArea"""
        expected_str = 'Test Community (New York, NY)'
        self.assertEqual(str(self.area), expected_str)
