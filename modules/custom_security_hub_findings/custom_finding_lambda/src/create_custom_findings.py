import datetime
import os


class CustomFindings:
    def __init__(self):
        self.iso8061_time = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        self.account_id = os.environ['account_num']
        self.aws_region = os.environ['region']
