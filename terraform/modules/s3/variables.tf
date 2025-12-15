variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "glacier_transition_days" {
  description = "Days after which objects are transitioned to Glacier"
  type        = number
  default     = 30
}

variable "tags" {
  description = "Tags to apply to S3 resources"
  type        = map(string)
  default     = {}
}
