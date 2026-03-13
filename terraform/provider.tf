terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
  required_version = ">= 1.3.0"
}

provider "google" {
  project = "ci-cd-pipeline-implementation"
  region  = "us-central1"
  zone    = "us-central1-a"
}
