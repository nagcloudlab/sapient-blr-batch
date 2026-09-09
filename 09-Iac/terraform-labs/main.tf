# -----------------------------------------------
# Terraform Demo: 2 VMs + Firewall on GCP
# -----------------------------------------------

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# -----------------------------------------------
# Firewall: Allow SSH and HTTP
# -----------------------------------------------
resource "google_compute_firewall" "allow_ssh_http" {
  name    = "allow-ssh-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22", "80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
}

# -----------------------------------------------
# VM 1 - Nginx Web Server
# -----------------------------------------------
resource "google_compute_instance" "vm1" {
  name         = "vm1-nginx"
  machine_type = var.machine_type
  tags         = ["web-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  network_interface {
    network = "default"
    access_config {} # gives external IP
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    echo "<h1>Hello from VM1 - Nginx</h1>" > /var/www/html/index.html
    systemctl start nginx
  EOT
}

# -----------------------------------------------
# VM 2 - App Server
# -----------------------------------------------
resource "google_compute_instance" "vm2" {
  name         = "vm2-app"
  machine_type = var.machine_type
  tags         = ["web-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    echo "<h1>Hello from VM2 - App Server</h1>" > /var/www/html/index.html
    systemctl start nginx
  EOT
}
