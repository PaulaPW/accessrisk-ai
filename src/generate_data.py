import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

def generate_access_logs(n=10000):
    rows = []

    countries = ["US", "Canada", "UK", "Germany", "Nigeria", "Russia", "China", "India"]
    roles = ["employee", "manager", "admin", "contractor", "service_account"]
    apps = ["Salesforce", "AWS", "GitHub", "Payroll", "ServiceNow", "Slack", "Azure"]

    for i in range(n):
        failed_logins = np.random.poisson(1)
        mfa_failures = np.random.poisson(0.5)
        new_device = np.random.choice([0, 1], p=[0.8, 0.2])
        new_country = np.random.choice([0, 1], p=[0.85, 0.15])
        impossible_travel = np.random.choice([0, 1], p=[0.93, 0.07])
        after_hours = np.random.choice([0, 1], p=[0.7, 0.3])
        privileged = np.random.choice([0, 1], p=[0.75, 0.25])
        sensitive_app = np.random.choice([0, 1], p=[0.65, 0.35])
        dormant_account = np.random.choice([0, 1], p=[0.9, 0.1])
        contractor = np.random.choice([0, 1], p=[0.8, 0.2])
        downloads = np.random.poisson(3)

        risk_score = (
            failed_logins * 6 +
            mfa_failures * 10 +
            new_device * 12 +
            new_country * 14 +
            impossible_travel * 25 +
            after_hours * 10 +
            privileged * 18 +
            sensitive_app * 12 +
            dormant_account * 15 +
            contractor * 8 +
            downloads * 2
        )

        if risk_score >= 70:
            label = 2
            risk_level = "High Risk"
        elif risk_score >= 35:
            label = 1
            risk_level = "Suspicious"
        else:
            label = 0
            risk_level = "Normal"

        rows.append({
            "user_id": f"user_{i}",
            "country": random.choice(countries),
            "role": random.choice(roles),
            "app": random.choice(apps),
            "failed_logins": failed_logins,
            "mfa_failures": mfa_failures,
            "new_device": new_device,
            "new_country": new_country,
            "impossible_travel": impossible_travel,
            "after_hours": after_hours,
            "privileged": privileged,
            "sensitive_app": sensitive_app,
            "dormant_account": dormant_account,
            "contractor": contractor,
            "downloads": downloads,
            "risk_score": risk_score,
            "label": label,
            "risk_level": risk_level
        })

    return pd.DataFrame(rows)

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)

    df = generate_access_logs(10000)

    output_path = "data/raw/synthetic_access_logs.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset created successfully: {output_path}")
    print(df.head())
    print(df["risk_level"].value_counts())
