#!/usr/bin/env python3
"""
Generate comprehensive dummy data for the security compliance dashboard
"""
import json
import random
from datetime import datetime, timedelta
import dashboard

# Configuration
business_units = ["Engineering", "Marketing", "Sales", "Finance", "Operations"]
teams = ["Platform", "Digital", "Enterprise", "Operations", "Infrastructure"]
locations = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East/Africa"]

metrics = [
    {
        "metric_id": "access_mfa",
        "title": "Access Control - Multi-Factor Authentication",
        "category": "Identity Management",
        "slo": 0.95,
        "slo_min": 0.90,
        "weight": 1.0,
        "indicator": True
    },
    {
        "metric_id": "patch_management",
        "title": "Vulnerability - Patch Management",
        "category": "Vulnerability Management",
        "slo": 0.98,
        "slo_min": 0.95,
        "weight": 0.9,
        "indicator": True
    },
    {
        "metric_id": "data_encryption",
        "title": "Data Protection - Encryption at Rest",
        "category": "Data Security",
        "slo": 0.99,
        "slo_min": 0.97,
        "weight": 1.2,
        "indicator": True
    },
    {
        "metric_id": "incident_response",
        "title": "Incident Response - Time to Resolution",
        "category": "Incident Management",
        "slo": 0.85,
        "slo_min": 0.80,
        "weight": 0.8,
        "indicator": False
    },
    {
        "metric_id": "backup_validation",
        "title": "Business Continuity - Backup Validation",
        "category": "Business Continuity",
        "slo": 0.92,
        "slo_min": 0.88,
        "weight": 0.7,
        "indicator": False
    },
    {
        "metric_id": "network_segmentation",
        "title": "Network Security - Segmentation Controls",
        "category": "Network Security",
        "slo": 0.96,
        "slo_min": 0.92,
        "weight": 1.1,
        "indicator": True
    },
    {
        "metric_id": "privileged_access",
        "title": "Privileged Access Management",
        "category": "Identity Management",
        "slo": 0.98,
        "slo_min": 0.94,
        "weight": 1.3,
        "indicator": True
    },
    {
        "metric_id": "security_training",
        "title": "Security Awareness Training",
        "category": "Human Security",
        "slo": 0.90,
        "slo_min": 0.85,
        "weight": 0.6,
        "indicator": False
    },
    {
        "metric_id": "asset_inventory",
        "title": "Asset Management - Inventory Completeness",
        "category": "Asset Management",
        "slo": 0.94,
        "slo_min": 0.90,
        "weight": 0.5,
        "indicator": False
    },
    {
        "metric_id": "log_monitoring",
        "title": "Security Monitoring - Log Coverage",
        "category": "Security Operations",
        "slo": 0.97,
        "slo_min": 0.93,
        "weight": 1.0,
        "indicator": True
    }
]

# Time range - monthly snapshots
start_date = datetime(2024, 7, 1)
dates = []
for i in range(6):  # 6 months
    current_date = start_date + timedelta(days=30 * i)
    dates.append(current_date.strftime("%Y-%m-%d"))

def generate_summary_data():
    """Generate comprehensive summary data"""
    summary_data = []
    
    # Base performance by business unit (some perform better than others)
    bu_performance = {
        "Engineering": 0.95,
        "Operations": 0.92,
        "Finance": 0.88,
        "Marketing": 0.85,
        "Sales": 0.82
    }
    
    # Base resource counts by business unit
    bu_base_resources = {
        "Engineering": 150,
        "Operations": 200,
        "Finance": 80,
        "Marketing": 90,
        "Sales": 70
    }
    
    for date_idx, datestamp in enumerate(dates):
        for metric in metrics:
            for bu in business_units:
                for team in teams:
                    for location in locations:
                        # Calculate base performance with some variance
                        base_perf = bu_performance[bu]
                        
                        # Add some metric-specific adjustment
                        if metric["metric_id"] in ["data_encryption", "privileged_access"]:
                            base_perf *= 1.02  # These are typically higher
                        elif metric["metric_id"] in ["incident_response", "security_training"]:
                            base_perf *= 0.95  # These are typically lower
                        
                        # Add gradual improvement over time
                        time_improvement = 0.01 * date_idx
                        
                        # Add some randomness
                        variance = random.uniform(-0.05, 0.05)
                        
                        performance_ratio = min(0.999, max(0.75, base_perf + time_improvement + variance))
                        
                        # Calculate resource counts
                        base_resources = bu_base_resources[bu]
                        growth_factor = 1 + (0.02 * date_idx)  # 2% growth per month
                        location_factor = random.uniform(0.7, 1.3)
                        
                        total_resources = int(base_resources * growth_factor * location_factor)
                        total_ok = int(total_resources * performance_ratio)
                        
                        record = {
                            "datestamp": datestamp,
                            "metric_id": metric["metric_id"],
                            "title": metric["title"],
                            "category": metric["category"],
                            "slo": metric["slo"],
                            "slo_min": metric["slo_min"],
                            "weight": metric["weight"],
                            "indicator": metric["indicator"],
                            "business_unit": bu,
                            "team": team,
                            "location": location,
                            "totalok": total_ok,
                            "total": total_resources
                        }
                        
                        summary_data.append(record)
    
    return summary_data

