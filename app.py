#!/usr/bin/env python3

from flask import Flask, request
app = Flask(__name__)

@app.route("/send", methods=['POST'])
def send():
    sender, recipients, subject, body, cc, bcc, attachments = parse_send_form_data(request)
    return "Mail sent! {}, {}, {}, {}, {}, {}, {}".format(sender, recipients, subject, body, cc, bcc, attachments)

def parse_send_form_data(request):
    sender = request.form['sender']
    recipients = request.form['recipients'].split(',')
    subject = request.form['subject']
    body = request.form['body']
    cc = parse_optional_parameter(request, 'cc', [])
    bcc = parse_optional_parameter(request, 'bcc', [])
    attachments = parse_optional_parameter(request, 'attachments', [])
    return sender, recipients, subject, body, cc, bcc, attachments

def parse_optional_parameter(request, parameter_name, default_value):
    if parameter_name in request.form.keys():
        return request.form[parameter_name]
    return default_value

if __name__ == "__main__":
    app.debug = True
    app.run()