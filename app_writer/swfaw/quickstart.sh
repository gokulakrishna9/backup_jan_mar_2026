#!/bin/bash

# Quick Start Script for swfaw_v2
# Generates a sample Spring WebFlux application

echo "🚀 Spring WebFlux Application Writer v2 - Quick Start"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -q pydantic jinja2

echo ""
echo "🔨 Generating Spring WebFlux application from sample..."
python main.py --input sample_database_definition.json --output ../generated-course-app

echo ""
echo "✅ Generation complete!"
echo ""
echo "📋 Next steps:"
echo "   1. cd ../generated-course-app"
echo "   2. mvn clean install"
echo "   3. mvn spring-boot:run"
echo "   4. Open http://localhost:8080/swagger-ui.html"
echo ""
echo "📚 For more information, see USAGE_GUIDE.md"
