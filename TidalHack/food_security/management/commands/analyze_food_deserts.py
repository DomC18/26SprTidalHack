from django.core.management.base import BaseCommand
from food_security.models import FoodDesertArea, AnalysisResult, Recommendation
from food_security.analysis import FoodDesertAnalyzer
import json


class Command(BaseCommand):
    help = 'Analyze food desert areas and generate recommendations'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--area-id',
            type=int,
            help='Analyze a specific area by ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Analyze all areas'
        )
    
    def handle(self, *args, **options):
        analyzer = FoodDesertAnalyzer()
        
        if options['area_id']:
            # Analyze specific area
            try:
                area = FoodDesertArea.objects.get(pk=options['area_id'])
                self.analyze_area(analyzer, area)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully analyzed area: {area.area_name}')
                )
            except FoodDesertArea.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Area with ID {options["area_id"]} not found')
                )
        
        elif options['all']:
            # Analyze all areas
            areas = FoodDesertArea.objects.all()
            for area in areas:
                self.analyze_area(analyzer, area)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully analyzed {areas.count()} areas')
            )
        
        else:
            self.stdout.write(
                self.style.WARNING('Please specify --area-id or --all')
            )
    
    def analyze_area(self, analyzer, area):
        """Analyze a single area"""
        area_data = {
            'area_name': area.area_name,
            'population': area.population,
            'poverty_rate': area.poverty_rate,
            'median_income': area.median_income,
            'distance_to_grocery': area.distance_to_grocery,
            'grocery_store_count': area.grocery_store_count,
            'has_public_transit': area.has_public_transit,
            'vehicle_ownership_rate': area.vehicle_ownership_rate,
            'farmers_market_count': area.farmers_market_count,
            'food_assistance_programs': area.food_assistance_programs,
            'unemployment_rate': area.unemployment_rate,
            'food_insecurity_rate': area.food_insecurity_rate,
            'health_problems_rate': area.health_problems_rate,
        }
        
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
        
        # Create detailed recommendations
        if created or not result.detailed_recommendations.exists():
            result.detailed_recommendations.all().delete()
            
            for rec_data in analysis_data['recommendations']:
                Recommendation.objects.create(
                    analysis=result,
                    category=rec_data['category'],
                    title=rec_data['title'],
                    description=rec_data['description'],
                    rationale=rec_data['rationale'],
                    expected_impact=rec_data['expected_impact'],
                    implementation_steps=[],
                    required_resources='',
                    success_metrics=[],
                    priority=rec_data['priority'],
                    feasibility=rec_data['feasibility'],
                    estimated_cost=rec_data['estimated_cost'],
                    timeline_months=rec_data['timeline'],
                )
