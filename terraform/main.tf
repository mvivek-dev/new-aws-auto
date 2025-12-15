locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

module "s3_logs" {
  source = "./modules/s3"

  bucket_name             = var.s3_bucket_name
  glacier_transition_days = var.glacier_transition_days

  tags                   = local.common_tags
}

module "ec2_app" {
  source = "./modules/ec2"

  vpc_id        = var.vpc_id
  subnet_id     = var.public_subnet_id
  project_name  = var.project_name
  environment   = var.environment

  
  s3_bucket_arn = module.s3_logs.bucket_arn

  tags = local.common_tags
}

module "rds_mysql" {
  source = "./modules/rds"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password

  allowed_security_group_ids = [
    module.ec2_app.security_group_id
  ]
  tags = local.common_tags
}