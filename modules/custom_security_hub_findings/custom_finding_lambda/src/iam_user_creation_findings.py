import uuid
from .create_custom_findings import CustomFindings


class IamUserCreationFindings(CustomFindings):
    def __init__(self, event):
        super().__init__()
        self.product_field = {'UserAgent': event['detail']['userAgent']}
        self.title = "IAM User Created"
        self.severity = "MEDIUM"
        self.compliance = "FAILED"
        self.note_text = event['detail']['userIdentity']['type']
        self.note_updated_by = event['detail']['userIdentity']['arn']
        self.resource_arn = event['detail']['responseElements']['user']['arn']
        self.resource_id = event['detail']['responseElements']['user']['userId']
        self.resource_user_name = event['detail']['responseElements']['user']['userName']

    def create_notification(self):
        ecr_finding = [
            {
                'SchemaVersion': '2018-10-08',
                'Id': str(uuid.uuid4()),
                'ProductArn': 'arn:aws:securityhub:' + self.aws_region + ':' + self.account_id + ':product/' + self.account_id + '/default',
                'ProductFields': self.product_field,
                'GeneratorId': str(uuid.uuid4()),
                'AwsAccountId': self.accountId,
                'Types': ['Software and Configuration Checks'],
                'FirstObservedAt': self.iso8061_time,
                'UpdatedAt': self.iso8061_time,
                'CreatedAt': self.iso8061_time,
                'Severity': {'Label': self.severity},
                'Title': self.title,
                'Description': self.title,
                'Resources': [
                    {
                        'Type': 'AwsIAM',
                        'Id': self.resource_arn,
                        'Partition': 'aws',
                        'Region': self.aws_region,
                        'Details': {
                            'AwsIamUser': {'CreateDate': self.iso8061_time, 'Path': '/', 'UserId': self.resource_id,
                                           'UserName': self.resource_user_name}
                        }
                    }
                ],
                'WorkflowState': 'NEW',
                'Compliance': {'Status': self.compliance},
                'RecordState': 'ACTIVE',
                'Note': {'Text': self.note_text, 'UpdatedBy': self.note_updated_by, 'UpdatedAt': self.iso8061_time}
            }
        ]
        return ecr_finding
