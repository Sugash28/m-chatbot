# Azure deployment — MuoviTech / TurboCollector chatbot
 
Context for Claude Code and people working in this repo. Snapshot as of 2026-10-02: verify with `az` before relying on it.
 
## Where it runs
 
- **Subscription:** `egr-ai-dev` (`9fbce2ab-1088-449d-b853-ba5c6ee4f2de`), tenant Ernströmgruppen AB (`792adadf-4a72-4643-8d49-8e5de1d4b145`). Dev/PoC hosting for the EGR AI team, administered by Advania. Pay per use; budgets only alert.
- **Region:** Sweden Central.
- **Resource group:** `rg-muovitech-chatbot`, tag `project=muovitech-chatbot`.
| Resource | Name | Managed by | Notes |
| --- | --- | --- | --- |
| Foundry (AIServices) | `foundry-muovitech-chatbot` | CLI (not Terraform) | Endpoint in app setting `FOUNDRY_ENDPOINT` |
| Model deployment | `gpt-4o` | CLI | Chat + vision, **Standard** (regional, Sweden Central), 30 units ≈ 30k tokens/min |
| Model deployment | `embed-v-4-0` | CLI/portal | Cohere Embed v4, multilingual, Global Standard (may process outside EU) |
| Key Vault | `kv-muovitech-chatbot` | CLI | RBAC mode. Secrets: `foundry-api-key`, later `entra-client-secret` |
| App Service plan | `asp-muovitech-chatbot` | Terraform (`infra/`) | Linux, B2, **1 instance** |
| Web app | `app-muovitech-chatbot` | Terraform | `https://app-muovitech-chatbot.azurewebsites.net`, Python 3.12, system-assigned identity |
| Budget | `budget-muovitech-chatbot` | Terraform | Alerts at 80 % actual and 100 % forecast |
 
Terraform references the CLI-created resources as data sources; `terraform destroy` removes only the App Service, role assignments and budget.
 
## Contract between the app and Azure
 
The web app gets these environment variables (set in `infra/main.tf`):
 
| Variable | Value |
| --- | --- |
| `FOUNDRY_ENDPOINT` | Foundry resource endpoint |
| `OPENAI_BASE_URL` | `https://foundry-muovitech-chatbot.openai.azure.com/openai/v1/` |
| `CHAT_DEPLOYMENT` | `gpt-4o` |
| `EMBED_DEPLOYMENT` | `embed-v-4-0` |
| `FOUNDRY_API_KEY` | Key Vault reference, resolved by App Service at runtime |
| `DATA_DIR` | `/home/data` (persistent) |
 
Rules the app code must follow:
 
- **Listen on port 8000, address 0.0.0.0.** The startup command is `python -m streamlit run chatbot/app.py --server.port 8000 --server.address 0.0.0.0 --server.headless true`. Change `startup_command` in `infra/variables.tf` if the entry point moves.
- **Dependencies come from `requirements.txt`** at the repo root; App Service installs them on deploy.
- **Persistent data lives under `DATA_DIR`.** `/home` survives restarts and deploys but is a network share: keep the SQLite conversation DB there with one instance only, and copy the Chroma index to `/tmp` at startup (or rebuild it from `chunks.jsonl`) instead of querying it on `/home`.
- **Use deployment names, not model names**, in API calls (`model="gpt-4o"`).
- **Logged-in user** (once Entra login is on): read `X-MS-CLIENT-PRINCIPAL-NAME` from the request headers (`st.context.headers`). This replaces the shared password and the name prompt.
- **No secrets in code or git.** Locally, read the key into `.env` (git-ignored) with `az keyvault secret show --vault-name kv-muovitech-chatbot -n foundry-api-key --query value -o tsv`.
- Later option: drop the key entirely and authenticate with the web app's managed identity (it already has *Cognitive Services User* on the Foundry resource).
## How to deploy
 
**Infrastructure: from the terminal**, rarely, by Oliver. Role assignments need Owner activated in PIM first.
 
```bash
cd infra
az login --tenant 792adadf-4a72-4643-8d49-8e5de1d4b145
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```
 
**App code: GitHub Actions** (`.github/workflows/deploy-app.yml`) on every push to `main`. Fallback from the terminal:
 
```bash
git archive --format=zip -o app.zip HEAD -- . ':!infra' ':!.github'
az webapp deploy -g rg-muovitech-chatbot -n app-muovitech-chatbot --src-path app.zip --type zip
```
 
Pushes to `main` deploy straight to the running app (GitHub Free has no branch protection on private repos), so test locally first.
 
## One-time setup (not yet done)
 
