terraform {
  required_version = ">= 1.3.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

variable "domain_name" {
  description = "Subdomínio configurado para a aplicação OpenClaw"
  type        = string
  default     = "bot.cdc.org.br"
}

variable "server_ip" {
  description = "IP Público do servidor VPS"
  type        = string
  default     = "147.79.110.132"
}

resource "local_file" "ansible_inventory" {
  content = templatefile("${path.module}/inventory.tpl", {
    server_ip   = var.server_ip
    domain_name = var.domain_name
  })
  filename = "${path.module}/../ansible/inventory/hosts.ini"
}

output "subdomain_url" {
  value = "https://${var.domain_name}"
}
