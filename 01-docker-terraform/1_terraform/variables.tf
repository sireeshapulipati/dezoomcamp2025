variable "bq_dataset_name" {
    description = "My BigQuery dataset name"
    default = "demo_dataset"
}

variable "gcs_storage_class" {
    description = "GCS Bucket Storage Class"
    default = "STANDARD"
}