1. **Terraform state backend** (shared by all EGR projects), if `rg-egr-tfstate` doesn't exist yet:
```bash
   RG=rg-egr-tfstate; SA=stegrtfstate$RANDOM
   az group create -n $RG -l swedencentral --tags project=platform
   az storage account create -n $SA -g $RG -l swedencentral --sku Standard_LRS \
     --min-tls-version TLS1_2 --allow-blob-public-access false --tags project=platform
   az role assignment create --assignee "oliver.odhe@ernstromgruppen.com" \
     --role "Storage Blob Data Contributor" --scope $(az storage account show -n $SA -g $RG --query id -o tsv)
   az storage container create -n tfstate --account-name $SA --auth-mode login
```
 
   Put the storage account name into `infra/versions.tf`.
 
2. **Pipeline identity for GitHub Actions** (after `terraform apply` has created the web app):
```bash
   ORG=<github-org>; REPO=<repo>
   az group create -n rg-egr-platform -l swedencentral --tags project=platform
   az identity create -n id-gh-muovitech-chatbot -g rg-egr-platform
   az identity federated-credential create --name gh-main \
     --identity-name id-gh-muovitech-chatbot -g rg-egr-platform \
     --issuer https://token.actions.githubusercontent.com \
     --subject "repo:$ORG/$REPO:ref:refs/heads/main" --audiences api://AzureADTokenExchange
   az role assignment create --role "Website Contributor" \
     --assignee-object-id $(az identity show -n id-gh-muovitech-chatbot -g rg-egr-platform --query principalId -o tsv) \
     --assignee-principal-type ServicePrincipal \
     --scope $(az webapp show -g rg-muovitech-chatbot -n app-muovitech-chatbot --query id -o tsv)
```
 
   GitHub repo > Settings > Secrets and variables > Actions > Variables: `AZURE_CLIENT_ID` (the identity's client ID), `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`. Org and repo names in the subject are case-sensitive.
 
3. **Entra ID login.** Needs permission to register applications in the tenant; if refused, Advania creates the registration.
```bash
   REDIRECT=$(terraform -chdir=infra output -raw login_redirect_uri)
   APP_ID=$(az ad app create --display-name "MuoviTech Chatbot" --sign-in-audience AzureADMyOrg \
     --web-redirect-uris "$REDIRECT" --enable-id-token-issuance true --query appId -o tsv)
   SECRET=$(az ad app credential reset --id $APP_ID --display-name easyauth --years 1 --query password -o tsv)
   az keyvault secret set --vault-name kv-muovitech-chatbot -n entra-client-secret --value "$SECRET" --query name -o tsv
   echo "entra_client_id = \"$APP_ID\"" >> infra/terraform.tfvars
   terraform -chdir=infra apply
```
 
   `AzureADMyOrg` limits login to Ernströmgruppen accounts. The client secret expires after one year.
 
## Checking and debugging
 
```bash
az webapp show -g rg-muovitech-chatbot -n app-muovitech-chatbot --query "{state:state, url:defaultHostName}" -o table
az webapp log tail -g rg-muovitech-chatbot -n app-muovitech-chatbot      # live logs
az webapp restart -g rg-muovitech-chatbot -n app-muovitech-chatbot
az cognitiveservices account deployment list -n foundry-muovitech-chatbot -g rg-muovitech-chatbot -o table
```
 
| Symptom | Likely cause |
| --- | --- |
| App shows "Application Error" | Startup command or port wrong; check `az webapp log tail` |
| Page loads but keeps reconnecting | WebSockets off, or the app crashed after start |
| `FOUNDRY_API_KEY` is the literal `@Microsoft.KeyVault(...)` text | Web app identity lacks *Key Vault Secrets User*, or the secret name is wrong |
| 429 from the model | `gpt-4o` capacity (30k tokens/min) exceeded; images count as tokens |
| 404 `DeploymentNotFound` | Wrong deployment name or endpoint |
| `terraform apply` fails on role assignment | Owner not activated in PIM |
| `MissingSubscriptionRegistration` | Run `az provider register -n <namespace> --wait` |
 
## Rules for Claude Code in this repo
 
- Never print, log or commit API keys or secrets; load them into variables.
- Ask before running `terraform apply`, `terraform destroy`, `az ... delete` or anything that changes Azure.
- Don't create Azure resources outside `rg-muovitech-chatbot` without asking; every new resource gets `project=muovitech-chatbot`.
- Prefer changing `infra/` and applying over one-off `az` changes, so the setup stays reproducible for a later move to MuoviTech's own Azure.
- Contacts: Oliver Odhe (Azure subscription), Sugash Krishnamoorthy (app code), Jonathan Wistrand at Advania (PIM, Foundry access, quota).
