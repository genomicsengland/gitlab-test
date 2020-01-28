import pymsteams
import sharepy
import os
import json

WEBHOOK_URL = "https://outlook.office.com/webhook/a16a3386-a850-47fc-a9c3-c1c684176750@1fd5d786-267c-428d-b933-8465ef232363/IncomingWebhook/ef102be1eb1f4b3699b25ce0fbe32052/b5bfa296-0937-47f1-b027-459cfdfbbd28"

def send_msg_to_ms_teams(webhook_url, msg):
    """
    Send a message to a webhook (generated for a specific MS channel)
    For info on creating webhooks, see https://docs.microsoft.com/en-us/\
    microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook
    """
    tms_msg = pymsteams.connectorcard(webhook_url)
    tms_msg.test(msg)
    tm_msg.send()

def load_or_create_sp_session(sp_url="genomicsenglandltd.sharepoint.com",
                              username=None,
                              password=None):
    """
    check if a session file already exists
    if it does, load it, if not create one
    the resulting sp-session.pkl files are portable, to create one you'll
    need to create an app password to get through 2FA. See
    https://support.office.com/en-gb/article/create-an-app-password-for-office-365-3e7c860f-bda4-4441-a618-b53953ee1183
    username for sign-in is your full GEL email, e.g.
    simon.thompson@genomicsengland.co.uk
    the sessions will auto-refresh
    """
    if os.path.isfile("sp-session.pkl"):
        s = sharepy.load()
    else:
        if username and password:
            s = sharepy.connect(sp_url, username=username, password=password)
        else:
            s = sharepy.connect(sp_url)
        s.save()
    return s

def upload_file_to_sp(file_to_upload, dest_filename, dest_team, dest_fldr):
    """
    upload a file to a sharepoint destination
    file_to_upload: filepath for the file to upload
    dest_filename: name for file at destination
    dest_team: name of the team to upload to
    dest_fldr: folder path to upload to
    """
    # create or load session
    s = load_or_create_sp_session()
    # open the file
    with open(file_to_upload, 'rb') as read_file:
        content = read_file.read()
    headers = {"accept": "application/json;odata=verbose",
               "content-type": "application/x-www-urlencoded; charset=UTF-8"}
    url=f"https://genomicsenglandltd.sharepoint.com/teams/{dest_team}/_api/web/GetFolderByServerRelativeUrl('{dest_fldr}')/Files/add(url='{dest_filename}',overwrite=true)"
    p = s.post(url, data=content, headers=headers)
    p.raise_for_status()
    return p

def download_file_from_sp(team, fldr, filename):
    """
    download a file from a team sharepoint
    team: the sharepoint team hosting the file
    filepath: the filepath for the file
    """
    # create or load session
    s = load_or_create_sp_session()
    # make the url
    url=f"https://genomicsenglandltd.sharepoint.com/teams/{team}/_api/web/GetFolderByServerRelativeUrl('{fldr}')/Files('{filename}')/$value"
    p = s.get(url)
    p.raise_for_status()
    return p


def list_fldr_contents(team, fldr):
    """
    list the files and folders in a sharepoint folder
    team: the sharepoint team hosting the folder
    fldr: the folder path to inspect
    """
    # create or load session
    s = load_or_create_sp_session()
    # assemble the url and make the request
    url=f"https://genomicsenglandltd.sharepoint.com/teams/{team}/_api/web/GetFolderByServerRelativeUrl('{fldr}')?$expand=Folders,Files"
    p = s.get(url)
    p.raise_for_status()
    # get the list of files and folders
    d = json.loads(p.content.decode('utf-8'))['d']
    return ([x['Name'] for x in d['Folders']['results']],
            [x['Name'] for x in d['Files']['results']])


if __name__ == "__main__":
    import pandas as pd
    import xlrd
    import os
    load_or_create_sp_session(username=os.environ['SP_USERNAME'],
                              password=os.environ['SP_PASSWORD'])
    a = download_file_from_sp('GE-simon-test', 'Shared Documents/General', 'new-file.xlsx')
    c = pd.read_excel(xlrd.open_workbook(file_contents = a.content))
    print(c)

