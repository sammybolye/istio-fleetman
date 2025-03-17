variable "user_metadata" {
  type = map(string)
  default = {}
}

resource "google_workbench_instance" "instance" {
  name     = "sine"
  location = "us-central1-a"

  gce_setup {
    machine_type = "e2-standard-2" 
    container_image {
      repository = "us-central1-docker.pkg.dev/vertex-421211/vertex-docker-repo/dl-vscode"
      tag        = "startup"
    }

    metadata = merge(
      {
        terraform                  = "true"
        notebook-disable-terminal  = "true"
        notebook-disable-root      = "false"
        post-startup-script        = "gs://vertex-421211/setroot.sh"
      },
      var.user_metadata
    )

    tags = ["egress"]
  } 

  labels = {
    owner = "shyamn"
  }
}
output "merged_metadata" {
  value = merge(
    {
      terraform                  = "true"
      notebook-disable-terminal  = "true"
      notebook-disable-root      = "false"
      post-startup-script        = "gs://vertex-421211/setroot.sh"
    },
    var.user_metadata
  )
}

