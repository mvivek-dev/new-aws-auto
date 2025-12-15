# DevOps Automation Assignment

**Owner:** Vivek M.

## 📌 Project Overview
This project demonstrates end-to-end DevOps automation using:
- Terraform for Infrastructure as Code
- AWS (EC2, S3, RDS)
- Python automation using boto3 and PyMySQL
- CI/CD using GitHub Actions

---

## 🏗️ Architecture
- EC2: Application server
- S3: Log storage
- RDS (MySQL): Metadata persistence
- IAM Role: Secure AWS access

---

## 🚀 Infrastructure Setup (Terraform)

```bash
cd terraform
terraform init
terraform apply

Resources created:

* EC2 with IAM role
* Versioned S3 bucket
* Private MySQL RDS


## 🐍 Automation Script

Location:

```
scripts/aws_automation.py

Functionality:

* Uploads logs to S3
* Writes log entries to RDS

Run on EC2:

```bash
python3 scripts/aws_automation.py


## 🔁 CI/CD Pipeline

Implemented using GitHub Actions:

* Python dependency install
* Terraform Validation in CI
* Test execution using pytest

## 🧹 Cleanup

```bash
terraform destroy


## 🔐 Security Best Practices

* No hardcoded AWS credentials
* IAM roles used for EC2
* Environment variables for secrets


## ✅ Status

✔ Infrastructure provisioned
✔ Automation working
✔ CI/CD configured



# 4️⃣ FINAL PROJECT STRUCTURE (CHECK THIS)

aws-automation/
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── ec2/
│       ├── s3/
│       └── rds/
├── scripts/
│   └── aws_automation.py
├── ci-cd/
│   └── main.yml
├── tests/
│   └── test_dummy.py
├── requirements.txt
├── .env.example
└── README.md

