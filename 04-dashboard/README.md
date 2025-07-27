# Interactive Security Dashboard

A production-ready web dashboard for visualizing and analyzing cybersecurity metrics. Built with vanilla JavaScript for simplicity and performance, providing executive overview, detailed scorecards, and drill-down analysis capabilities.

## Features

- **Overview Dashboard**: Executive summary with aggregated metrics and trend charts
- **Scorecard View**: Tabular display of all metrics with sortable columns and sparkline trends  
- **Detail View**: In-depth analysis of individual metrics with evidence tables
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Filter Persistence**: Maintains filter state across all dashboard views
- **Data Caching**: Automatically caches JSON data for 1 hour to improve performance

## Project Structure

```
04-dashboard/
├── src/
│   ├── js/                    # JavaScript modules
│   │   ├── app.js            # Main application entry point
│   │   ├── data-loader.js    # JSON data loading and caching
│   │   ├── filters.js        # Filter management across views
│   │   ├── chart-manager.js  # Chart.js chart rendering
│   │   ├── scorecard.js      # Scorecard table and sparklines
│   │   └── detail.js         # Detail view and evidence table
│   ├── json/                 # Data files (see schemas below)
│   │   ├── summary.json      # Aggregated metric summaries
│   │   └── detail.json       # Individual resource compliance records
│   ├── styles/
│   │   └── main.css          # Application styling
│   └── index.html            # Main dashboard page
├── index.html                # Entry point (redirects to src/)
├── dashboard.py              # Python script to read the data, and start a web server
└── README.md                 # This file
```

## Getting Started

### Quick Start (Recommended)
```bash
# Generate sample data and start dashboard server
python generate_data.py    # Starts web server at http://localhost:8000
```

### Manual Setup
```bash
# Convert parquet files and start web server
python dashboard.py         # Converts ../data/*.parquet to JSON and starts server

# Or serve static files directly
python -m http.server 8000  # Basic Python web server
# Then open http://localhost:8000 in your browser
```

### Usage
1. **Navigate**: Use the top navigation menu to switch between Overview and Scorecard views
2. **Filter data**: Use the sidebar filters to narrow down results by business unit, team, or location  
3. **Drill down**: Click any metric row in the Scorecard to view detailed analysis
4. **Stop server**: Press Ctrl+C to stop the web server

## Data Files and Schemas

### summary.json - Aggregated Metric Data

This file contains pre-aggregated compliance statistics grouped by metric and organizational dimensions.

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `datestamp` | String (YYYY-MM-DD) | Date when the metric was calculated |
| `metric_id` | String | Unique identifier for the security metric |
| `title` | String | Human-readable metric name |
| `category` | String | High-level metric categorization |
| `slo` | Number (0-1) | Target Service Level Objective threshold |
| `slo_min` | Number (0-1) | Minimum acceptable SLO threshold |
| `weight` | Number | Relative importance for scoring calculations |
| `indicator` | Boolean | Whether metric is a key performance indicator |
| `business_unit` | String | Business unit (use "undefined" if not applicable) |
| `team` | String | Responsible team (use "undefined" if not applicable) |
| `location` | String | Resource location (use "undefined" if not applicable) |
| `totalok` | Integer | Count of compliant resources |
| `total` | Integer | Total count of assessed resources |

**Example:**
```json
[
  {
    "datestamp": "2024-07-01",
    "metric_id": "access_mfa",
    "title": "Access Control - Multi-Factor Authentication",
    "category": "Identity Management",
    "slo": 0.95,
    "slo_min": 0.9,
    "weight": 1.0,
    "indicator": true,
    "business_unit": "Engineering",
    "team": "Platform",
    "location": "North America",
    "totalok": 151,
    "total": 168
  }
]
```

### detail.json - Individual Resource Compliance

This file contains detailed compliance records for individual resources with supporting evidence.

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `resource` | String | Unique identifier for the assessed resource |
| `resource_type` | String | Category of resource (host, user, application, etc.) |
| `detail` | String | Human-readable compliance finding or evidence |
| `compliance` | Number (0-1) | Compliance status (1=compliant, 0=non-compliant) |
| `metric_id` | String | Unique identifier matching summary.json |
| `title` | String | Human-readable metric name |
| `category` | String | High-level metric categorization |
| `indicator` | Boolean | Whether metric is a key performance indicator |
| `weight` | Number | Relative importance for scoring |
| `type` | String | Classification of metric type |
| `description` | String | Detailed explanation of the metric |
| `how` | String | Methodology for metric calculation |
| `slo_min` | Number (0-1) | Minimum acceptable threshold |
| `slo` | Number (0-1) | Target threshold |
| `datestamp` | String (YYYY-MM-DD) | Assessment date |
| `business_unit` | String | Business unit (use "undefined" if not applicable) |
| `team` | String | Responsible team (use "undefined" if not applicable) |
| `location` | String | Resource location (use "undefined" if not applicable) |

