provider "aws" {
  region = "us-east-2"
}


module "custom_security_hub_findings" {
  source                    = "./modules/custom_security_hub_findings"
  deployment_target_ids     = ["sdg"]
  deployment_target_regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]
}