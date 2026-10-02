output "app_url" {
  value = "https://${azurerm_linux_web_app.app.default_hostname}"
}

output "app_name" {
  value = azurerm_linux_web_app.app.name
}

output "resource_group" {
  value = data.azurerm_resource_group.rg.name
}

output "app_principal_id" {
  description = "Managed identity of the web app"
  value       = azurerm_linux_web_app.app.identity[0].principal_id
}

output "login_redirect_uri" {
  description = "Add this as a Web redirect URI on the Entra app registration"
  value       = "https://${azurerm_linux_web_app.app.default_hostname}/.auth/login/aad/callback"
}
