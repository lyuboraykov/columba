# Columba
[![Build Status](https://travis-ci.org/lyuboraykov/columba.svg)](https://travis-ci.org/lyuboraykov/columba)

<img align="right" height="100" alt="Columba logo" src="https://github.com/lyuboraykov/columba/blob/master/views/columba.png?raw=true">
[Columba](https://github.com/lyuboraykov/columba)
is an email sending service. 
It supports multiple providers with failover between them.
Currently Sendgrid and Mailgun are supported, Sendgrid being the first choice and failing over to Mailgun.


## Usage

Columba is hosted on Heroku here: [Columba](https://columba.herokuapp.com) and can be tested 
with the provided form.
Here are some examples of using it:

```bash
# Columba with curl
curl columba.herokuapp.com/send \
    -F from='sender@columba.com' \
    -F to='recipient@columba.com' \
    -F cc='cc@columba.com' \
    -F bcc='bcc@columba.com' \
    -F subject='Hello' \
    -F body='Testing some Columba awesomness!'
    -F attachment=@files/somefile.jpg
    -F attachment=@files/someotherfile.jpg
```

This is the full list of fields:

| Field         | Values                                                            | Mandatory:
| ------------- |-------------                                                      |------------- 
| from          | The email address of the sender                                   | Yes
| to            | Supports multiple recipients divided by whitespace                | Yes
| cc            | ditto                                                             | No
| bcc           | ditto                                                             | No
| subject       | The text of the subject                                           | Yes
| body          | The text of the body.                                             | Yes
| attachment    | Can be multiple, each header should be in the format name="attachment" filename="real-filename.extension" \<The file content\>                                                                      | No

The API will return `HTTP 200` if the message has reached one of the providers.
This **doesn't** mean that the message was delivered.

## Design details

### Continuous deployment
[Travis CI](https://travis-ci.org/lyuboraykov/columba) runs the tests each time a new change is pushed in the repository and if the build passes Heroku deploys it. It is based entirely on Python 3.4. 

Columba is deployed in a [Gunicorn](http://gunicorn.org/) server.

### API
Columba relies on [Flask](http://flask.pocoo.org/) for it's API handling.
Flask is lightweight, easy to use and provides 100% WSGI compliance.
The send method is available under  https://columba.herokuapp.com/send and 
recieves POST requests with form data for the fields.
Under https://columba.herokuapp.com it returns a html form for testing purposes.

### Failover
Columba has a number of registered providers with priority for each.
Once a provider fails to send a message it chooses the next one sorted by priority.
It uses a [heap](http://en.wikipedia.org/wiki/Heap_%28data_structure%29) to choose the next one used to send the message.
The heap provides an optimal solution to the problem and python provides algorithms for it in [the standard library](https://docs.python.org/2/library/heapq.html).

### Registering providers
Currently [Sendgrid](https://sendgrid.com/) and [Mailgun](https://mailgun.com) are the registered providers.
To register a new provider one has to implement a client for it that inherits the [Provider](https://github.com/lyuboraykov/columba/blob/master/providers/provider.py) class. It basically has a `Send(message)` and an `__init__(authentication, username)` method.

By convention the providers' credentials are provided as environment variables to the columba client.
The provider accounts are part of the application configuration and most standard PaaS solutions use mechanisms for inserting it as
environment variables.

### Testing

Columba uses [Pytest](http://pytest.org/latest/) and Flasks `test_client` for it's testing part.
Pytest provides a more lightweight interface for testing and a logical convetion for separating test sections.

## Future improvements

There are a number of improvements that are to be implemeted to Columba's functionality.

### Authentication
Columba is to provide authentication with registration confirmation to prevent abuse of the API and restrict attacks. 

### Testing end to end scenarios
Columba is to test that actual emails are sent.
It currently tests all scenarios until requests reach the providers.
To do this it must have a testing account in an email service.
Also emails typically don't reach their destination immediately.
The providers, especially Mailgun have a noticable lag when receiving requests that should be handled by the tests.

### More providers
More providers are to be registered to take full advantage of Columba's potential.

### More email options

replyto and other email fields are to be implemented. Also the email body currently is text-only.
It could be provided as raw MIME or as HTML. Also inline images can be included.

### Better logo

The current logo is very low res but a better one is to be implemented.