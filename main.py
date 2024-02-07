import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SAMPLE_SPREADSHEET_ID = "1fclu6EaP2E-xyDdXQMmBIzHPB_tJuPJDPuCYHtAqoBg"
SAMPLE_RANGE_NAME = "engenharia_de_software!C4:F27"

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port = 0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        
        def read_sheet(range_name):
            return sheet.values().get(
                spreadsheetId = SAMPLE_SPREADSHEET_ID,
                range = range_name
            ).execute()
        
        result = read_sheet(SAMPLE_RANGE_NAME)
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        arrays = {"absences": [], "P1": [], "P2": [], "P3": [], "m": [], "situation": [], "naf": []}

        for row in values:
            arrays["absences"].append(int(row[0]))
            arrays["P1"].append(int(row[1]))
            arrays["P2"].append(int(row[2]))
            arrays["P3"].append(int(row[3]))

        number_of_students = len(arrays["absences"])

        for i in range(number_of_students):
            average = (arrays["P1"][i] + arrays["P2"][i] + arrays["P3"][i]) / 30
            arrays["m"].append(average)

        sheet_classes = read_sheet("engenharia_de_software!A2:H2").get("values")
        number_of_classes = int(((str(sheet_classes[0])).split(": ")[1]).split("']")[0])
        
        def status(text, grade_needed):
            return arrays["situation"].append(text), arrays["naf"].append(grade_needed)

        for i in range(number_of_students):
            if (arrays["absences"][i] / number_of_classes < 0.25):
                if (arrays["m"][i] < 5):                    
                    status("Reprovado por Nota", 0)
                elif (arrays["m"][i] >= 5 and arrays["m"][i] < 7):
                    status("Exame Final", 10 - arrays["m"][i])
                else:
                    status("Aprovado", 0)
            else:
                status("Reprovado por Falta", 0)

        add_values = []

        def ceil(number):
            return 0 if not number else (int(number + (1 if int(number) % number == int(number) else 0)))

        for i in range(number_of_students):
            add_values.append([arrays["situation"][i], ceil(arrays["naf"][i])])

        result = sheet.values().update(
            spreadsheetId = SAMPLE_SPREADSHEET_ID,
            range = '!G4',
            valueInputOption = "USER_ENTERED",
            body = {"values": add_values}
            ).execute()

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
