# Deployment Guide

## Overview

This guide covers deploying the Cosmere API to production environments. The API is designed to be deployed using Docker and can run on various cloud platforms.

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database (version 12 or higher)
- Redis (optional, for caching)
- Domain name and SSL certificate
- Cloud platform account (AWS, GCP, Azure, etc.)

## Environment Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name
DATABASE_TEST_URL=postgresql://username:password@host:port/test_database_name

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Cosmere API
VERSION=1.0.0
DESCRIPTION=Comprehensive API for Brandon Sanderson's Cosmere universe

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]

# Redis (Optional)
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# Health Checks
HEALTH_CHECK_INTERVAL=30
```

### Production Environment Variables

For production, use environment-specific variables:

```bash
# Production Database
DATABASE_URL=postgresql://prod_user:prod_password@prod_host:5432/cosmere_prod

# Production Redis
REDIS_URL=redis://prod_redis_host:6379

# Production CORS
BACKEND_CORS_ORIGINS=["https://yourdomain.com", "https://api.yourdomain.com"]

# Production Security
SECRET_KEY=your-production-secret-key
```

## Docker Deployment

### 1. Build the Docker Image

```bash
# Build the production image
docker build -t cosmere-api:latest .

# Tag for registry
docker tag cosmere-api:latest your-registry/cosmere-api:latest
```

### 2. Docker Compose for Production

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  api:
    image: cosmere-api:latest
    container_name: cosmere-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://cosmere_user:password@db:5432/cosmere_prod
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - BACKEND_CORS_ORIGINS=${BACKEND_CORS_ORIGINS}
    depends_on:
      - db
      - redis
    networks:
      - cosmere-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15
    container_name: cosmere-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=cosmere_prod
      - POSTGRES_USER=cosmere_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - cosmere-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U cosmere_user -d cosmere_prod"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    container_name: cosmere-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - cosmere-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    container_name: cosmere-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    networks:
      - cosmere-network

volumes:
  postgres_data:
  redis_data:

networks:
  cosmere-network:
    driver: bridge
```

### 3. Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # CORS headers
            add_header Access-Control-Allow-Origin $http_origin always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
            add_header Access-Control-Allow-Credentials true always;
            
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin $http_origin;
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
                add_header Access-Control-Allow-Headers "Content-Type, Authorization";
                add_header Access-Control-Allow-Credentials true;
                add_header Content-Length 0;
                add_header Content-Type text/plain;
                return 204;
            }
        }

        # Health check
        location /health {
            proxy_pass http://api/api/v1/health/;
            access_log off;
        }

        # Static files (if any)
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### 4. Database Initialization

Create `init.sql`:

```sql
-- Create database and user
CREATE DATABASE cosmere_prod;
CREATE USER cosmere_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE cosmere_prod TO cosmere_user;

-- Create test database
CREATE DATABASE cosmere_test;
GRANT ALL PRIVILEGES ON DATABASE cosmere_test TO cosmere_user;
```

### 5. Deploy with Docker Compose

```bash
# Start the services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f api

# Run database migrations
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

## Cloud Platform Deployment

### AWS Deployment

#### 1. ECS Fargate

Create `task-definition.json`:

```json
{
  "family": "cosmere-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "cosmere-api",
      "image": "your-registry/cosmere-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://user:password@rds-endpoint:5432/cosmere"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://elasticache-endpoint:6379"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cosmere-api",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/api/v1/health/ || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3
      }
    }
  ]
}
```

#### 2. Application Load Balancer

```yaml
# AWS CloudFormation template snippet
Resources:
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: cosmere-api-alb
      Scheme: internet-facing
      Type: application
      SecurityGroups:
        - !Ref ALBSecurityGroup
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2

  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: cosmere-api-tg
      Port: 8000
      Protocol: HTTP
      VpcId: !Ref VPC
      TargetType: ip
      HealthCheckPath: /api/v1/health/
      HealthCheckIntervalSeconds: 30
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
```

### Google Cloud Platform

#### 1. Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy cosmere-api \
  --image gcr.io/your-project/cosmere-api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars DATABASE_URL=postgresql://user:password@host:5432/cosmere
```

#### 2. Cloud SQL

```bash
# Create Cloud SQL instance
gcloud sql instances create cosmere-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=your-password

# Create database
gcloud sql databases create cosmere_prod --instance=cosmere-db
```