**Example:**
```json
[
  {
    "resource": "user_0001@company.com",
    "resource_type": "user",
    "detail": "MFA enabled and configured correctly",
    "compliance": 1,
    "metric_id": "access_mfa",
    "title": "Access Control - Multi-Factor Authentication",
    "category": "Identity Management",
    "indicator": true,
    "weight": 1.0,
    "type": "control",
    "description": "Compliance check for Access Control - Multi-Factor Authentication",
    "how": "Automated assessment of access control - multi-factor authentication controls",
    "slo_min": 0.9,
    "slo": 0.95,
    "datestamp": "2024-11-28",
    "business_unit": "Engineering",
    "team": "Platform",
    "location": "North America"
  }
]
```

## Use Cases

### 1. Executive Reporting
- **View**: Overview Dashboard
- **Purpose**: High-level visibility into security posture
- **Features**: Aggregated score cards, trend charts, SLO compliance tracking
- **Audience**: Leadership, security executives, compliance officers

### 2. Operational Management  
- **View**: Scorecard Dashboard
- **Purpose**: Monitor individual metric performance and trends
- **Features**: Sortable metric tables, sparkline trend indicators, comparative analysis
- **Audience**: Security operations teams, metric owners, program managers

### 3. Incident Investigation
- **View**: Detail Dashboard + Evidence Table
- **Purpose**: Deep-dive analysis of specific compliance failures
- **Features**: Resource-level evidence, detailed compliance findings, historical trends
- **Audience**: Security analysts, incident responders, auditors

### 4. Compliance Reporting
- **View**: All views with organizational filters
- **Purpose**: Generate compliance reports by business unit, team, or location
- **Features**: Multi-dimensional filtering, historical trending, evidence collection
- **Audience**: Compliance teams, auditors, regulatory reporting

## Data Generation

### Python Scripts

- **`generate_data.py`**: Creates sample data and automatically starts the web server
- **`dashboard.py`**: Converts parquet files to JSON and starts the web server  
- **`get_json.py`**: Collects real data from your security tools and systems (if available)

### Automated Data Pipeline

For production use, implement an automated pipeline that:

1. **Collects** raw security data from various tools and systems
2. **Processes** data into the required JSON schema format
3. **Aggregates** individual resource records into summary statistics
4. **Stores** both summary.json and detail.json files in the `src/json/` directory
5. **Schedules** regular updates (daily/weekly) to maintain current data

## Production Deployment

### Web Server Setup
The dashboard includes a built-in Python web server for production use:

```bash
# Production deployment
cd 04-dashboard
python dashboard.py    # Starts server on port 8000

# Custom port
python -c "import dashboard; dashboard.start_server(port=8080)"
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY 04-dashboard/ .

RUN pip install pandas

EXPOSE 8000
CMD ["python", "dashboard.py"]
```

### Reverse Proxy Configuration

#### Nginx
```nginx
server {
    listen 80;
    server_name dashboard.company.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Apache
```apache
<VirtualHost *:80>
    ServerName dashboard.company.com
    ProxyPass / http://localhost:8000/
    ProxyPassReverse / http://localhost:8000/
</VirtualHost>
```

### Data Pipeline Integration

#### Automated Data Updates
```bash
#!/bin/bash
# Update dashboard data from metrics pipeline
cd /app/cyber-metrics

# Generate fresh metrics
cd 02-metrics && python metrics.py

# Convert and start dashboard  
cd ../04-dashboard && python dashboard.py
```

#### CI/CD Integration
```yaml
# GitHub Actions example
name: Deploy Dashboard
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Metrics
        run: |
          cd 02-metrics
          python metrics.py
      - name: Deploy Dashboard
        run: |
          cd 04-dashboard  
          python dashboard.py &
```

## Technical Requirements

- **Browser Compatibility**: Modern browsers supporting ES6+ JavaScript
- **Dependencies**: Chart.js (included via CDN), Bootstrap 5 (included via CDN)
- **Server**: Built-in Python HTTP server (production-ready)
- **Data Format**: UTF-8 encoded JSON files
- **Performance**: Optimized for datasets up to 10,000 records per file
- **Security**: HTTPS recommended for production deployment

## Design Principles

- **Vanilla JavaScript**: No heavyweight frameworks - maintains simplicity and performance
- **Modular Architecture**: Reusable components for filters, charts, and data processing
- **Cache Management**: Automatic 1-hour caching of JSON data using localStorage
- **Responsive Design**: Mobile-first approach using Bootstrap 5
- **Filter Persistence**: Maintains user context across all dashboard views
- **Data Consistency**: Uses `metric_id` for reliable data grouping and navigation

## Contributing

1. Follow the existing code patterns and conventions
2. Maintain the modular architecture in the `src/js/` directory
3. Test with both sample and production data
4. Ensure responsive design works across device sizes
5. Update documentation for any schema or API changes