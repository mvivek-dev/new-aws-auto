output "instance_id" {
  value = aws_instance.this.id
}

output "private_ip" {
  value = aws_instance.this.private_ip
}

output "security_group_id" {
  value = aws_security_group.ec2_sg.id
}

output "iam_role_name" {
  value = aws_iam_role.ec2_role.name
}
