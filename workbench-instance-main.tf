resource "google_workbench_instance" "instance" {
  name = "sin"
  location = "us-central1-a"

  gce_setup {
    machine_type = "e2-standard-2" 
    container_image {
      repository = "us-central1-docker.pkg.dev/vertex-421211/vertex-docker-repo/dl-vscode"
      tag = "iconv"
    }
  

      metadata = {
      terraform = "true"
      notebook-disable-terminal = "true"
      notebook-disable-root = "true"
    }

    tags = ["egress"]
  } 

    labels = {
    owner = "shyamn"
    } 

}
