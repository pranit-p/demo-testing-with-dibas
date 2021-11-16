import uuid
from .create_custom_findings import CustomFindings


class EcrImageScanFindings(CustomFindings):
    def __init__(self, event):
        super().__init__()
        self.product_field = {'ECRRepoName': event['detail']['repository-name']}
        self.title = "ECR Finding"
        self.severity = "LOW"
        self.compliance = 'PASSED'

        finding_sev_counts = event['detail']['finding-severity-counts']
        num_critical = finding_sev_counts['CRITICAL'] if finding_sev_counts.get('CRITICAL') else 0
        num_medium = finding_sev_counts['MEDIUM'] if finding_sev_counts.get('MEDIUM') else 0
        num_high = finding_sev_counts['HIGH'] if finding_sev_counts.get('HIGH') else 0

        if num_high:
            self.severity, self.title, self.compliance = "HIGH", "High ECR Vulnerability", 'FAILED'
        if num_critical:
            self.severity, self.title, self.compliance = "CRITICAL", "Critical ECR Vulnerability", 'FAILED'
        if num_medium:
            self.severity, self.title, self.compliance = "MEDIUM", "Medium ECR Vulnerability", 'FAILED'
        self.resource_id = event['resources'][0]

    def create_notification(self):
        ecr_finding = [
            {
                'SchemaVersion': '2018-10-08',
                'Id': str(uuid.uuid4()),
                'ProductArn': 'arn:aws:securityhub:' + self.aws_region + ':' + self.account_id + ':product/' + self.account_id + '/default',
                'ProductFields': self.productField,
                'GeneratorId': str(uuid.uuid4()),
                'AwsAccountId': self.accountId,
                'Types': ['Software and Configuration Checks'],
                'FirstObservedAt': self.iso8061_time,
                'UpdatedAt': self.iso8061_time,
                'CreatedAt': self.iso8061_time,
                'Severity': {'Label': self.severity},
                'Title': self.title,
                'Description': self.title,
                'Resources': [{
                    'Type': 'AwsEcr',
                    'Id': self.resource_id,
                    'Partition': 'aws',
                    'Region': self.aws_region,
                }],
                'WorkflowState': 'NEW',
                'Compliance': {'Status': self.compliance},
                'RecordState': 'ACTIVE',
                'Note': {'Text': self.note_text, 'UpdatedBy': self.note_updated_by, 'UpdatedAt': self.iso8061_time}
            }
        ]
        return ecr_finding
