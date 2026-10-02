data "azurerm_client_config" "current" {}

locals {
  tags = { project = var.project }
}

# ---------------------------------------------------------------------------
# Existing resources, created with the Azure CLI on 2026-10-02.
# Referenced, not managed: `terraform destroy` will NOT remove them.
# ---------------------------------------------------------------------------
data "azurerm_resource_group" "rg" {
  name = "rg-${var.project}"
}

data "azurerm_cognitive_account" "foundry" {
  name                = "foundry-${var.project}"
  resource_group_name = data.azurerm_resource_group.rg.name
}

data "azurerm_key_vault" "kv" {
  name                = "kv-${var.project}"
  resource_group_name = data.azurerm_resource_group.rg.name
}

# ---------------------------------------------------------------------------
# App Service (Linux, Python, Streamlit)
# ---------------------------------------------------------------------------
resource "azurerm_service_plan" "plan" {
  name                = "asp-${var.project}"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = var.app_sku
  worker_count        = 1 # single instance: SQLite on /home must not have concurrent writers
  tags                = local.tags
}

resource "azurerm_linux_web_app" "app" {
  name                = "app-${var.project}" # becomes app-muovitech-chatbot.azurewebsites.net
  location            = var.location
  resource_group_name = data.azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.plan.id
  https_only          = true
  tags                = local.tags

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on          = true
    websockets_enabled = true # Streamlit needs websockets
    app_command_line   = var.startup_command
    ftps_state         = "Disabled"
    minimum_tls_version = "1.2"

    application_stack {
      python_version = "3.12"
    }
  }

  app_settings = {
    SCM_DO_BUILD_DURING_DEPLOYMENT      = "true" # installs requirements.txt on deploy
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "true" # /home persists across restarts and deploys

    DATA_DIR = "/home/data" # SQLite conversation DB; copy Chroma to /tmp at startup

    FOUNDRY_ENDPOINT  = data.azurerm_cognitive_account.foundry.endpoint
    OPENAI_BASE_URL   = "https://${data.azurerm_cognitive_account.foundry.name}.openai.azure.com/openai/v1/" # custom domain = resource name
    CHAT_DEPLOYMENT   = var.chat_deployment
    EMBED_DEPLOYMENT  = var.embed_deployment
    FOUNDRY_API_KEY   = "@Microsoft.KeyVault(VaultName=${data.azurerm_key_vault.kv.name};SecretName=foundry-api-key)"

    # Read by Easy Auth when login is enabled
    MICROSOFT_PROVIDER_AUTHENTICATION_SECRET = "@Microsoft.KeyVault(VaultName=${data.azurerm_key_vault.kv.name};SecretName=entra-client-secret)"
  }

  logs {
    application_logs {
      file_system_level = "Information"
    }
    http_logs {
      file_system {
        retention_in_days = 7
        retention_in_mb   = 35
      }
    }
  }

  # Microsoft Entra ID login, restricted to the Ernströmgruppen tenant.
  # Turned on once var.entra_client_id is set.
  dynamic "auth_settings_v2" {
    for_each = var.entra_client_id == "" ? [] : [1]
    content {
      auth_enabled           = true
      require_authentication = true
      unauthenticated_action = "RedirectToLoginPage"
      default_provider       = "azureactivedirectory"

      active_directory_v2 {
        client_id                  = var.entra_client_id
        tenant_auth_endpoint       = "https://login.microsoftonline.com/${data.azurerm_client_config.current.tenant_id}/v2.0"
        client_secret_setting_name = "MICROSOFT_PROVIDER_AUTHENTICATION_SECRET"
      }

      login {
        token_store_enabled = true
      }
    }
  }
}

# ---------------------------------------------------------------------------
# Permissions for the app's managed identity
# (role assignments require Owner activated in PIM when applying)
# ---------------------------------------------------------------------------
resource "azurerm_role_assignment" "app_kv_secrets" {
  scope                = data.azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id
}

# Enables keyless calls to Foundry later (Entra token instead of FOUNDRY_API_KEY)
resource "azurerm_role_assignment" "app_foundry_user" {
  scope                = data.azurerm_cognitive_account.foundry.id
  role_definition_name = "Cognitive Services User"
  principal_id         = azurerm_linux_web_app.app.identity[0].principal_id
}

# ---------------------------------------------------------------------------
# Budget alert for the whole project resource group (alerts only, no cap)
# ---------------------------------------------------------------------------
resource "azurerm_consumption_budget_resource_group" "budget" {
  name              = "budget-${var.project}"
  resource_group_id = data.azurerm_resource_group.rg.id
  amount            = var.budget_amount
  time_grain        = "Monthly"

  time_period {
    start_date = var.budget_start_date
  }

  notification {
    enabled        = true
    threshold      = 80
    operator       = "GreaterThan"
    threshold_type = "Actual"
    contact_emails = var.budget_emails
  }

  notification {
    enabled        = true
    threshold      = 100
    operator       = "GreaterThan"
    threshold_type = "Forecasted"
    contact_emails = var.budget_emails
  }
}
