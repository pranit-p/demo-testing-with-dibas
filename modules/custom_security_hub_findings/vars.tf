variable "deployment_target_ids" {
  type        = set(string)
  description = "Deployment target - prefer organization root id"
}

variable "deployment_target_regions" {
  type        = set(string)
  description = "Deployment target regions"
}
