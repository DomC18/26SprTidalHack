# Food Security & Desert Analysis System

A sophisticated AI/ML-powered Django application that analyzes food desert areas and generates data-driven recommendations to improve food security and community access to nutritious food.

## 🎯 Mission

Empower communities and organizations to identify, analyze, and solve food desert challenges through intelligent data analysis and actionable recommendations.

## ✨ Key Features

### 🔬 Advanced Analysis Engine
- **Multi-factor Assessment** of 13+ food security indicators
- **Machine Learning Algorithms** for intelligent scoring
- **Severity Classification** (Critical, Severe, Moderate, Mild)
- **Component Analysis** (Accessibility, Income, Infrastructure, Health)

### 💡 Smart Recommendations
- **8 Solution Categories** tailored to area challenges
- **Prioritized Actions** ranked by impact and feasibility
- **Short & Long-term Plans** with realistic timelines
- **Cost Estimates** for budgeting and planning

### 📊 Interactive Dashboard
- Real-time analytics and statistics
- Visual severity assessment
- Impact metrics and population data
- Quick-access analysis tools

### 🛠️ Comprehensive Tools
- **REST API** for programmatic access
- **Web Interface** for user-friendly data entry
- **Django Admin** for management
- **Management Commands** for batch operations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 6.0.2
- pip or conda

### Installation

1. **Navigate to project**:
```bash
cd /path/to/26SprTidalHack
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
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

5. **Create admin user**:
```bash
python manage.py createsuperuser
```

6. **Start server**:
```bash
python manage.py runserver
```

Visit `http://localhost:8000/` to access the application!

## 📌 Project Structure

```
TidalHack/
├── manage.py                 # Django CLI
├── requirements.txt          # Dependencies
├── SYSTEM_DOCUMENTATION.md   # Detailed documentation
├── TidalHack/               # Project configuration
│   ├── settings.py          # App configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
└── food_security/           # Main application
    ├── models.py            # Data models
    ├── views.py             # Views & APIs
    ├── serializers.py       # DRF serializers
    ├── urls.py              # URL patterns
    ├── forms.py             # Django forms
    ├── admin.py             # Admin panel
    ├── analysis.py          # ML analysis engine
    ├── tests.py             # Unit tests
    ├── management/          # CLI commands
    ├── templates/           # HTML templates
    └── static/              # CSS, JS, images
```

## 📚 Usage Guide

### Web Interface

**Dashboard** (`/`)
- Overview of all food desert areas
- Statistics on severity and population impact
- Recent analysis history

**Food Deserts** (`/areas/`)
- Browse all registered food desert areas
- Filter and search by location, severity, or metrics
- Quick actions for analysis

**Add New Area** (`/areas/new/`)
- Enter comprehensive data about an area
- 20+ data fields covering location, demographics, food access, infrastructure
- Automatic validation and feedback

**Analysis Dashboard** (`/areas/<id>/analysis/`)
- Detailed analysis results with severity scores
- Categorized recommendations
- Action plans and implementation timelines
- Cost and feasibility assessments

### REST API

**Food Desert Areas**
```bash
GET    /api/food-deserts/                    # List areas
POST   /api/food-deserts/                    # Create area
GET    /api/food-deserts/{id}/               # Get area
PUT    /api/food-deserts/{id}/               # Update area
POST   /api/food-deserts/{id}/analyze/       # Analyze area
GET    /api/food-deserts/critical_areas/     # Critical areas
```

**Quick Analysis** (no storage)
```bash
POST   /api/quick-analysis/
```

**Analysis Results & Recommendations**
```bash
GET    /api/analysis-results/                # All results
GET    /api/analysis-results/by_severity/?severity=critical
GET    /api/recommendations/                 # All recommendations
GET    /api/recommendations/by_category/?category=retail
```

### Management Commands

Analyze specific area:
```bash
python manage.py analyze_food_deserts --area-id=1
```

Analyze all areas:
```bash
python manage.py analyze_food_deserts --all
```

## 🔍 How It Works

### 1. Data Input
Enter comprehensive data about a food desert area:
- Geographic location and demographics
- Food retail availability and accessibility
- Transportation infrastructure
- Income and poverty levels
- Health and nutrition indicators

