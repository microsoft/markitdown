// ──────────────────────────────────────────────────────────────
// MarkItDown – Azure Infrastructure (Container Apps)
// ──────────────────────────────────────────────────────────────

targetScope = 'resourceGroup'

// ─── Parameters ──────────────────────────────────────────────

@description('Primary location for all resources')
param location string = resourceGroup().location

@description('Unique suffix to avoid naming collisions (default: first 6 chars of resource group ID)')
param uniqueSuffix string = substring(uniqueString(resourceGroup().id), 0, 6)

@description('Container image (set during CI/CD)')
param containerImage string

@description('Container port exposed by the app')
param containerPort int = 8000

@description('Enable MarkItDown plugins inside the service')
param enablePlugins bool = false

@description('Shared ACR login server (e.g. myacr.azurecr.io) – set by CI/CD')
param acrLoginServer string

@description('Shared ACR admin username – set by CI/CD')
param acrUsername string

@description('Shared ACR admin password – set by CI/CD')
@secure()
param acrPassword string

// ─── Variables ───────────────────────────────────────────────

var appName = 'markitdown-https-server'
var logAnalyticsName = 'markitdown-logs-${uniqueSuffix}'
var appEnvName = 'markitdown-env-${uniqueSuffix}'

// ─── Log Analytics Workspace ─────────────────────────────────

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  tags: {
    Component: 'MarkItDown'
  }
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// ─── Container Apps Environment ──────────────────────────────

resource appEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: appEnvName
  location: location
  tags: {
    Component: 'MarkItDown'
  }
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ─── Container App ───────────────────────────────────────────

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  location: location
  tags: {
    Component: 'MarkItDown'
  }
  properties: {
    managedEnvironmentId: appEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: containerPort
        transport: 'auto'
        allowInsecure: false
      }
      registries: [
        {
          server: acrLoginServer
          username: acrUsername
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: acrPassword
        }
      ]
    }
    template: {
      containers: [
        {
          name: appName
          image: containerImage
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/healthz'
                port: containerPort
                scheme: 'HTTP'
              }
              initialDelaySeconds: 10
              periodSeconds: 30
            }
          ]
          env: [
            {
              name: 'MARKITDOWN_ENABLE_PLUGINS'
              value: enablePlugins ? 'true' : 'false'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
      }
    }
  }
}

// ─── Outputs ─────────────────────────────────────────────────

output containerAppFqdn string = containerApp.properties.configuration.ingress.fqdn
output containerAppName string = containerApp.name
output containerAppEnvironmentName string = appEnvironment.name
