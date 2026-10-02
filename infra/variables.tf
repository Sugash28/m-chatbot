variable "subscription_id" {
  description = "egr-ai-dev subscription ID (not a secret)"
  type        = string
  default     = "9fbce2ab-1088-449d-b853-ba5c6ee4f2de"
}

variable "project" {
  type    = string
  default = "muovitech-chatbot"
}

variable "location" {
  type    = string
  default = "swedencentral"
}

variable "app_sku" {
  description = "App Service plan size. B2 (2 cores, 3.5 GB) leaves room for local reranker/PyTorch."
  type        = string
  default     = "B2"
}

variable "startup_command" {
  type    = string
  default = "python -m streamlit run chatbot/app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true"
}

variable "chat_deployment" {
  type    = string
  default = "gpt-4o"
}

variable "embed_deployment" {
  type    = string
  default = "embed-v-4-0"
}

variable "entra_client_id" {
  description = "Client ID of the Entra app registration for login. Leave empty until it exists; login is then off."
  type        = string
  default     = ""
}

variable "budget_amount" {
  description = "Monthly budget alert for the resource group, in the billing currency"
  type        = number
  default     = 150
}

variable "budget_emails" {
  type    = list(string)
  default = ["oliver.odhe@ernstromgruppen.com", "eskil.nilsson@ernstromgruppen.com"]
}

variable "budget_start_date" {
  description = "First day of a month, RFC3339"
  type        = string
  default     = "2026-10-01T00:00:00Z"
}
