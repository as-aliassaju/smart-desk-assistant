output "kubeconfig_command" {
  value = "gcloud container clusters get-credentials ${google_container_cluster.primary.name} --zone ${var.region} --project ${var.project_id}"
}
