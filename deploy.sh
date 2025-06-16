#!/bin/bash

# NBFC Django API - Quick Deployment Script
# Usage: ./deploy.sh [NEW_IP_ADDRESS]

set -e

echo "🚀 NBFC Django API Deployment Script"
echo "======================================"

# Get the new IP address
if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <NEW_IP_ADDRESS>"
    echo "Example: ./deploy.sh 40.90.224.166"
    exit 1
fi

NEW_IP="$1"
echo "📍 Configuring for IP: $NEW_IP"

# Backup existing .env if it exists
if [ -f .env ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "📄 Backed up existing .env file"
fi

# Create new .env from template
cp .env.example .env

# Update the HOST_IP in .env
sed -i "s/HOST_IP=.*/HOST_IP=$NEW_IP/" .env

echo "✅ Updated configuration files"
echo "🏗️  Building and starting services..."

# Stop existing containers
docker compose down

# Build and start
docker compose up -d --build

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo ""
    echo "🌐 Access your application:"
    echo "   API: http://$NEW_IP:8000"
    echo "   Admin: http://$NEW_IP/admin"
    echo "   Frontend: http://$NEW_IP:3000 (when available)"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Create superuser: docker compose exec web python manage.py createsuperuser"
    echo "   2. Test API: curl http://$NEW_IP:8000/api/"
else
    echo "❌ Deployment failed. Check logs:"
    echo "   docker compose logs"
fi
