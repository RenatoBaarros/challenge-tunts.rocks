# Challenge Tunts.Rocks 2024
<p align="center">
  <a href="" rel="noopener">
 <img width=auto height=120px padding-bottom=0px src="./logo_dev_training.png" alt="Scout logo"></a>
</p>

## 📝 Challenge

<p align="center"> 
Develop an application in a programming language of your choice (if applying for a specific programming language position, for example: Node.js developer, use the specific language/technology required for the position). <b>The application should be able to read a Google Sheets spreadsheet, retrieve the necessary information, calculate, and write the result back to the spreadsheet.</b>
</p>


## 📝 Step by step

- [Save the spreadsheet on Google Drive](#googledrive)
- [Set up the environment](#setupenvironment)
- [Install the client library and set up the sample](#installlibrary)
- [Set up the project](#setupproject)
- [Run the project](#runproject)
- [References](#references)

## 💻 Save the spreadsheet on Google Drive <a name="googledrive"></a>

<h3>→ <a href="https://docs.google.com/spreadsheets/d/1XvWJcRLj2WAeXO3ULQ_GxGm9---3SZkjMbGcXMJtt70/edit#gid=0">Original Spreadsheet</a></h3>

• Make a copy from original spreadsheet to google drive.<br>
• Allow access to anyone with the link.

<h3>→ <a href="https://docs.google.com/spreadsheets/d/1fclu6EaP2E-xyDdXQMmBIzHPB_tJuPJDPuCYHtAqoBg/edit#gid=0">My Spreadsheet</a></h3>

## 🌱 Set up the environment <a name="setupenvironment"></a>

• Create a Google Cloud project and enable the Google Drive API and Google Sheets API.<br>
• Configure the OAuth consent screen.<br>
• Authorize credentials for a desktop application.<br>
• Create my working directory.<br>
• Download the credentials and save as a JSON file as ```client_secret.json``` in my working directory.


## ⚙️ Install the client library <a name = "installlibrary"></a>

• Install the Google client library for Python:
```
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
• Create a file named ```main.py``` in my working directory.<br>
• Put the following code in ```main.py```:<br>
```python
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A2:E"


def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    print("Name, Major:")
    for row in values:
      # Print columns A and E, which correspond to indices 0 and 4.
      print(f"{row[0]}, {row[4]}")
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
```


## 🔧 Set up the project <a name = "setupproject"></a>

• Replace ```SAMPLE_SPREADSHEET_ID``` with the Google Drive's spreadsheet ID<br>
• Replace ```SAMPLE_RANGE_NAME``` to spreadsheet cell range from Google Drive.<br>
• Changge ```credential.json``` to ```client_secret.json```.<br>
• Delete comments and prints.<br>
• Create a *function* that calls the Sheets API.<br>
• Use the new *function* to receive the data from the spreadsheet cell range and another cell that are separated and hold the number of classes.<br>
• Create an *array* dictionary that will hold the *variables*.<br>
• Fill the *arrays* with the spreadsheet's data.<br>
• Create a *variable* that hold the number of students.<br>
• Use that spreadshet data to calculate the average grade from each student.<br>
• Use the *variable* ```sheet_classes``` to separate the number of classes of all semester that is into a *undefined* text and convert into an integer.<br>
• Create a new *function* to set the status from each student and the final grade needed to the ones who'll need to do the final exam.<br>
• Create a new *array* to hold the situation and the rounded final grade need from each student and create a new *function* that will return the rounded number.<br>
• To finish, replace in the spreadsheet the obtained values.<br>

## ▶️ Run the project <a name = "runproject"></a>

• Build and run the project:<br>
```
python3 main.py
```
• Authorize access<br>


## 📒 References <a name = "references"></a>

• https://developers.google.com/sheets/api/guides/concepts<br>
• https://developers.google.com/sheets/api/quickstart/python<br>