def generate_detail_data():
    """Generate detail data for the latest datestamp only"""
    detail_data = []
    latest_date = dates[-1]  # Latest date (2024-12-01)
    
    # Resource name generators
    def generate_resource_name(metric_id, idx):
        if metric_id in ["access_mfa", "privileged_access", "security_training"]:
            return f"user_{idx:04d}@company.com"
        elif metric_id in ["patch_management", "asset_inventory", "log_monitoring"]:
            return f"srv-{metric_id.replace('_', '')}-{idx:03d}.company.com"
        elif metric_id in ["data_encryption", "backup_validation"]:
            return f"database-{idx:03d}.company.com"
        elif metric_id == "network_segmentation":
            return f"network-segment-{idx:03d}"
        elif metric_id == "incident_response":
            return f"incident-{idx:05d}"
        else:
            return f"resource-{idx:04d}"
    
    def generate_detail_text(metric_id, compliance):
        details = {
            "access_mfa": [
                "MFA enabled and configured correctly",
                "MFA setup incomplete - missing backup methods",
                "No MFA configured on account"
            ],
            "patch_management": [
                "All critical patches applied within SLA",
                "Some patches pending - scheduled for next maintenance window",
                "Critical patches overdue by >30 days"
            ],
            "data_encryption": [
                "Data encrypted with AES-256, keys properly managed",
                "Encryption enabled but using deprecated algorithm",
                "No encryption detected on sensitive data"
            ],
            "incident_response": [
                "Incident resolved within SLA timeframe",
                "Incident resolved but exceeded target response time",
                "Incident response significantly delayed"
            ],
            "backup_validation": [
                "Backup integrity verified and restoration tested",
                "Backup exists but last validation >90 days ago",
                "Backup validation failed or no backup found"
            ],
            "network_segmentation": [
                "Network properly segmented with appropriate controls",
                "Basic segmentation in place but some gaps identified",
                "Insufficient network segmentation controls"
            ],
            "privileged_access": [
                "Privileged access properly managed and monitored",
                "Privileged access controls partially implemented",
                "Privileged access not properly controlled"
            ],
            "security_training": [
                "Security training completed within required timeframe",
                "Training overdue but less than 6 months",
                "Security training significantly overdue"
            ],
            "asset_inventory": [
                "Asset properly inventoried with all required metadata",
                "Asset in inventory but some metadata missing",
                "Asset not found in inventory system"
            ],
            "log_monitoring": [
                "Comprehensive logging enabled and monitored",
                "Basic logging enabled but coverage incomplete",
                "Insufficient logging or monitoring coverage"
            ]
        }
        
        metric_details = details.get(metric_id, ["Compliant", "Partially compliant", "Non-compliant"])
        
        if compliance == 1:
            return metric_details[0]
        elif compliance == 0:
            return metric_details[2]
        else:
            return metric_details[1]
    
    resource_counter = 1
    
    for metric in metrics:
        for bu in business_units:
            for team in teams:
                for location in locations:
                    # Determine number of resources for this combination
                    base_resources = random.randint(40, 120)
                    
                    # Generate individual resource records
                    for i in range(base_resources):
                        resource_name = generate_resource_name(metric["metric_id"], resource_counter)
                        resource_counter += 1
                        
                        # Determine compliance (matching summary ratios approximately)
                        bu_performance = {
                            "Engineering": 0.95,
                            "Operations": 0.92,
                            "Finance": 0.88,
                            "Marketing": 0.85,
                            "Sales": 0.82
                        }
                        
                        base_perf = bu_performance[bu]
                        if metric["metric_id"] in ["data_encryption", "privileged_access"]:
                            base_perf *= 1.02
                        elif metric["metric_id"] in ["incident_response", "security_training"]:
                            base_perf *= 0.95
                        
                        # Add some variance
                        performance_ratio = min(0.999, max(0.75, base_perf + random.uniform(-0.1, 0.1)))
                        
                        # Determine compliance
                        rand_val = random.random()
                        if rand_val < performance_ratio:
                            compliance = 1
                        elif rand_val < performance_ratio + 0.05:  # Small chance of partial compliance
                            compliance = random.uniform(0.1, 0.9)
                        else:
                            compliance = 0
                        
                        detail_text = generate_detail_text(metric["metric_id"], compliance)
                        
                        record = {
                            "resource": resource_name,
                            "resource_type": "user" if "user" in resource_name or "@" in resource_name else "system",
                            "detail": detail_text,
                            "compliance": compliance,
                            "metric_id": metric["metric_id"],
                            "title": metric["title"],
                            "category": metric["category"],
                            "indicator": metric["indicator"],
                            "weight": metric["weight"],
                            "type": "control",
                            "description": f"Compliance check for {metric['title']}",
                            "how": f"Automated assessment of {metric['title'].lower()} controls",
                            "slo_min": metric["slo_min"],
                            "slo": metric["slo"],
                            "datestamp": latest_date,
                            "business_unit": bu,
                            "team": team,
                            "location": location
                        }
                        
                        detail_data.append(record)
    
    return detail_data

if __name__ == "__main__":
    print("Generating summary data...")
    summary_data = generate_summary_data()
    
    print("Generating detail data...")
    detail_data = generate_detail_data()
    
    print(f"Generated {len(summary_data)} summary records")
    print(f"Generated {len(detail_data)} detail records")
    
    # Write summary.json
    with open("src/json/summary.json", "w") as f:
        json.dump(summary_data, f, indent=2)
    
    # Write detail.json
    with open("src/json/detail.json", "w") as f:
        json.dump(detail_data, f, indent=2)
    
    print("Data generation complete!")
    print("Starting dashboard web server...")
    
    # Start the web server
    dashboard.start_server()