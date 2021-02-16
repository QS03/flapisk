import os
import jinja2
import boto3
from botocore.exceptions import ClientError

from flask import current_app as app


def send_email_ses(ToAddresses, Source, Message):
    if 'AWS_EXECUTION_ENV' in os.environ:
        client = boto3.client('ses')
    else:
        client = boto3.client(
            'ses',
            region_name=app.config['AWS_REGION'],
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY']
        )

    # Provide the contents of the email.
    response = client.send_email(
        Destination={'ToAddresses': ToAddresses},
        Source=Source,
        Message=Message,
    )


def send_registration_email(reg_data, verify_token):
    subject = 'Email confirmation'
    template_loader = jinja2.FileSystemLoader(searchpath=app.config['TEMPLATES_DIR'])
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("registration.html")
    html_content = template.render(reg_data=reg_data, token=verify_token)

    Message = {
        'Body': {'Html': {'Charset': "UTF-8", 'Data': html_content}},
        'Subject': {'Charset': "UTF-8", 'Data': subject},
    }

    send_email_ses(
        [reg_data['email']],
        app.config['SERVICE_EMAIL'],
        Message
    )
