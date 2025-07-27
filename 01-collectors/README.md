# Data Collectors

The collectors module extracts raw security data from various tools and APIs, normalizing it for metric generation. Each collector is built around a common framework that handles authentication, data extraction, and storage to multiple destinations.

## Quick Start

```bash
# Set up environment variables (see Configuration section)
cd 01-collectors
python wrapper.py    # Discovers and runs all configured collectors
```

## Architecture

### Core Components

- **`wrapper.py`** - Main entry point that discovers and executes all collectors
- **`collector.py`** - Base class providing common functionality for all collectors  
- **`library.py`** - Shared utilities for logging, AWS operations, and string templating
- **`src_*.py`** - Individual collector implementations for each security tool

### Data Flow

```
Security Tools → Collectors → Multiple Storage Backends
    ↓              ↓              ↓
 API Calls    Environment     Local Files
              Variables       PostgreSQL  
                             AWS S3
                             DuckDB
```

## Supported Security Tools

| Collector | File | Required Environment Variables |
|-----------|------|-------------------------------|
| **CrowdStrike Falcon** | `src_crowdstrike.py` | `FALCON_CLIENT_ID`, `FALCON_SECRET` |
| **Tenable.io** | `src_tenable.py` | `TIO_ACCESS_KEY`, `TIO_SECRET_KEY` |
| **Okta** | `src_okta.py` | `OKTA_TOKEN`, `OKTA_DOMAIN` |
| **Snyk** | `src_snyk.py` | `SNYK_TOKEN` |
| **Microsoft 365** | `src_microsoft365.py` | `MICROSOFT365_*` variables |
| **AWS** | `src_aws.py` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |

> **Complete list**: See [collectors documentation](../00-docs/collectors.md) for all supported tools and their environment variables.

## Configuration

### Environment Variables

Collectors use environment variables for configuration. Create a `.env` file or export variables:

```bash
# Security tool API credentials
FALCON_CLIENT_ID="your_client_id"
FALCON_SECRET="your_secret_key"
TIO_ACCESS_KEY="your_access_key"
TIO_SECRET_KEY="your_secret_key"

# Storage destinations (optional - enables additional storage backends)
STORE_FILE="../data/source/%TAG/%TENANCY.json"
STORE_POSTGRES_HOST="localhost"
STORE_POSTGRES_USER="dbuser"
STORE_POSTGRES_PASSWORD="dbpass"
STORE_POSTGRES_DBNAME="security_metrics"
STORE_AWS_S3_BUCKET="security-data-bucket"
STORE_AWS_S3_KEY="data/%TAG/%YYYY/%MM/%DD/%UUID.json"
STORE_DUCKDB="../data/database.duckdb"
```

### Storage Backends

The collectors support simultaneous storage to multiple destinations:

#### Local Files (Default)
```bash
STORE_FILE="../data/source/%TAG/%TENANCY.json"
```

#### PostgreSQL Database  
```bash
STORE_POSTGRES_HOST="localhost"
STORE_POSTGRES_USER="username"
STORE_POSTGRES_PASSWORD="password"
STORE_POSTGRES_DBNAME="database"
STORE_POSTGRES_PORT="5432"
STORE_POSTGRES_SCHEMA="public"
```

#### AWS S3
```bash
STORE_AWS_S3_BUCKET="your-bucket-name"
STORE_AWS_S3_KEY="data/%TAG/%YYYY/%MM/%DD/%UUID.json"
STORE_AWS_S3_BACKUP="backup/%TAG/%TENANCY.json"
```

#### DuckDB
```bash
STORE_DUCKDB="../data/database.duckdb"
```

### Path Variables

Use these variables in storage paths for dynamic file naming:

| Variable | Description | Example |
|----------|-------------|---------|
| `%TAG` | Data source identifier | `crowdstrike` |
| `%TENANCY` | Tenant/organization identifier | `company` |
| `%UUID` | Unique identifier for this collection | `abc123...` |
| `%YYYY` | Year | `2024` |
| `%MM` | Month | `07` |
| `%DD` | Day | `15` |
| `%hh` | Hour | `14` |
| `%mm` | Minute | `30` |
| `%ss` | Second | `45` |

## Usage Examples

### Basic Extraction
```bash
# Set up environment variables (create .env file)
cd 01-collectors
python wrapper.py    # Discovers and runs all configured collectors
```

### Example Environment Setup
Create an `.env` file with your API credentials:

