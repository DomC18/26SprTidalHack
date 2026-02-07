# Food Security & Desert Analysis System

A comprehensive AI/ML-powered Django application for analyzing food desert areas and generating data-driven recommendations to improve food security and accessibility.

## Overview

This system helps communities and organizations:
- **Identify** food desert areas with limited food access
- **Analyze** food insecurity factors using machine learning algorithms
- **Generate** actionable, prioritized recommendations for improvement
- **Track** progress toward food security goals
- **Plan** interventions with cost and timeline estimates

## Features

### 🔍 Comprehensive Analysis Engine
- **Multi-factor Assessment**: Analyzes 13+ key indicators including:
  - Food accessibility (distance, store availability)
  - Income adequacy (poverty rates, employment)
  - Transportation infrastructure
  - Food assistance program availability
  - Health and nutrition outcomes

- **Severity Scoring**: Calculates food insecurity scores (0-100) with severity levels:
  - Critical (75-100): Immediate action required
  - Severe (60-74): High priority intervention
  - Moderate (40-59): Medium-term planning needed
  - Mild (0-39): Monitoring and preventive measures

### 💡 Intelligent Recommendations
- **8 Solution Categories**:
  1. Retail & Store Development
  2. Transportation & Access
  3. Income Support & Jobs
  4. Education & Literacy
  5. Food Assistance Programs
  6. Community Development
  7. Policy & Advocacy
  8. Technology & Innovation

- **Smart Prioritization**: Solutions ranked by:
  - Priority level (1-5)
  - Implementation feasibility
  - Cost estimates
  - Timeline projections

### 📊 Interactive Dashboard
- Real-time analytics and visualizations
- Severity level distribution
- Population impact metrics
- Recent analysis history
- Quick access to detailed reports

### 🛠️ Management Tools
- **REST API**: Full API for programmatic access
- **Web Interface**: User-friendly data entry and visualization
- **Django Admin**: Comprehensive admin panel
- **Management Commands**: Batch analysis operations

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 6.0.2+
- PostgreSQL or SQLite (default)

### Quick Start

1. **Clone and navigate to project**:
```bash
cd /home/khush/TIDALHACK/26SprTidalHack
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run migrations**:
```bash
cd TidalHack
python manage.py migrate
```

5. **Create superuser**:
```bash
python manage.py createsuperuser
```

6. **Run development server**:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Usage

### Web Interface

#### Dashboard
- **URL**: `/`
- View overview statistics
- See recent analyses
- Quick access to tools

#### Food Desert Areas
- **URL**: `/areas/`
- Browse all food desert areas
- View area details and previous analyses
- Add new areas

#### Create New Area
- **URL**: `/areas/new/`
- Enter comprehensive area data:
  - Location information
  - Demographics
  - Food access metrics
  - Transportation infrastructure
  - Health metrics

#### Analysis Dashboard
- **URL**: `/areas/<id>/analysis/`
- View detailed analysis results
- Review severity scores
- See prioritized recommendations
- Export insights for planning

### REST API

#### Base URL
```
http://localhost:8000/api/
```

#### Endpoints

**Food Desert Areas**:
```
GET    /api/food-deserts/                    # List all areas
POST   /api/food-deserts/                    # Create new area
GET    /api/food-deserts/{id}/               # Get area details
PUT    /api/food-deserts/{id}/               # Update area
DELETE /api/food-deserts/{id}/               # Delete area
POST   /api/food-deserts/{id}/analyze/       # Run analysis
GET    /api/food-deserts/critical_areas/     # Get critical areas
```

**Analysis Results**:
```
GET    /api/analysis-results/                # List all analyses
GET    /api/analysis-results/{id}/           # Get analysis details
GET    /api/analysis-results/by_severity/?severity=critical
```

**Recommendations**:
```
GET    /api/recommendations/                 # List all recommendations
GET    /api/recommendations/{id}/            # Get recommendation
GET    /api/recommendations/by_category/?category=retail
```

**Quick Analysis**:
```
POST   /api/quick-analysis/                  # Rapid assessment endpoint
```

### Management Commands

#### Analyze specific area:
```bash
python manage.py analyze_food_deserts --area-id=1
```

#### Analyze all areas:
```bash
python manage.py analyze_food_deserts --all
```

## Database Models

### FoodDesertArea
Stores comprehensive data about food desert regions:
- Location (coordinates, address)
- Demographics (population, poverty, income)
- Food access metrics (distance, store count)
- Infrastructure (transit, vehicles)
- Health indicators

### AnalysisResult
Stores analysis outcomes for each area:
- Severity level assessment
- Component scores (accessibility, income, infrastructure)
- Key challenges identified
- Short-term and long-term action plans
- Recommended solutions with priorities

### Recommendation
Individual recommendations within an analysis:
- Category classification
- Priority and feasibility ratings
- Cost estimates
- Implementation timeline
- Success metrics

## Analysis Algorithm

The system uses a sophisticated weighted scoring algorithm:

```
Food Insecurity Score = (
  (100 - Accessibility) × 0.25 +      # Food access 25%
  (100 - Income) × 0.25 +             # Income adequacy 25%
  (100 - Infrastructure) × 0.15 +     # Transportation 15%
  (100 - Health) × 0.15 +             # Health outcomes 15%
  Reported Insecurity Rate × 0.2      # Reported data 20%
)
```

Each component score is calculated from multiple factors:
- **Accessibility**: Distance to grocery, store availability, farmers markets
- **Income**: Poverty rate, median income, food assistance programs
- **Infrastructure**: Public transit, vehicle ownership, population density
- **Health**: Nutrition-related health problems, unemployment

## Recommendation Generation

The system intelligently generates recommendations based on:
1. **Area's severity level** - Critical areas get urgent interventions
2. **Component weaknesses** - Focused on lowest-scoring areas
3. **Data-driven insights** - Specific metrics drive recommendations
4. **Feasibility assessment** - Realistic timelines and costs
5. **Impact potential** - Highest ROI solutions prioritized

## API Examples

### Create Food Desert Area
```bash
curl -X POST http://localhost:8000/api/food-deserts/ \
  -H "Content-Type: application/json" \
  -d '{
    "area_name": "Downtown Community",
    "city": "Springfield",
    "state": "IL",
    "latitude": 39.7817,
    "longitude": -89.6501,
    "population": 5000,
    "poverty_rate": 25.0,
    "median_income": 35000,
    "distance_to_grocery": 3.5,
    "grocery_store_count": 1,
    "has_public_transit": true,
    "vehicle_ownership_rate": 60,
    "unemployment_rate": 8.5,
    "food_insecurity_rate": 18.0
  }'