### Azure

#### 1. Container Instances

```bash
# Deploy to Azure Container Instances
az container create \
  --resource-group myResourceGroup \
  --name cosmere-api \
  --image your-registry/cosmere-api:latest \
  --dns-name-label cosmere-api \
  --ports 8000 \
  --environment-variables DATABASE_URL=postgresql://user:password@host:5432/cosmere
```

## Database Setup

### 1. Run Migrations

```bash
# Apply migrations
alembic upgrade head

# Verify migration status
alembic current
alembic history
```

### 2. Seed Data (Optional)

```bash
# Run data import script
python scripts/import_data.py
```

## Monitoring and Logging

### 1. Application Monitoring

```python
# Add to main.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
```

### 2. Health Checks

```bash
# Test health endpoint
curl -f http://localhost:8000/api/v1/health/

# Test database health
curl -f http://localhost:8000/api/v1/health/db

# Test detailed health
curl -f http://localhost:8000/api/v1/health/detailed
```

### 3. Metrics Collection

```python
# Add Prometheus metrics
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Add middleware to collect metrics
@app.middleware("http")
async def collect_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Security Considerations

### 1. Environment Variables

- Never commit `.env` files to version control
- Use secrets management services (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)
- Rotate secrets regularly

### 2. Network Security

- Use VPCs and security groups to restrict access
- Implement proper firewall rules
- Use HTTPS/TLS for all communications

### 3. API Security

- Implement rate limiting
- Add authentication/authorization
- Validate all inputs
- Use CORS properly

### 4. Database Security

- Use strong passwords
- Enable SSL/TLS connections
- Regular security updates
- Backup encryption

## Backup and Recovery

### 1. Database Backups

```bash
# PostgreSQL backup
pg_dump -h host -U user -d cosmere_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql
```

### 2. Application Backups

```bash
# Backup application data
tar -czf app_backup_$(date +%Y%m%d_%H%M%S).tar.gz /app/data/

# Backup configuration
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
```

## Scaling

### 1. Horizontal Scaling

```yaml
# Docker Compose with multiple instances
services:
  api:
    image: cosmere-api:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### 2. Load Balancing

```nginx
# Nginx load balancer configuration
upstream api {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}
```

### 3. Database Scaling

- Use read replicas for read-heavy workloads
- Implement connection pooling
- Consider database sharding for large datasets

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database connectivity
   docker-compose exec api python -c "from app.core.database import engine; print(engine.execute('SELECT 1').scalar())"
   ```

2. **Migration Issues**
   ```bash
   # Check migration status
   docker-compose exec api alembic current
   
   # Rollback if needed
   docker-compose exec api alembic downgrade -1
   ```

3. **Memory Issues**
   ```bash
   # Check container memory usage
   docker stats cosmere-api
   
   # Increase memory limits
   docker-compose up -d --scale api=2
   ```

4. **Log Analysis**
   ```bash
   # View application logs
   docker-compose logs -f api
   
   # Search for errors
   docker-compose logs api | grep ERROR
   ```

### Performance Optimization

1. **Database Optimization**
   - Add indexes for frequently queried fields
   - Optimize slow queries
   - Use connection pooling

2. **Caching**
   - Enable Redis caching
   - Implement response caching
   - Use CDN for static assets

3. **Application Optimization**
   - Enable gzip compression
   - Optimize database queries
   - Use async operations where possible

## Maintenance

### Regular Tasks

1. **Security Updates**
   ```bash
   # Update base images
   docker pull postgres:15
   docker pull redis:7-alpine
   
   # Rebuild application
   docker-compose build --no-cache
   ```

2. **Database Maintenance**
   ```sql
   -- Vacuum database
   VACUUM ANALYZE;
   
   -- Update statistics
   ANALYZE;
   ```

3. **Log Rotation**
   ```bash
   # Rotate application logs
   logrotate /etc/logrotate.d/cosmere-api
   ```

4. **Backup Verification**
   ```bash
   # Test backup restoration
   psql -h host -U user -d test_db < backup_file.sql
   ```

This deployment guide provides a comprehensive approach to deploying the Cosmere API in production environments. Adjust the configurations based on your specific requirements and infrastructure. 