terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  credentials = "./keys/credentials.json"
  project = "datastudio-343704"
  region  = "us-central1"
}

resource "google_storage_bucket" "module1-bucket" {
  name          = "module1-bucket-343704"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "module1_dataset" {
  dataset_id                  = var.bq_dataset_name
  location                    = "US"
}