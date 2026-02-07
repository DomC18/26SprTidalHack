#!/bin/bash

# Food Security Analysis System - Setup Script
# This script sets up the development environment

echo "🚀 Food Security & Desert Analysis System Setup"
echo "=================================================="

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install requirements
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Navigate to TidalHack
cd TidalHack

# Run migrations
echo -e "${BLUE}Running database migrations...${NC}"
python manage.py migrate
echo -e "${GREEN}✓ Database migrations completed${NC}"

# Collect static files
echo -e "${BLUE}Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

# Create superuser prompt
echo ""
echo -e "${BLUE}Creating superuser...${NC}"
python manage.py createsuperuser

echo ""
echo -e "${GREEN}=================================================="
echo "✓ Setup completed successfully!"
echo -e "==================================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Start the development server with:"
echo "   python manage.py runserver"
echo ""
echo "2. Access the application at:"
echo "   http://localhost:8000/"
echo ""
echo "3. Access the admin panel at:"
echo "   http://localhost:8000/admin/"
echo ""
echo -e "${BLUE}API Endpoints:${NC}"
echo "- Food Deserts: http://localhost:8000/api/food-deserts/"
echo "- Analysis Results: http://localhost:8000/api/analysis-results/"
echo "- Recommendations: http://localhost:8000/api/recommendations/"
echo ""
echo -e "${BLUE}Management Commands:${NC}"
echo "- Analyze specific area: python manage.py analyze_food_deserts --area-id=1"
echo "- Analyze all areas: python manage.py analyze_food_deserts --all"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "- See README.md for quick reference"
echo "- See SYSTEM_DOCUMENTATION.md for comprehensive guide"
