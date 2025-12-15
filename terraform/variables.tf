variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "s3_bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "glacier_transition_days" {
  description = "Days before transition to Glacier"
  type        = number
  default     = 30
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_id" {
  type = string
}

variable "project_name" {
  type    = string
  default = "vivek-dev"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "private_subnet_ids" {
  description = "Private subnet IDs"
  type = list(string)
}


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

variable "tags" {
  description = "Tags for RDS resources"
  type        = map(string)
  default     = {}
}
