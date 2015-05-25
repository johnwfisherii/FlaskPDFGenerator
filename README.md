# FlaskPDFGenerator
Flask + PDF Generator

Basic Flask PDF Generator, requirements provided for virtual env. 

Requires settings.json with mandrill credentials & email sender.

## Configure

Create a `settings.json` file in the same directory as `main.py` :

```json
{
    "mail_username":"YOUR USERNAME",
    "mail_key":"YOUR KEY/PASSWORD",
    "sender_email":"YOUR EMAIL"
}
```