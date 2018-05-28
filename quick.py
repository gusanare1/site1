from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))


'''#VER ARCHIVOS
# Call the Drive v3 API
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('u{0} (u{1})'.format(item['name'], item['id']))
'''

'''
#crear y saber ID DE UNA CARPETA
file_metadata = {
    'name': 'python_images',
    'mimeType': 'application/vnd.google-apps.folder'
}
file = service.files().create(body=file_metadata,
                                    fields='id').execute()
print('Folder ID: %s' % file.get('id'))
'''


folder_id = '158Sk_z9ERQR5pSY94x1bhw4_SOGeUjgg'
file_metadata = {
    'name': 'photo.jpg',
    'parents': [folder_id]
}
media = MediaFileUpload('a.jpg',
                        mimetype='image/jpeg',
                        resumable=True)
file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
print('File ID: %s' % file.get('id'))


#DESCARGAR ARCHIVOS E INCRUSTARLOS EN HTTP

