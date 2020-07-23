## Drive Box

This is a GUI application which allows the user to:

- Upload files to Google Drive
- Download files from Google Drive

### Details

It uses [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2) and [Google Drive API](https://developers.google.com/drive) to get details of the files stored in Drive and Upload or Download files.
You only need to authenticate once and the application saves the access token for next run. Once Authorized, you can Upload/Download files easily.

### Requirements

- Python 3 (or above)
- [tkinter](https://docs.python.org/3/library/tk.html)
- Google client libraries
- [PIL](https://pypi.org/project/Pillow/)

### How to use?

- Install Python3 (if not already installed).
- Clone the Drive-Box git repository.
- Go to [Google API console](https://console.developers.google.com/apis).
- Create a new Project and enable Google Drive API for it.
- Now go to Credentials, select OAuth client ID, download client secrets from here, save it as 'credentials.json' and copy it in 'Drive-Box/files/important/' directory.

- Now, Install the required libraries by executing following command:

    `(sudo) pip3 install -r requirements.txt`

- Now, execute the following command from Drive-Box directory to run the script:

    `python3 __init__.py`

- A new browser window will be opened. Allow the application to access the Google Drive data and close the window after the authorization flow has completed.
- Now you can Upload and Download files.

Note: To remove the user, click on User's Profile Photo in top Right corner and then click Sign out button.
