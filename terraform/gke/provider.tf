
variable "esgischool_k8s_gcp_projectid" {
  type = string
}

variable "gcp_zone"{
  default="europe-west3-a"
}

provider "google-beta" {
  project = "${var.esgischool_k8s_gcp_projectid}"
  // Frankfurt
  region = "${var.gcp_zone}"
  //credentials = "${file("~/.gcp/terraform-esgischool-k8s.json")}"
}

