import boto3
from .ecr_image_scan_findings import EcrImageScanFindings
from .iam_user_creation_findings import IamUserCreationFindings


def lambda_handler(event, context):
    try:
        response = {}
        if event['source'] == "aws.ecr":
            response = boto3.client('securityhub').batch_import_findings(Findings=EcrImageScanFindings(event).create_notification)
        elif event['source'] == "aws.iam":
            response = boto3.client('securityhub').batch_import_findings(Findings=IamUserCreationFindings(event).create_notification)
        else:
            pass
        print(response)
    except Exception as e:
        print("Submitting finding to Security Hub failed, please troubleshoot further" + e)
        raise
