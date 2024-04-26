# Interact with Google Sheet

A demo of interacting with Google sheet with Camunda REST API authentication enabled. 


## Create a Google Sheet API key
1. Create a new API key for Google https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
2. Download the json and save it on the cretential.json
3. Copy the created email mpms-google.....@a........gserviceaccount.com
4. Go to the google sheet to want to integrate and share it with the above email **IMPORTANT** select it as editor

Demo sheet used: https://docs.google.com/spreadsheets/d/1jFHlcij79eiLlDhu2serhcn3ySSxmFrHb2bTYGpvHZg/edit?usp=sharing

# Simple example to get/write data to Google sheets
see: python/get_write_data_to_google_sheet.py

## Install python lib
pip3 install -r python/requirements.txt 

# Use Camunda Google sheets
- Run Camunda and deploy the externalRaiseTemperature_google_sheet.bpmn. The username and password is eurodyn:eurodyn
- Run externalGetDataFromGoogleSheet.py
- See the temperature to raise

![demo](./camunda_google_sheet.gif)

# Configuration
The following enviromental variables can be setup for changing the default:
- MPMS_SERVER
- MPMS_USERNAME
- MPMS_PASSOWRD

ie export MPMS_SERVER=demo-processorcestrator-server.eurodyn.com:8080