# Quick Start Guide

## Food Security & Desert Analysis System

Get up and running in 5 minutes!

### Prerequisites
- Python 3.8 or higher
- Git
- Terminal/Command prompt

### Step 1: Navigate to Project
```bash
cd /path/to/26SprTidalHack
```

### Step 2: Run Automated Setup (Recommended)
```bash
bash setup.sh
```

**Or manual setup:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Navigate to Django project
cd TidalHack

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

### Step 3: Start Server
```bash
python manage.py runserver
```

### Step 4: Access the Application

**Web Interface**:
- Dashboard: http://localhost:8000/
- Food Deserts: http://localhost:8000/areas/
- Add Area: http://localhost:8000/areas/new/
- Admin: http://localhost:8000/admin/

**API**:
- Food Deserts API: http://localhost:8000/api/food-deserts/
- Analysis API: http://localhost:8000/api/analysis-results/
- Recommendations API: http://localhost:8000/api/recommendations/

### Step 5: Test the System

#### Via Web Interface:
1. Go to http://localhost:8000/areas/new/
2. Fill in sample data for a food desert area
3. Submit the form
4. Click "Analyze" to generate analysis
5. View results in the analysis dashboard

#### Via API:
```bash
# Create an area
curl -X POST http://localhost:8000/api/food-deserts/ \
  -H "Content-Type: application/json" \
  -d '{
    "area_name": "Downtown",
    "city": "Springfield",
    "state": "IL",
    "latitude": 39.78,
    "longitude": -89.65,
    "population": 5000,
    "poverty_rate": 25,
    "median_income": 35000,
    "distance_to_grocery": 3,
    "grocery_store_count": 1,
    "vehicle_ownership_rate": 60,
    "unemployment_rate": 8,
    "food_insecurity_rate": 18
  }'

# Analyze the area (ID = 1)
curl -X POST http://localhost:8000/api/food-deserts/1/analyze/

# Get analysis results
curl http://localhost:8000/api/analysis-results/
```

### Step 6: Explore Features

**Dashboard**:
- View statistics and recent analyses
- Monitor food insecurity severity levels
- Track population at risk

**Food Deserts**:
- Browse all registered areas
- View detailed area information
- Compare multiple areas

**Analysis**:
- View severity scores and components
- Review generated recommendations
- Plan interventions with cost estimates

**Admin Panel**:
- Manage areas and analyses
- View comprehensive data
- Export reports

### Useful Commands

```bash
# Run tests
python manage.py test food_security

# Analyze specific area
python manage.py analyze_food_deserts --area-id=1

# Analyze all areas
python manage.py analyze_food_deserts --all

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files (production)
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Clear database (development only!)
python manage.py flush

# Open Django shell
python manage.py shell
```

### Sample Data Entry

When adding a new food desert area, you'll need:

**Location**:
- Area name: e.g., "Downtown Community"
- Latitude: e.g., 39.7817
- Longitude: e.g., -89.6501
- Address: Full address
- City, State, Zip: Location info

**Demographics**:
- Population: Number of residents
- Poverty rate: % in poverty (0-100)
- Median income: Annual household income
- Unemployment rate: % unemployed

**Food Access**:
- Distance to grocery: Miles to nearest store
- Grocery store count: Number of stores
- Farmers markets: Number available
- Food assistance programs: Number of programs

**Infrastructure**:
- Has public transit: Yes/No
- Vehicle ownership rate: % with vehicles

**Health**:
- Food insecurity rate: % without consistent food access
- Health problems rate: % with nutrition-related issues

### Understanding Results

**Severity Levels**:
- 🔴 **Critical** (75-100): Immediate action required
- 🟠 **Severe** (60-74): High priority intervention
- 🟡 **Moderate** (40-59): Medium-term planning
- 🟢 **Mild** (0-39): Monitoring needed

**Recommendations**:
- Prioritized by impact and feasibility
- Include costs and timelines
- Grouped by solution category
- Include implementation steps

**Scores** (Higher = Better):
- Accessibility Score: Access to food
- Income Score: Economic resources
- Infrastructure Score: Transportation access
- Food Insecurity: Lower is better

### Troubleshooting

**Issue**: Port 8000 already in use
```bash
python manage.py runserver 8001
```

**Issue**: Database errors
```bash
python manage.py migrate
```

**Issue**: Static files not loading
```bash
python manage.py collectstatic
```

**Issue**: Admin password forgotten
```bash
python manage.py changepassword admin
```

### Next Steps

1. **Read Documentation**:
   - See README.md for overview
   - See SYSTEM_DOCUMENTATION.md for complete guide
   - See IMPLEMENTATION_SUMMARY.md for technical details

2. **Customize**:
   - Update templates/styles
   - Add custom analysis rules
   - Integrate with external data

3. **Deploy**:
   - Configure PostgreSQL database
   - Set up Gunicorn + Nginx
   - Deploy to cloud provider

4. **Extend**:
   - Add advanced ML models
   - Integrate GIS mapping
   - Build mobile app

### Getting Help

- **Documentation**: See SYSTEM_DOCUMENTATION.md
- **Examples**: Check test cases in tests.py
- **API Docs**: Available at /api/ in browser
- **Django Docs**: https://docs.djangoproject.com/

### Common URLs

| Page | URL |
|------|-----|
| Dashboard | http://localhost:8000/ |
| All Areas | http://localhost:8000/areas/ |
| Add Area | http://localhost:8000/areas/new/ |
| Area Details | http://localhost:8000/areas/{id}/ |
| Analysis | http://localhost:8000/areas/{id}/analysis/ |
| Admin | http://localhost:8000/admin/ |
| API | http://localhost:8000/api/ |

### Environment Variables

Create a `.env` file:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### System Requirements

- **RAM**: 1GB minimum (2GB recommended)
- **Disk**: 500MB for installation
- **CPU**: Single core minimum
- **DB**: SQLite (included) or PostgreSQL

### Success!

You now have a fully functional food security analysis system!

Start analyzing food deserts and generating actionable recommendations.

---

**Need Help?** Check SYSTEM_DOCUMENTATION.md
**Want Details?** See IMPLEMENTATION_SUMMARY.md
**Examples?** Browse the code and comments

Happy analyzing! 🚀