### 2. Intelligent Analysis
The system analyzes data across four domains:
- **Accessibility Score**: Distance to food, store availability
- **Income Score**: Poverty rates, economic resources
- **Infrastructure Score**: Transit, vehicle ownership
- **Health Score**: Nutrition-related health impacts

### 3. Severity Assessment
Calculates an overall Food Insecurity Score (0-100):
- **0-20**: Mild challenges
- **20-40**: Moderate issues
- **40-60**: Severe problems
- **60-100**: Critical situation

### 4. Smart Recommendations
Generates prioritized solutions across 8 categories:
- Retail development (grocery stores, food hubs)
- Transportation programs (shuttles, transit)
- Income support (jobs, training)
- Food assistance expansion
- Community education
- Local food production
- Policy advocacy
- Technology solutions

### 5. Implementation Planning
Provides for each recommendation:
- Detailed description and rationale
- Expected impact and outcomes
- Step-by-step implementation guide
- Resource requirements
- Success metrics
- Timeline (months)
- Cost estimates

## 🎯 Use Cases

1. **Community Planning**: Assess local food security and plan interventions
2. **Grant Applications**: Provide data-driven evidence for funding requests
3. **Policy Making**: Inform food security policy with comprehensive analysis
4. **Comparative Analysis**: Compare multiple areas to prioritize resources
5. **Impact Tracking**: Monitor changes after implementing solutions
6. **Advocacy**: Build compelling cases for food security initiatives

## 📊 Data Models

**FoodDesertArea** - Tracks area characteristics
- Location (coordinates, address)
- Demographics (population, poverty, income)
- Food access metrics
- Infrastructure details
- Health indicators

**AnalysisResult** - Stores analysis outcomes
- Severity level
- Component scores
- Recommendations
- Action plans
- Timelines and costs

**Recommendation** - Individual solutions
- Category and title
- Detailed description
- Priority and feasibility
- Cost and timeline
- Success metrics

## 🔧 Development

### Running Tests
```bash
python manage.py test food_security
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin Panel
Access at `/admin/` with superuser credentials

## 🌐 API Examples

### Create an Area
```bash
curl -X POST http://localhost:8000/api/food-deserts/ \
  -H "Content-Type: application/json" \
  -d '{
    "area_name":"Community Zone",
    "city":"Springfield",
    "state":"IL",
    "latitude":39.78,
    "longitude":-89.65,
    "population":5000,
    "poverty_rate":25,
    "median_income":35000,
    "distance_to_grocery":3,
    "grocery_store_count":1,
    "vehicle_ownership_rate":60,
    "unemployment_rate":8,
    "food_insecurity_rate":18
  }'
```

### Analyze an Area
```bash
curl -X POST http://localhost:8000/api/food-deserts/1/analyze/
```

### Get Critical Areas
```bash
curl http://localhost:8000/api/food-deserts/critical_areas/
```

## 📚 Documentation

For comprehensive documentation, see [SYSTEM_DOCUMENTATION.md](SYSTEM_DOCUMENTATION.md)

- Complete feature overview
- Detailed installation guide
- Database schema documentation
- API reference
- Algorithm explanation
- Deployment instructions
- Contributing guidelines

## 🚀 Deployment

### Requirements
- Python 3.8+
- PostgreSQL (recommended) or SQLite
- Web server (Gunicorn, uWSGI)
- Reverse proxy (Nginx)

### Quick Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn TidalHack.wsgi:application --bind 0.0.0.0:8000
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Advanced ML models (Random Forest, Neural Networks)
- Predictive analytics features
- GIS integration with mapping
- Real-time data feeds
- Mobile application
- Multi-language support

## 📝 License

This project is provided for educational and community development purposes.

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [USDA Food Access Data](https://www.ers.usda.gov/)
- [Food Security Research](https://www.ers.usda.gov/topics/food-nutrition-assistance/)

## 📧 Support

For questions, issues, or suggestions:
1. Check SYSTEM_DOCUMENTATION.md
2. Review test cases for examples
3. Check existing GitHub issues
4. Create a new issue with details

## 🌟 Acknowledgments

Built with Django, driven by a commitment to food security and community health.

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: February 2024
