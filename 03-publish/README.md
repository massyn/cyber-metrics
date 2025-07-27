# Results Publisher

The publisher module sends processed security metrics to external systems including databases, APIs, and dashboards. It supports multiple output formats and destinations for integration with existing security infrastructure.

## Quick Start

```bash
cd 03-publish
python publish.py                    # Publish to configured destinations
python publish.py -parquet ../data/custom.parquet # Custom parquet file
```

## Architecture

### Core Components

- **`publish.py`** - Main publishing engine with multi-destination support
- **Output Destinations** - Database, API, and file-based publishing
- **Data Transformation** - Format conversion and schema mapping
- **Error Handling** - Retry logic and failure recovery

### Data Flow

```
Parquet Files → Publisher → Multiple Destinations
     ↓             ↓              ↓
Metric Results  Format        PostgreSQL
Summary Data    Conversion    REST APIs
                             File Systems
                             S3 Buckets
```

## Supported Destinations

### Database Publishing

#### PostgreSQL
```bash
# Environment variables
PUBLISH_POSTGRES_HOST="localhost"
PUBLISH_POSTGRES_USER="publisher"
PUBLISH_POSTGRES_PASSWORD="password"
PUBLISH_POSTGRES_DBNAME="security_metrics"
PUBLISH_POSTGRES_PORT="5432"
PUBLISH_POSTGRES_SCHEMA="public"
```

**Database Schema**:
```sql
-- Summary metrics table
CREATE TABLE metric_summary (
    datestamp DATE,
    metric_id VARCHAR(100),
    title VARCHAR(500),
    category VARCHAR(100),
    business_unit VARCHAR(100),
    team VARCHAR(100),
    location VARCHAR(100),
    totalok INTEGER,
    total INTEGER,
    slo DECIMAL(5,4),
    slo_min DECIMAL(5,4),
    weight DECIMAL(5,2),
    indicator BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Detail results table
CREATE TABLE metric_detail (
    metric_id VARCHAR(100),
    resource VARCHAR(500),
    resource_type VARCHAR(100),
    compliance DECIMAL(5,4),
    detail TEXT,
    business_unit VARCHAR(100),
    team VARCHAR(100),
    location VARCHAR(100),
    datestamp DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### MySQL/MariaDB
```bash
PUBLISH_MYSQL_HOST="localhost"
PUBLISH_MYSQL_USER="publisher"
PUBLISH_MYSQL_PASSWORD="password"
PUBLISH_MYSQL_DATABASE="security_metrics"
PUBLISH_MYSQL_PORT="3306"
```

### API Publishing

#### REST API Endpoints
```bash
# Generic REST API
PUBLISH_API_URL="https://dashboard.company.com/api/metrics"
PUBLISH_API_TOKEN="bearer_token_here"
PUBLISH_API_FORMAT="json"  # json, csv, parquet
```

#### Dashboard API
```bash
# Cyber Dashboard API
PUBLISH_DASHBOARD_URL="https://dashboard.company.com"
PUBLISH_DASHBOARD_TOKEN="api_token"
PUBLISH_DASHBOARD_ORG="organization_id"
```

### File-Based Publishing

#### Local Files
```bash
PUBLISH_FILE_SUMMARY="../output/summary_%YYYY%MM%DD.json"
PUBLISH_FILE_DETAIL="../output/detail_%YYYY%MM%DD.json"
PUBLISH_FILE_FORMAT="json"  # json, csv, parquet
```

#### AWS S3
```bash
PUBLISH_S3_BUCKET="metrics-output-bucket"
PUBLISH_S3_KEY_SUMMARY="metrics/summary/%YYYY/%MM/%DD/summary.parquet"
PUBLISH_S3_KEY_DETAIL="metrics/detail/%YYYY/%MM/%DD/detail.parquet"
PUBLISH_S3_REGION="us-east-1"
```

#### Azure Blob Storage
```bash
PUBLISH_AZURE_ACCOUNT="storageaccount"
PUBLISH_AZURE_CONTAINER="metrics"
PUBLISH_AZURE_KEY_SUMMARY="summary/%YYYY/%MM/%DD/summary.json"
PUBLISH_AZURE_SAS_TOKEN="sas_token_here"
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-h` | Display help information | |
| `-parquet <path>` | Specify input parquet file | `python publish.py -parquet ../data/metrics.parquet` |
| `-summary <path>` | Specify summary parquet file | `python publish.py -summary ../data/summary.parquet` |
| `-detail <path>` | Specify detail parquet file | `python publish.py -detail ../data/detail.parquet` |
| `-destination <dest>` | Publish to specific destination only | `python publish.py -destination postgres` |
| `-format <format>` | Output format (json, csv, parquet) | `python publish.py -format csv` |
| `-dryrun` | Test mode - validate without publishing | `python publish.py -dryrun` |

## Configuration

### Environment-Based Configuration

Create a `.env` file or export environment variables:

```bash
# Database publishing
PUBLISH_POSTGRES_HOST="db.company.com"
PUBLISH_POSTGRES_USER="metrics_publisher"
PUBLISH_POSTGRES_PASSWORD="secure_password"
PUBLISH_POSTGRES_DBNAME="security_metrics"

