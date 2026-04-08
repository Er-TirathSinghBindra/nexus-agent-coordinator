#!/bin/bash

# Get Google Cloud Project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Could not determine Google Cloud Project ID."
    echo "Please run 'gcloud config set project <PROJECT_ID>' first."
    exit 1
fi

echo "Found Project ID: $PROJECT_ID"

# Enable necessary APIs
echo "Enabling required APIs for the Multi-Agent System..."
gcloud services enable aiplatform.googleapis.com --project=$PROJECT_ID
gcloud services enable apikeys.googleapis.com --project=$PROJECT_ID
gcloud services enable firestore.googleapis.com --project=$PROJECT_ID

# Setup .env file correctly directed to the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="$SCRIPT_DIR/../.env"

echo "Please provide your MCP Tool configurations below:"
read -p "Enter your Jira API Token: " JIRA_API_TOKEN
read -p "Enter your Jira Domain (e.g., your-domain.atlassian.net): " JIRA_DOMAIN
read -p "Enter your Jira User Email: " JIRA_USER
read -p "Enter your Notion API Key: " NOTION_API_KEY

cat <<EOF > "$ENV_FILE"
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=global
JIRA_API_TOKEN=$JIRA_API_TOKEN
JIRA_DOMAIN=$JIRA_DOMAIN
JIRA_USER=$JIRA_USER
NOTION_API_KEY=$NOTION_API_KEY
EOF

echo "Successfully generated local environment config at $ENV_FILE!"
