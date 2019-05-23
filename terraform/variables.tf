variable "aws_region" {
  description = "The AWS region to deploy into (e.g. us-east-1)."
  default     = "us-east-1"
}

variable "tags" {
  type        = "map"
  description = "Tags to apply to all AWS resources created"

  default = {
    Team        = "NCATS OIS - Development"
    Application = "ansible-role-cyhy-runner testing"
  }
}

variable "ssm_parameters" {
  type        = "list"
  description = "The AWS SSM parameters that the IAM user needs to be able to read."
  default     = ["/github/oauth_token"]
}