# API publishing  
PUBLISH_API_URL="https://api.company.com/metrics"
PUBLISH_API_TOKEN="Bearer xyz123..."

# File publishing
PUBLISH_FILE_SUMMARY="../output/summary_%YYYY%MM%DD.json"
PUBLISH_FILE_DETAIL="../output/detail_%YYYY%MM%DD.json"

# S3 publishing
PUBLISH_S3_BUCKET="company-security-metrics"
PUBLISH_S3_KEY_SUMMARY="data/summary/%YYYY/%MM/%DD/%UUID.parquet"
```

### Multiple Destinations

Publishers can simultaneously send data to multiple destinations:

```bash
# Enable multiple outputs
PUBLISH_POSTGRES_HOST="db.company.com"    # Database
PUBLISH_API_URL="https://api.company.com" # REST API  
PUBLISH_S3_BUCKET="backup-bucket"         # S3 backup
PUBLISH_FILE_SUMMARY="../local/summary.json" # Local file
```

## Data Formats

### JSON Output
```json
{
  "summary": [
    {
      "datestamp": "2024-07-15",
      "metric_id": "access_mfa",
      "title": "Access Control - Multi-Factor Authentication",
      "category": "Identity Management", 
      "business_unit": "Engineering",
      "team": "Platform",
      "location": "North America",
      "totalok": 143,
      "total": 150,
      "slo": 0.95,
      "slo_min": 0.90,
      "weight": 1.0,
      "indicator": true
    }
  ],
  "detail": [
    {
      "metric_id": "access_mfa",
      "resource": "user001@company.com",
      "resource_type": "user",
      "compliance": 1,
      "detail": "MFA enabled and configured",
      "business_unit": "Engineering",
      "team": "Platform", 
      "location": "North America",
      "datestamp": "2024-07-15"
    }
  ]
}
```

### CSV Output
```csv
# summary.csv
datestamp,metric_id,title,category,business_unit,totalok,total,slo,slo_min
2024-07-15,access_mfa,Access Control - MFA,Identity Management,Engineering,143,150,0.95,0.90

# detail.csv  
metric_id,resource,resource_type,compliance,detail,business_unit,datestamp
access_mfa,user001@company.com,user,1,MFA enabled and configured,Engineering,2024-07-15
```

## Usage Examples

### Basic Publishing
```bash
# Publish to all configured destinations
cd 03-publish
python publish.py
```

### Specific Destination
```bash
# Publish to PostgreSQL only
python publish.py -destination postgres

# Publish to S3 only
python publish.py -destination s3
```

### Custom Data Source
```bash
# Publish custom parquet file
python publish.py -parquet /path/to/custom/metrics.parquet

