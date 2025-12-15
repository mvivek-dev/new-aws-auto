resource "aws_db_subnet_group" "this" {
  name       = "mysql-subnet-group"
  subnet_ids = var.subnet_ids
  tags       = var.tags
}

resource "aws_security_group" "rds_sg" {
  name        = "mysql-rds-sg"
  description = "Security group for MySQL RDS"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = var.allowed_security_group_ids
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}

resource "aws_db_parameter_group" "this" {
  name   = "mysql-parameter-group"
  family = "mysql8.0"

  parameter {
    name  = "max_connections"
    value = "150"
  }

  tags = var.tags
}

resource "aws_db_instance" "this" {
  identifier              = "mysql-logs-db"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = var.db_instance_class
  allocated_storage       = 20

  db_name                 = var.db_name
  username                = var.db_username
  password                = var.db_password

  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]

  publicly_accessible     = false
  skip_final_snapshot     = true
  deletion_protection     = false
  parameter_group_name    = aws_db_parameter_group.this.name

  tags = var.tags
}
