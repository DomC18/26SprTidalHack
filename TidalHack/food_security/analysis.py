"""
Food Desert Analysis Engine

This module provides intelligent analysis of food desert areas and generates
actionable recommendations to improve food security.
"""

import math
from typing import Dict, List, Tuple
from enum import Enum


class SeverityLevel(Enum):
    """Food insecurity severity levels"""
    CRITICAL = 'critical'
    SEVERE = 'severe'
    MODERATE = 'moderate'
    MILD = 'mild'


class FoodDesertAnalyzer:
    """
    Analyzes food desert data and generates comprehensive recommendations
    """
    
    def __init__(self):
        """Initialize the analyzer with default thresholds"""
        self.thresholds = {
            'critical': 75,
            'severe': 60,
            'moderate': 40,
            'mild': 20,
        }
    
    def analyze_area(self, area_data: Dict) -> Dict:
        """
        Comprehensive analysis of a food desert area
        
        Args:
            area_data: Dictionary containing FoodDesertArea data
            
        Returns:
            Dictionary with analysis results and recommendations
        """
        # Calculate component scores
        accessibility_score = self._calculate_accessibility_score(area_data)
        income_score = self._calculate_income_adequacy_score(area_data)
        infrastructure_score = self._calculate_infrastructure_score(area_data)
        health_score = self._calculate_health_impact_score(area_data)
        
        # Calculate overall food insecurity score
        food_insecurity_score = self._calculate_food_insecurity_score(area_data)
        
        # Determine severity level
        severity = self._determine_severity(food_insecurity_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            area_data, 
            severity,
            accessibility_score,
            income_score,
            infrastructure_score,
            health_score
        )
        
        return {
            'food_insecurity_score': round(food_insecurity_score, 2),
            'accessibility_score': round(accessibility_score, 2),
            'income_adequacy_score': round(income_score, 2),
            'infrastructure_score': round(infrastructure_score, 2),
            'severity_level': severity.value,
            'key_challenges': self._identify_key_challenges(
                area_data,
                accessibility_score,
                income_score,
                infrastructure_score
            ),
            'short_term_actions': self._generate_short_term_actions(
                area_data, severity, recommendations
            ),
            'long_term_actions': self._generate_long_term_actions(
                area_data, severity, recommendations
            ),
            'recommendations': recommendations,
            'priority_solutions': self._rank_solutions(recommendations),
            'estimated_investment': self._estimate_investment(severity, recommendations),
            'implementation_timeline': self._estimate_timeline(severity),
        }
    
    def _calculate_accessibility_score(self, area_data: Dict) -> float:
        """Calculate food accessibility score (0-100)"""
        score = 100.0
        
        # Distance penalty: 0.5 miles is ideal, increases beyond that
        distance = area_data.get('distance_to_grocery', 1.0)
        if distance > 0.5:
            score -= min(40, (distance - 0.5) * 20)
        
        # Grocery store availability penalty
        grocery_stores = area_data.get('grocery_store_count', 0)
        if grocery_stores == 0:
            score -= 30
        elif grocery_stores == 1:
            score -= 15
        
        # Farmers market availability bonus
        farmers_markets = area_data.get('farmers_market_count', 0)
        score += min(10, farmers_markets * 3)
        
        # Vehicle ownership impact
        vehicle_rate = area_data.get('vehicle_ownership_rate', 50)
        transit = area_data.get('has_public_transit', False)
        
        if vehicle_rate < 50 and not transit:
            score -= 20
        elif vehicle_rate < 70 and not transit:
            score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_income_adequacy_score(self, area_data: Dict) -> float:
        """Calculate income adequacy for food security (0-100)"""
        score = 100.0
        
        # Poverty rate impact
        poverty = area_data.get('poverty_rate', 20)
        score -= poverty * 0.8  # Higher poverty reduces score
        
        # Food assistance availability
        assistance = area_data.get('food_assistance_programs', 0)
        score += min(15, assistance * 5)  # Bonus for food assistance
        
        # Food insecurity rate (direct impact)
        food_insecurity = area_data.get('food_insecurity_rate', 12)
        score -= food_insecurity * 0.7
        
        return max(0, min(100, score))
    
    def _calculate_infrastructure_score(self, area_data: Dict) -> float:
        """Calculate transportation and infrastructure score (0-100)"""
        score = 100.0
        
        # Public transit availability
        if not area_data.get('has_public_transit', False):
            score -= 30
        
        # Vehicle ownership
        vehicle_rate = area_data.get('vehicle_ownership_rate', 50)
        if vehicle_rate < 60:
            score -= (60 - vehicle_rate) * 0.5
        
        # Population density (proxy for infrastructure)
        population = area_data.get('population', 5000)
        if population < 2000:
            score -= 20  # Sparse areas have less infrastructure
        
        return max(0, min(100, score))
    
    def _calculate_health_impact_score(self, area_data: Dict) -> float:
        """Calculate health impact of food insecurity (0-100)"""
        score = 100.0
        
        # Health problems related to nutrition
        health_problems = area_data.get('health_problems_rate', 10)
        score -= health_problems * 2
        
        # Correlation with unemployment
        unemployment = area_data.get('unemployment_rate', 5)
        score -= unemployment * 1.5
        
        return max(0, min(100, score))
    
    def _calculate_food_insecurity_score(self, area_data: Dict) -> float:
        """
        Calculate overall food insecurity score (0-100)
        Uses weighted average of multiple factors
        """
        accessibility = self._calculate_accessibility_score(area_data)
        income = self._calculate_income_adequacy_score(area_data)
        infrastructure = self._calculate_infrastructure_score(area_data)
        health = self._calculate_health_impact_score(area_data)
        
        # Direct data point
        reported_insecurity = area_data.get('food_insecurity_rate', 12)
        
        # Weighted average (inverse scale - higher score = more insecurity)
        score = (
            (100 - accessibility) * 0.25 +  # Accessibility 25%
            (100 - income) * 0.25 +          # Income 25%
            (100 - infrastructure) * 0.15 +  # Infrastructure 15%
            (100 - health) * 0.15 +         # Health 15%
            reported_insecurity * 0.2        # Reported rate 20%
        )
        
        return min(100, score)
    
    def _determine_severity(self, score: float) -> SeverityLevel:
        """Determine severity level based on score"""
        if score >= 75:
            return SeverityLevel.CRITICAL
        elif score >= 60:
            return SeverityLevel.SEVERE
        elif score >= 40:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MILD
    
    def _identify_key_challenges(
        self,
        area_data: Dict,
        accessibility: float,
        income: float,
        infrastructure: float
    ) -> str:
        """Identify and describe key challenges"""
        challenges = []
        
        if accessibility < 50:
            challenges.append("Limited food store access - distance and availability issues")
        
        if income < 40:
            challenges.append("High poverty and income constraints limiting food purchasing power")
        
        if infrastructure < 40:
            challenges.append("Inadequate transportation infrastructure for food access")
        
        if area_data.get('unemployment_rate', 0) > 10:
            challenges.append(f"High unemployment rate ({area_data.get('unemployment_rate')}%)")
        
        if area_data.get('has_public_transit', False) is False:
            challenges.append("No public transportation available")
        
        if area_data.get('grocery_store_count', 0) == 0:
            challenges.append("CRITICAL: No grocery stores in service area")
        
        return "\n• ".join(["Key Challenges:"] + challenges) if challenges else "No major challenges identified"
    
    def _generate_recommendations(
        self,
        area_data: Dict,
        severity: SeverityLevel,
        accessibility: float,
        income: float,
        infrastructure: float,
        health: float
    ) -> List[Dict]:
        """Generate detailed recommendations based on analysis"""
        recommendations = []
        
        # Critical accessibility issues
        if accessibility < 40:
            recommendations.append({
                'category': 'retail',
                'priority': 1,
                'title': 'Establish New Grocery Store or Food Hub',
                'description': 'Create a full-service grocery store or community food hub within walking distance',
                'rationale': f'Current distance to nearest grocery is {area_data.get("distance_to_grocery", 5)} miles',
                'expected_impact': '40-60% increase in fresh food access, reduced food insecurity by 30-50%',
                'feasibility': 2,
                'estimated_cost': '$500K-$2M',
                'timeline': 18,
            })
        
        # Transportation issues
        if infrastructure < 40:
            recommendations.append({
                'category': 'transportation',
                'priority': 1 if severity == SeverityLevel.CRITICAL else 2,
                'title': 'Implement Food Access Transportation Program',
                'description': 'Create shuttle services or subsidized transport to food retailers',
                'rationale': f'Vehicle ownership rate is {area_data.get("vehicle_ownership_rate", 50)}%',
                'expected_impact': '25-40% improvement in food accessibility',
                'feasibility': 4,
                'estimated_cost': '$50K-$200K annually',
                'timeline': 6,
            })
        
        # Income support
        if income < 40:
            recommendations.append({
                'category': 'income',
                'priority': 1,
                'title': 'Expand Income Support and Job Creation',
                'description': 'Launch job training, education, and employment programs',
                'rationale': f'Poverty rate is {area_data.get("poverty_rate", 20)}%',
                'expected_impact': '30-50% increase in household income, improved food security',
                'feasibility': 2,
                'estimated_cost': '$200K-$1M annually',
                'timeline': 12,
            })
        
        # Food assistance programs
        if area_data.get('food_assistance_programs', 0) < 2:
            recommendations.append({
                'category': 'assistance',
                'priority': 2,
                'title': 'Expand Food Assistance Programs',
                'description': 'Increase SNAP/WIC availability, add emergency food programs',
                'rationale': 'Insufficient existing food assistance infrastructure',
                'expected_impact': '20-35% reduction in food insecurity short-term',
                'feasibility': 4,
                'estimated_cost': '$50K-$300K annually',
                'timeline': 3,
            })
        
        # Community education
        recommendations.append({
            'category': 'education',
            'priority': 3,
            'title': 'Launch Nutrition and Food Literacy Programs',
            'description': 'Community workshops on nutrition, cooking, budgeting',
            'rationale': 'Maximize impact of available food resources',
            'expected_impact': '15-25% improvement in nutritional outcomes',
            'feasibility': 5,
            'estimated_cost': '$20K-$100K annually',
            'timeline': 3,
        })
        
        # Farmers markets and local production
        if area_data.get('farmers_market_count', 0) < 1:
            recommendations.append({
                'category': 'retail',
                'priority': 3,
                'title': 'Develop Local Food Production Capacity',
                'description': 'Start community gardens, farmers markets, urban farms',
                'rationale': 'Increase local fresh food availability and community engagement',
                'expected_impact': '10-20% increase in fresh produce availability',
                'feasibility': 5,
                'estimated_cost': '$30K-$150K',
                'timeline': 12,
            })
        
        # Policy advocacy
        recommendations.append({
            'category': 'policy',
            'priority': 4,
            'title': 'Policy Advocacy and Zoning Reform',
            'description': 'Work with government to reform zoning and support retail development',
            'rationale': 'Address systemic barriers to grocery store development',
            'expected_impact': 'Long-term structural improvement in food access',
            'feasibility': 2,
            'estimated_cost': 'Variable',
                        'timeline': 24,
            })
        
        return recommendations
    
    def _generate_short_term_actions(
        self,
        area_data: Dict,
        severity: SeverityLevel,
        recommendations: List[Dict]
    ) -> str:
        """Generate short-term action plan (0-6 months)"""
        actions = [
            "1. Assess and map existing food resources (stores, assistance programs)",
            "2. Conduct community needs assessment and engagement",
            "3. Apply for emergency food assistance grants and programs",
            "4. Launch food pantry or emergency food distribution",
            "5. Initiate partnerships with local nonprofits and government agencies",
        ]
        
        if severity == SeverityLevel.CRITICAL:
            actions.insert(0, "0. URGENT: Implement emergency food assistance measures immediately")
        
        return "\n".join(actions)
    
    def _generate_long_term_actions(
        self,
        area_data: Dict,
        severity: SeverityLevel,
        recommendations: List[Dict]
    ) -> str:
        """Generate long-term action plan (1-3+ years)"""
        actions = [
            "1. Develop grocery store recruitment and support program",
            "2. Create sustainable funding model for food access initiatives",
            "3. Build community wealth and economic development",
            "4. Implement systemic policy changes (zoning, incentives)",
            "5. Establish permanent community food systems infrastructure",
            "6. Monitor and evaluate progress with key metrics",
            "7. Scale successful models to other food desert areas",
        ]
        
        return "\n".join(actions)
    
    def _rank_solutions(self, recommendations: List[Dict]) -> List[Dict]:
        """Rank solutions by priority and feasibility"""
        # Create priority score: lower priority number + higher feasibility = better
        ranked = []
        for rec in recommendations:
            priority_score = rec['priority'] - (rec['feasibility'] / 10)
            ranked.append({
                'title': rec['title'],
                'category': rec['category'],
                'priority_score': priority_score,
                'priority': rec['priority'],
                'feasibility': rec['feasibility'],
                'timeline': rec['timeline'],
                'cost': rec['estimated_cost'],
            })
        
        return sorted(ranked, key=lambda x: x['priority_score'])
    
    def _estimate_investment(self, severity: SeverityLevel, recommendations: List[Dict]) -> str:
        """Estimate total investment needed"""
        if severity == SeverityLevel.CRITICAL:
            return '$1M - $3M'
        elif severity == SeverityLevel.SEVERE:
            return '$500K - $1.5M'
        elif severity == SeverityLevel.MODERATE:
            return '$250K - $750K'
        else:
            return '$100K - $300K'
    
    def _estimate_timeline(self, severity: SeverityLevel) -> str:
        """Estimate implementation timeline"""
        if severity == SeverityLevel.CRITICAL:
            return '2-3 years for critical interventions, 5-7 years for full transformation'
        elif severity == SeverityLevel.SEVERE:
            return '2-4 years for major improvements, 5-8 years for full transformation'
        else:
            return '3-5 years for significant progress'
