
# Provider / Global

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}


# Project / Environment

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "vivek-dev"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}


# Networking

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID for EC2 instance (public subnet)"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs (for RDS)"
  type        = list(string)
}


# EC2

variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}


# S3

variable "s3_bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "glacier_transition_days" {
  description = "Days before transition to Glacier"
  type        = number
  default     = 30
}


# RDS

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Master DB username"
  type        = string
}

variable "db_password" {
  description = "Master DB password"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}


# Tags

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}
