provider "aws" {
  alias  = "us-east-2"
  region = "us-east-2"
}

provider "aws" {
  alias  = "us-west-1"
  region = "us-west-1"
}

provider "aws" {
  alias  = "us-west-2"
  region = "us-west-2"
}



resource "aws_s3_bucket" "bucket_us_east_1" {
  bucket = "custom-security-hub-finding-code-us-east-1"
  acl    = "private"
}

resource "aws_s3_bucket" "bucket_us_east_2" {
  bucket = "custom-security-hub-finding-code-us-east-2"
  provider = aws.us-east-2
  acl    = "private"
  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "bucket_us_west_1" {
  bucket = "custom-security-hub-finding-code-us-west-1"
  provider = aws.us-west-1
  acl    = "private"
  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "bucket_us_west_2" {
  bucket = "custom-security-hub-finding-code-us-west-2"
  provider = aws.us-west-2
  acl    = "private"
  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

data "archive_file" "lambda_archive" {
  type        = "zip"
  source_dir  = "${path.module}/custom_findings_lambda"
  output_path = "${path.module}/lambda.zip"
}

resource "aws_s3_bucket_object" "object_us_east_1" {
  bucket = aws_s3_bucket.bucket_us_east_1.id
  key    = "custom_findings_lambda"
  source =  "${path.module}/lambda.zip"
}

resource "aws_s3_bucket_object" "object_us_east_2" {
  bucket = aws_s3_bucket.bucket_us_east_2.id
  key    = "custom_findings_lambda"
  provider = aws.us-east-2
  source = "${path.module}/lambda.zip"
}

resource "aws_s3_bucket_object" "object_us_west_1" {
  bucket = aws_s3_bucket.bucket_us_west_1.id
  key    = "custom_findings_lambda"
  provider = aws.us-west-1
  source = "${path.module}/lambda.zip"
}

resource "aws_s3_bucket_object" "object_us_west_2" {
  bucket = aws_s3_bucket.bucket_us_west_2.id
  key    = "custom_findings_lambda"
  provider = aws.us-west-2
  source = "${path.module}/lambda.zip"
}


resource "aws_cloudformation_stack_set" "enable_custom_security_hub_findings" {
  name             = "EnableCustomSecurityHubFindingssdfds"
  description      = "Enable Custom Security Findings from multiple accounts"
  permission_model = "SERVICE_MANAGED"
  capabilities     = ["CAPABILITY_IAM"]

  template_body = file("${path.module}/custom_security_findings_stackset.yaml")

  #If the lambda source code goes beyond 4096 characters, need to move to S3 bucket for source
  parameters = {
    S3BucketNameUSEastA : aws_s3_bucket.bucket_us_east_1.id
    S3BucketNameUSEastB : aws_s3_bucket.bucket_us_east_2.id
    S3BucketNameUSWestC : aws_s3_bucket.bucket_us_west_1.id
    S3BucketNameUSWestD : aws_s3_bucket.bucket_us_west_2.id
  }

  auto_deployment {
    enabled                          = true
    retain_stacks_on_account_removal = false
  }

  // Ignoring changes to administration_role_arn because auto_deployment conflicts with this
  lifecycle {
    ignore_changes = [administration_role_arn]
  }
}