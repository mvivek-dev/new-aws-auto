output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.this.id
}

output "private_ip" {
  description = "Private IP of EC2 instance"
  value       = aws_instance.this.private_ip
}

output "security_group_id" {
  description = "Security group ID attached to EC2"
  value       = aws_security_group.ec2_sg.id
}

output "iam_role_name" {
  description = "IAM role attached to EC2 instance"
  value       = aws_iam_role.ec2_role.name
}

output "iam_instance_profile" {
  description = "IAM instance profile used by EC2"
  value       = aws_iam_instance_profile.ec2_profile.name
}
