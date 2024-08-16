# Reference: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_cluster#example-usage---with-the-default-node-pool

resource "google_container_cluster" "k8s-cluster" {
  name     = "k8s-cluster"
  location = var.location

  initial_node_count = var.node_count

  node_config {
    machine_type = "e2-small"
    disk_size_gb = 20
    disk_type    = "pd-standard"
  }

}