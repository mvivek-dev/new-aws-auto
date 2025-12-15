output "s3_bucket_name" {
  value = module.s3_logs.bucket_name
}

output "s3_bucket_arn" {
  value = module.s3_logs.bucket_arn
}

output "ec2_instance_id" {
  value = module.ec2_app.instance_id
}

output "ec2_private_ip" {
  value = module.ec2_app.private_ip
}
