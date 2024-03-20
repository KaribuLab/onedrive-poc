# OneDrive POC

This is a simple POC to connect a python application with REST API of OneDrive

## Getting Started

First create a virtual environment and activate it:

```shell
virtualenv .venv
source .venv/bin/activate
```

Then create a `.env` file with the following content:

```shell
CLIENT_ID=096c39fe-2f68-4877-a48c-2747e009deb7
LOG_LEVEL=DEBUG # This variable is optional
```

> NOTE: To obtain your client_id, you must read this documentation: https://learn.microsoft.com/en-us/graph/auth-register-app-v2.
> When you choose the client application type select Multitenant.

Now install the dependencies:

```shell
pip install -r requirements.txt
```

To get the authorization code you need authorize your application with your **Microsoft Account**. Run the `main.py` script:

```shell
python main.py
```

Access to the link generated for the script login in your account and accept all permisions. When you are logged in you will be redirected to an authorization URL, copy it and paste in the input console.

If you have followed this steps you can run the script again and see the list of your OneDrive files.