# DevOps Automation Assignment

Project Overview
This project demonstrates end-to-end DevOps automation using:
- Terraform for Infrastructure as Code
- AWS (EC2, S3, RDS)
- Python automation using boto3 and PyMySQL
- CI/CD using GitHub Actions


Architecture
- EC2: Application server
- S3: Log storage
- RDS (MySQL): Metadata persistence
- IAM Role: Secure AWS access


Infrastructure Setup (Terraform)

```bash
cd terraform
terraform init
terraform validate
terraform apply

Resources created:

* EC2 with IAM role
* Versioned S3 bucket
* Private MySQL RDS

## Automation Script

Location:

```
scripts/aws_automation.py

Functionality:

* Uploads logs to S3
* Writes log entries to RDS


Run on EC2:

* login to ec2 using putty
* install dependencies - python3, pip3, git
* install requirements from requirements.txt
* run script
```bash
python3 scripts/aws_automation.py

-- output --
Log uploaded to S3
Log written to RDS
Automation completed


# CI/CD Pipeline

Implemented using GitHub Actions:

* Python dependency install
* Terraform Validation in CI
* Test execution using pytest

# Cleanup

```bash
terraform destroy


# Security Best Practices

* No hardcoded AWS credentials
* IAM roles used for EC2
* Environment variables for secrets


# Status

✔ Infrastructure provisioned
✔ Automation working
✔ CI/CD configured



# FINAL PROJECT STRUCTURE

aws-automation/
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       ├── ec2/
|       |     └──main.tf
|       |     └──variables.tf
|       |     └──outputs.tf
│       ├── s3/
|       |     └──main.tf
|       |     └──variables.tf
|       |     └──outputs.tf
│       └── rds/
|       |     └──main.tf
|       |     └──variables.tf
|       |     └──outputs.tf
├── scripts/
│   └── aws_automation.py
├── ci-cd/
│   └── main.yml
├── tests/
│   └── test_dummy.py
├── requirements.txt
├── .env.example
└── README.md
