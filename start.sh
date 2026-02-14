#!/bin/bash
# Quick start script for Collider Platform

set -e

echo "🚀 Collider Platform - Quick Start"
echo "=================================="
echo ""

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker-compose down -v 2>/dev/null || true
echo ""

# Start services
echo "🏗️  Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
echo "   This may take 30-60 seconds on first run..."
echo ""

# Wait for PostgreSQL
echo "   Waiting for PostgreSQL..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U physics &> /dev/null; then
        echo "   ✅ PostgreSQL is ready"
        break
    fi
    sleep 2
done

# Wait for Kafka
echo "   Waiting for Kafka..."
for i in {1..30}; do
    if docker-compose logs kafka 2>&1 | grep -q "Kafka Server started" ; then
        echo "   ✅ Kafka is ready"
        break
    fi
    sleep 2
done

# Wait for API Gateway
echo "   Waiting for API Gateway..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health &> /dev/null; then
        echo "   ✅ API Gateway is ready"
        break
    fi
    sleep 2
done

echo ""
echo "🎉 Collider Platform is ready!"
echo ""
echo "📍 Access Points:"
echo "   Frontend:     http://localhost:8080"
echo "   API Docs:     http://localhost:8000/docs"
echo "   API Health:   http://localhost:8000/health"
echo ""
echo "📊 Useful Commands:"
echo "   View logs:           docker-compose logs -f"
echo "   Stop services:       docker-compose down"
echo "   Restart services:    docker-compose restart"
echo "   View events in DB:   docker-compose exec postgres psql -U physics -d collider_db -c 'SELECT COUNT(*) FROM events;'"
echo ""
echo "🔍 Check Status:"
echo "   Service status:      docker-compose ps"
echo ""
echo "Happy hacking! 🚀⚛️"