```bash
# CrowdStrike Falcon API keys
FALCON_CLIENT_ID="xxx"
FALCON_SECRET="yyy"

# Tenable API Keys  
TIO_ACCESS_KEY="xxx"
TIO_SECRET_KEY="yyy"

# Storage destinations (optional)
STORE_FILE="../data/source/%TAG/%TENANCY.json"
STORE_AWS_S3_BUCKET="my-s3-bucket-name"
STORE_AWS_S3_KEY="data/%TAG/%YYYY/%MM/%DD/%UUID.json"
```

Upon completion, you will have a `data` folder populated with JSON files from each configured collector.

### Test Specific Collector
```bash
# Run individual collector
python src_crowdstrike.py

# Check collector metadata
python -c "import src_crowdstrike; print(src_crowdstrike.meta())"
```

### Production Setup
```bash
# Using environment file
cd 01-collectors
export $(cat .env | xargs)
python wrapper.py

# Docker deployment
docker run -d --env-file .env cyber-metrics-collectors
```

## Output Format

All collectors produce standardized JSON output with consistent metadata:

```json
{
  "data": [...],           // Raw extracted data
  "metadata": {
    "tenancy": "company",
    "upload_id": "uuid",
    "timestamp": "2024-07-15T14:30:45Z",
    "tag": "crowdstrike",
    "records": 150
  }
}
```

## State Management & Backup

For production reliability, collectors support state management using AWS S3 backup:

```bash
# Enable backup mechanism
STORE_AWS_S3_BUCKET="backup-bucket"
STORE_AWS_S3_BACKUP="backup/%TAG/%TENANCY.json"
```

When collectors fail to retrieve fresh data, they automatically fall back to the last successful backup from S3.

### Managing State in Production

When all collectors work fine all the time, there is no issue. When they fail, and the API is unable to retrieve data, the metrics will not generate. When running in a Docker-based environment, every time the docker image spins up, none of the data is available. Using AWS S3 as a backup storage will allow the last downloaded data to be available for querying by the metric if required.

To utilize the AWS S3 backup mechanism:

```bash
export STORE_AWS_S3_BUCKET=my-s3-bucket-name
export STORE_AWS_S3_BACKUP='data/%TAG/%TENANCY.json'
```

This provides automatic fallback to the last successful data collection when API calls fail.

## Development

### Adding a New Collector

1. **Create collector file**: `src_newtool.py`
2. **Implement required functions**:
   ```python
   def meta():
       """Return collector metadata"""
       return {
           "tag": "newtool",
           "description": "New Security Tool Collector",
           "env_vars": ["NEWTOOL_API_KEY", "NEWTOOL_URL"]
       }
   
   def main():
       """Main collection logic"""
       collector = Collector()
       
       # Validate environment
       collector.check_env_vars(["NEWTOOL_API_KEY", "NEWTOOL_URL"])
       
       # Extract data
       data = extract_from_newtool()
       
       # Store results  
       collector.store(data)
   ```

3. **Test implementation**:
   ```bash
   python src_newtool.py
   ```

### Base Collector Class

The `Collector` base class provides:

- **Environment validation**: `check_env_vars()`
- **Multi-destination storage**: `store()`
- **Metadata enrichment**: Automatic timestamps, UUIDs, tenancy
- **Error handling**: Graceful failure and backup recovery
- **Logging**: Structured logging with Slack integration

## Monitoring & Troubleshooting

### Logs
Collectors provide structured logging with different severity levels:
- **INFO**: Normal operations
- **WARNING**: Non-critical issues
- **ERROR**: Collection failures
- **CRITICAL**: System-level problems

### Slack Integration
Configure Slack notifications for collection status:
```bash
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Environment variable not set" | Missing API credentials | Check `.env` file or environment variables |
| "Permission denied" | Invalid API keys | Verify credentials with security tool |
| "Network timeout" | API connectivity issues | Check network/firewall settings |
| "Storage failed" | Database/S3 permissions | Verify storage destination credentials |

## Performance

- **Parallel execution**: Collectors run independently and can be parallelized
- **Rate limiting**: Built-in respect for API rate limits
- **Efficient storage**: Bulk operations for database writes
- **Memory management**: Streaming processing for large datasets

## Security

- **Credential management**: Environment-based secrets (recommend external secret management)
- **Data encryption**: In-transit encryption for all API calls
- **Access control**: Principle of least privilege for storage destinations
- **Audit logging**: Complete audit trail of all data collection activities

## Links

- **[Complete Collector List](../00-docs/collectors.md)** - All supported tools and environment variables
- **[Writing a Collector](../00-docs/writing-a-collector.md)** - Developer guide for new collectors