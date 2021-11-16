locals {
  bucket_prefix = "custom-ding-code-for-testing-lambda"
  bucket_key    = "lambda.zip"
}

resource "aws_cloudformation_stack_set" "enable_custom_security_hub_findings" {
  name             = "EnableCustomSecurityHubFindings"
  description      = "Enable Custom Security Findings from multiple accounts"
  permission_model = "SERVICE_MANAGED"
  capabilities     = ["CAPABILITY_IAM"]

  template_body = file("${path.module}/custom_security_findings_stackset.yaml")

  #If the lambda source code goes beyond 4096 characters, need to move to S3 bucket for source
  parameters = {
    BucketPrefix = local.bucket_prefix
    BucketKey    = local.bucket_key
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


module "s3_bucket_for_us_east_1" {
  source        = "../regional_s3_bucket"
  bucket_prefix = local.bucket_prefix

}

module "s3_bucket_for_us_east_2" {
  source        = "../regional_s3_bucket"
  bucket_prefix = local.bucket_prefix
  providers = {
    aws = aws.us-east-2
  }
}

module "s3_bucket_for_us_west_1" {
  source        = "../regional_s3_bucket"
  bucket_prefix = local.bucket_prefix
  providers = {
    aws = aws.us-west-1
  }
}

module "s3_bucket_for_us_west_2" {
  source        = "../regional_s3_bucket"
  bucket_prefix = local.bucket_prefix
  providers = {
    aws = aws.us-west-2
  }
}

data "archive_file" "lambda_archive" {
  type        = "zip"
  source_dir  = "${path.module}/custom_finding_lambda/src/"
  output_path = "${path.module}/${local.bucket_key}"
}
//
//resource "aws_s3_bucket_object" "s3_object_for_us_east_1" {
//  bucket = module.s3_bucket_for_us_east_1.bucket.id
//  key    = local.bucket_key
//  source = data.archive_file.lambda_archive.output_path
//}
//
//resource "aws_s3_bucket_object" "s3_object_for_us_east_2" {
//  bucket = module.s3_bucket_for_us_east_2.bucket.id
//  key    = local.bucket_key
//  source = data.archive_file.lambda_archive.output_path
//  provider = aws.us-east-2
//}
//
//resource "aws_s3_bucket_object" "s3_object_for_us_west_1" {
//  bucket = module.s3_bucket_for_us_west_1.bucket.id
//  key    = local.bucket_key
//  source = data.archive_file.lambda_archive.output_path
//  provider = aws.us-west-1
//}
//
//resource "aws_s3_bucket_object" "s3_object_for_us_west_2" {
//  bucket = module.s3_bucket_for_us_west_2.bucket.id
//  key    = local.bucket_key
//  source = data.archive_file.lambda_archive.output_path
//  provider = aws.us-west-2
//}
