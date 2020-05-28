# -*- coding:utf-8 -*-
import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def get_auth():
  credentials = google.oauth2.credentials.Credentials(
      os.environ.get('ACCESS_TOKEN'),
      refresh_token=os.environ.get('REFRESH_TOKEN'),
      token_uri='https://oauth2.googleapis.com/token',
      client_id=os.environ.get('CLIENT_ID'),
      client_secret=os.environ.get('CLIENT_SECRET')
  )
  service = build('script', 'v1', credentials=credentials, cache_discovery=False)
  return service

def write_data(service, request):
  service.scripts().run(
    body = request,
    scriptId = os.environ.get('SCRIPT_ID')
  ).execute()
