import datetime
import os
import uuid
import boto3


def create_custom_finding_json(accountId, awsRegion, productField, resources, severity, title, compliance, iso8061Time, noteText,
                                noteUpdatedBy):
    ecr_finding = [
        {
            'SchemaVersion': '2018-10-08',
            'Id': str(uuid.uuid4()),
            'ProductArn': 'arn:aws:securityhub:' + awsRegion + ':' + accountId + ':product/' + accountId + '/default',
            'ProductFields': productField,
            'GeneratorId': str(uuid.uuid4()),
            'AwsAccountId': accountId,
            'Types': ['Software and Configuration Checks'],
            'FirstObservedAt': iso8061Time,
            'UpdatedAt': iso8061Time,
            'CreatedAt': iso8061Time,
            'Severity': {'Label': severity},
            'Title': title,
            'Description': title,
            'Resources': resources,
            'WorkflowState': 'NEW',
            'Compliance': {'Status': compliance},
            'RecordState': 'ACTIVE',
            'Note': {'Text': noteText, 'UpdatedBy': noteUpdatedBy, 'UpdatedAt': iso8061Time}
        }
    ]
    return ecr_finding


def ecr_image_scan_finding(event, accountId, awsRegion, iso8061Time):
    findingsevcounts = event['detail']['finding-severity-counts']
    numCritical = findingsevcounts['CRITICAL'] if findingsevcounts.get('CRITICAL') else 0
    numMedium = findingsevcounts['MEDIUM'] if findingsevcounts.get('MEDIUM') else 0
    numHigh = findingsevcounts['HIGH'] if findingsevcounts.get('HIGH') else 0
    severity = "LOW"
    title = "ECR Finding"
    ECRComplianceRating = 'PASSED'
    if numHigh: severity, title, ECRComplianceRating = "HIGH", "High ECR Vulnerability", 'FAILED'
    if numCritical: severity, title, ECRComplianceRating = "CRITICAL", "Critical ECR Vulnerability", 'FAILED'
    if numMedium: severity, title, ECRComplianceRating = "MEDIUM", "Medium ECR Vulnerability", 'FAILED'
    productField = {'ECRRepoName': event['detail']['repository-name']}
    resources = [{
        'Type': 'AwsEcr',
        'Id':  event['resources'][0],
        'Partition': 'aws',
        'Region': awsRegion,
    }]
    return create_custom_finding_json(accountId, awsRegion, productField, resources, severity, title, ECRComplianceRating, iso8061Time, "dummy",
                                       event['resources'][0])


def iam_user_creation_finding(event, accountId, awsRegion, iso8061Time):
    productField = {'UserAgent': event['detail']['userAgent']}
    resources = [
        {
            'Type': 'AwsIAM',
            'Id': event['detail']['responseElements']['user']['arn'],
            'Partition': 'aws',
            'Region': awsRegion,
            'Details': {
                'AwsIamUser': {'CreateDate': iso8061Time, 'Path': '/', 'UserId': event['detail']['responseElements']['user']['userId'],
                               'UserName': event['detail']['responseElements']['user']['userName']}
            }
        }
    ]
    return create_custom_finding_json(accountId, awsRegion, productField, resources, "MEDIUM", "IAM User Created", "FAILED",
                                       iso8061Time, event['detail']['userIdentity']['type'], event['detail']['userIdentity']['arn'])


def lambda_handler(event, context):
    try:
        response, iso8061Time = {}, datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        if event['source'] == "aws.ecr":
            response = boto3.client('securityhub').batch_import_findings(
                Findings=ecr_image_scan_finding(event, os.environ['account_num'], os.environ['region'], iso8061Time))
        elif event['source'] == "aws.iam":
            response = boto3.client('securityhub').batch_import_findings(
                Findings=iam_user_creation_finding(event, os.environ['account_num'], os.environ['region'], iso8061Time))
        else:
            pass
        print(response)
    except Exception as e:
        print("Submitting finding to Security Hub failed, please troubleshoot further" + e)
        raise
