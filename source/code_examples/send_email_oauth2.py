"""
Send an e-mail message via your GMail account.

Adapted from:
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
https://developers.google.com/identity/protocols/OAuth2
https://blog.macuyiko.com/post/2016/how-to-send-html-mails-with-oauth2-and-gmail-in-python.html

To run:
1.) Get client app id
    You can get API credentials from:
    https://console.developers.google.com/?pli=1
    Sign up for account, select "Credentials"
    Click "Create Credentials" at the top. Select OAuth Client ID
    Select "Desktop App"
    Give it a name
    Copy/paste the values in for GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
2.) Run the app. It will give you a URL to paste into a browser and authenticate.
3.) Once authenticated using the URL, you'll get the access token. Paste it in
    as a string for GOOGLE_REFRESH_TOKEN.
4.) Update the FROM_ADDRESS to the account you logged in as.
5.) Update the TO_ADDRESS to where you want the e-mail to go.
6.) Run the app yet again. As you have a refresh token, it will now send the e-mail
    instead of trying to get a refresh token.
"""

import base64
import json
import smtplib
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import lxml.html

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# You can get API credentials from:
# https://console.developers.google.com/?pli=1
GOOGLE_CLIENT_ID = '<PUT OAUTH2 CLIENT ID HERE>'
GOOGLE_CLIENT_SECRET = '<PUT CLIENT SECRET HERE>'

# Once you get the API setup, run this file. It will give you a web address to
# log in. Once you log in, you'll get a verification code. Give that to the program
# which will give you a refresh token. Paste the refresh token below.
GOOGLE_REFRESH_TOKEN = None

FROM_ADDRESS = '<PUT YOUR ACCOUNT E_MAIL HERE>'
TO_ADDRESS = '<PUT DESTINATION ACCOUNT HERE>'


def command_to_url(command):
    return f'{GOOGLE_ACCOUNTS_BASE_URL}/{command}'


def url_escape(text):
    return urllib.parse.quote(text, safe='~-._')


def url_format_params(params):
    param_fragments = []
    for param in sorted(params.items(), key=lambda x: x[0]):
        param_fragments.append(f'{param[0]}={ url_escape(param[1])}')
    return '&'.join(param_fragments)


def generate_permission_url(client_id, scope='https://mail.google.com/'):
    params = {'client_id': client_id,
              'redirect_uri': REDIRECT_URI,
              'scope': scope,
              'response_type': 'code'}
    return f"{command_to_url('o/oauth2/auth')}?{url_format_params(params)}"


def call_authorize_tokens(client_id, client_secret, authorization_code):
    params = {'client_id': client_id,
              'client_secret': client_secret,
              'code': authorization_code,
              'redirect_uri': REDIRECT_URI,
              'grant_type': 'authorization_code'}
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url,
                                      urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def call_refresh_token(client_id, client_secret, my_refresh_token):
    params = {'client_id': client_id,
              'client_secret': client_secret,
              'refresh_token': my_refresh_token,
              'grant_type': 'refresh_token'}
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url,
                                      urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def generate_oauth2_string(username, my_access_token, as_base64=False):
    auth_string = f'user={username}\1auth=Bearer {my_access_token}\1\1'
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string


def get_authorization(google_client_id, google_client_secret):
    scope = "https://mail.google.com/"
    print('Navigate to the following URL to auth:', generate_permission_url(google_client_id, scope))
    authorization_code = input('Enter verification code: ')
    response = call_authorize_tokens(google_client_id, google_client_secret, authorization_code)
    return response['refresh_token'], response['access_token'], response['expires_in']


def refresh_authorization(google_client_id, google_client_secret, my_refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, my_refresh_token)
    return response['access_token'], response['expires_in']


def send_mail(fromaddr, toaddr, subject, message):
    my_access_token, my_expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, my_access_token, as_base64=True)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()


if __name__ == '__main__':
    if GOOGLE_REFRESH_TOKEN is None:
        print('No refresh token found, obtaining one')
        refresh_token, access_token, expires_in = get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
        print('Set the following as your GOOGLE_REFRESH_TOKEN:', refresh_token)
        exit()

    send_mail(FROM_ADDRESS, TO_ADDRESS,
              'A mail from you from Python',
              '<b>A mail from you from Python</b><br><br>' +
              'So happy to hear from you!')