```

### Analyze Area
```bash
curl -X POST http://localhost:8000/api/food-deserts/1/analyze/
```

### Quick Analysis (without storing)
```bash
curl -X POST http://localhost:8000/api/quick-analysis/ \
  -H "Content-Type: application/json" \
  -d '{
    "area_name": "Test Area",
    "population": 5000,
    "poverty_rate": 25,
    ...
  }'
```

### Get Critical Areas
```bash
curl http://localhost:8000/api/food-deserts/critical_areas/
```

## Configuration

### Settings (`settings.py`)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Update with your domain
- `DATABASES`: Configure your database
- `REST_FRAMEWORK`: API configuration
- `INSTALLED_APPS`: Registered applications

### Environment Variables
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Performance Features

- **Database Indexing**: Optimized queries for fast results
- **Pagination**: Handles large datasets efficiently
- **Caching Ready**: DRF caching framework compatible
- **Bulk Operations**: Management commands for batch processing
- **Read-only APIs**: Efficient for dashboard queries

## Security

- **CSRF Protection**: Enabled on all forms
- **Authentication**: Session-based with permission checks
- **Input Validation**: Comprehensive form and model validation
- **SQL Injection Protection**: Django ORM prevents attacks
- **XSS Prevention**: Template auto-escaping enabled

## Testing

Run tests with:
```bash
python manage.py test food_security
```

Test coverage includes:
- Analysis algorithm accuracy
- Data model creation and validation
- API endpoint functionality
- View rendering and context

## Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Update `SECRET_KEY` to a secure random value
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL recommended)
5. Set up static files serving
6. Configure email for notifications
7. Enable HTTPS/SSL
8. Set up database backups
9. Monitor application logs

### Gunicorn Deployment
```bash
gunicorn TidalHack.wsgi:application --bind 0.0.0.0:8000
```

### Docker Support
Create `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Project Structure

```
TidalHack/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── TidalHack/
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Main URL configuration
│   ├── wsgi.py                       # WSGI application
│   └── asgi.py                       # ASGI application
└── food_security/                     # Main application
    ├── models.py                      # Database models
    ├── views.py                       # Views and viewsets
    ├── serializers.py                 # DRF serializers
    ├── urls.py                        # App URL patterns
    ├── forms.py                       # Django forms
    ├── admin.py                       # Admin configuration
    ├── analysis.py                    # ML analysis engine
    ├── tests.py                       # Unit tests
    ├── management/
    │   └── commands/
    │       └── analyze_food_deserts.py  # Management command
    ├── templates/
    │   └── food_security/
    │       ├── base.html              # Base template
    │       ├── index.html             # Dashboard
    │       ├── area_list.html         # Areas listing
    │       ├── area_form.html         # Area form
    │       ├── area_detail.html       # Area details
    │       └── analysis_dashboard.html # Analysis view
    └── static/                        # Static files
```

## Contributing

To contribute improvements:
1. Create a feature branch
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## Future Enhancements

- [ ] Advanced ML models (Random Forest, XGBoost)
- [ ] Predictive modeling for food insecurity trends
- [ ] GIS integration with mapping
- [ ] Real-time data integration from USDA/Census
- [ ] Community impact simulation
- [ ] Cost-benefit analysis tools
- [ ] Multi-language support
- [ ] Mobile application

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [USDA Food Access Data](https://www.ers.usda.gov/webdocs/DataFiles/)
- [Food Security Research](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-hunger/)

## License

This project is provided for educational and community development purposes.

## Support

For issues, questions, or suggestions:
- Check the documentation
- Review API examples
- Examine test cases for usage patterns
- Contact project maintainers

## Acknowledgments

Built with Django and driven by a commitment to food security and community health.

---

**Version**: 1.0.0  
**Last Updated**: February 2024  
**Status**: Production Ready
