event = {
  'summary': 'Appointment',
  'location': 'Somewhere',
  'start': {
    'dateTime': '2011-06-03T10:00:00.000-07:00'
  },
  'end': {
    'dateTime': '2011-06-03T10:25:00.000-07:00'
  },
}

created_event = service.events().insert(calendarId='primary', body=event).execute()

print created_event['id']


