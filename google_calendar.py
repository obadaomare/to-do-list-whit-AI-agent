import datetime
import os
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# النطاقات المطلوبة للوصول إلى تقويم Google
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_google():
    """المصادقة باستخدام OAuth 2.0"""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # حفظ بيانات المصادقة
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def add_event_to_google_calendar(title, description, start_time, end_time):
    """إضافة مهمة إلى تقويم Google"""
    creds = authenticate_google()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"✅ Task added to Google Calendar: {event.get('htmlLink')}")

# اختبار سريع
if __name__ == "__main__":
    add_event_to_google_calendar(
        title="Test Meeting",
        description="Discuss project updates",
        start_time="2025-03-01T09:00:00Z",
        end_time="2025-03-01T10:00:00Z"
    )