# Publish specific summary and detail files
python publish.py -summary ../data/summary.parquet -detail ../data/detail.parquet
```

### Format Conversion
```bash
# Convert to CSV format
python publish.py -format csv -destination file

# Convert to JSON for API
python publish.py -format json -destination api
```

### Testing
```bash
# Dry run - validate configuration without publishing
python publish.py -dryrun

# Test specific destination
python publish.py -destination postgres -dryrun
```

## Error Handling & Retry Logic

### Automatic Retry
The publisher includes automatic retry logic for transient failures:

```python
# Configurable retry settings
PUBLISH_RETRY_ATTEMPTS=3       # Number of retry attempts
PUBLISH_RETRY_DELAY=5          # Delay between retries (seconds)
PUBLISH_RETRY_BACKOFF=2        # Exponential backoff multiplier
```

### Failure Recovery
- **Database failures**: Automatic transaction rollback and retry
- **API failures**: HTTP error handling with exponential backoff
- **Network issues**: Connection timeout and retry logic
- **Authentication**: Token refresh and re-authentication

### Error Logging
Comprehensive error logging includes:
- **Destination-specific errors**: Database, API, file system issues
- **Data validation errors**: Schema mismatches, data type errors
- **Network errors**: Timeouts, connection failures
- **Authentication errors**: Token expiration, permission issues

## Monitoring & Alerting

### Metrics
Publisher tracks key metrics:
- **Records published**: Count of successful publications per destination
- **Error rates**: Failed publications by error type
- **Performance**: Publishing duration and throughput
- **Data volumes**: Record counts and data sizes

### Health Checks
Built-in health checks validate:
- **Destination connectivity**: Database, API, storage accessibility
- **Authentication**: Valid credentials and permissions
- **Data integrity**: Schema validation and data consistency
- **Performance**: Publishing duration within SLA thresholds

### Slack Integration
Configure Slack notifications for publishing status:
```bash
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
SLACK_CHANNEL="#security-metrics"
```

## Security

### Credential Management
- **Environment variables**: Store credentials securely
- **Secret management**: Integration with HashiCorp Vault, AWS Secrets Manager
- **Principle of least privilege**: Minimal required permissions
- **Credential rotation**: Regular rotation of API tokens and database passwords

### Data Protection
- **Encryption in transit**: TLS for all network communications
- **Encryption at rest**: Encrypted storage for sensitive data
- **Data masking**: Optional PII masking for compliance
- **Access logging**: Complete audit trail of data access

## Performance Optimization

### Batch Processing
- **Bulk operations**: Efficient batch inserts for databases
- **Parallel publishing**: Concurrent publishing to multiple destinations
- **Memory management**: Streaming processing for large datasets
- **Connection pooling**: Efficient database connection management

### Scalability
- **Horizontal scaling**: Support for multiple publisher instances
- **Load balancing**: Distribute publishing load across instances
- **Queue management**: Message queues for reliable processing
- **Resource monitoring**: CPU, memory, and network usage tracking

## Integration Examples

### CI/CD Pipeline
```bash
#!/bin/bash
# Automated publishing in CI/CD
cd 03-publish

# Publish to staging
PUBLISH_POSTGRES_HOST="staging-db.company.com" python publish.py

# Publish to production (on main branch)
if [ "$BRANCH" = "main" ]; then
    PUBLISH_POSTGRES_HOST="prod-db.company.com" python publish.py
fi
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

COPY 03-publish/ /app/
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "publish.py"]
```

### Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: metrics-publisher
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: publisher
            image: company/metrics-publisher:latest
            env:
            - name: PUBLISH_POSTGRES_HOST
              valueFrom:
                secretKeyRef:
                  name: postgres-credentials
                  key: host
```

## Links

- **[Dashboard Integration](../04-dashboard/README.md)** - Dashboard publishing setup