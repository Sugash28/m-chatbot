terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.60"
    }
  }

  # Shared state backend for egr-ai-dev (created once, see docs/azure-deployment.md)
  backend "azurerm" {
    resource_group_name  = "rg-egr-tfstate"
    storage_account_name = "<STATE_STORAGE_ACCOUNT>"
    container_name       = "tfstate"
    key                  = "muovitech-chatbot.tfstate"
    use_azuread_auth     = true
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
