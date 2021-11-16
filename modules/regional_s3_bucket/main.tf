data "aws_region" "current" {}

#tfsec:ignore:AWS002 tfsec:ignore:AWS098 we don't need logging enabled for this bucket and public access block because it's a script bucket
resource "aws_s3_bucket" "lambda_code_bucket_for_demss" {
  bucket = "${var.bucket_prefix}-${data.aws_region.current.name}"
  acl    = "private"

  lifecycle {
    prevent_destroy = false
  }

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}
//
//data "aws_iam_policy_document" "lambda_code_bucket_policy_document" {
//  statement {
//    sid       = "ReadObject"
//    actions   = ["s3:GetObject", "s3:GetObjectVersion"]
//    effect    = "Allow"
//    resources = ["${aws_s3_bucket.lambda_code_bucket_for_demss.arn}/*"]
//    principals {
//      type        = "AWS"
//      identifiers = ["*"]
//    }
//  }
//}
//
//resource "aws_s3_bucket_policy" "lambda_code_bucket_policy" {
//  bucket = aws_s3_bucket.lambda_code_bucket_for_demss.id
//  policy = data.aws_iam_policy_document.lambda_code_bucket_policy_document.json
//}
