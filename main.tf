provider "google" {
  project = "your-project-id" # Replace with a placeholder or note it’s assumed
  region  = "us-central1"
}

resource "google_cloud_run_service" "default" {
  name     = "doubleit-model"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/your-project-id/doubleit-model" # Placeholder image
      }
    }
  }
}