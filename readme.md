Python Sample for Alexa Top Sites
---------------------------------

This sample will make a request to the Alexa Top Sites web service 
using your Access Key ID and Secret Access Key.

Requirements:  
  * Python v2.7.3  
  * [Requests: HTTP for Humans &rarr;](http://python-requests.org)  
  * [xml.etree.ElementTree: XML parser for Python &rarr;](http://effbot.org/zone/element-index.htm)

Steps:  
  * Sign up for an [Amazon Web Services &rarr;](http://aws.amazon.com)  
  * Get your `Access Key ID` and `Secret Access Key`  
  * Sign up for [Alexa Top Sites &rarr;](http://aws.amazon.com/alexatopsites)  
  * Install all requirements using `pip`  
  * Run `topsites.py --auth auth.yaml --country XX`  

Installation and Usage:

    $ pip install -r requirements.txt
    $ python topsites.py --auth auth.yaml --country XX

Authorization File:
The format for the authorization file is:

```
access_key_id: ACCESS_KEY_ID
secret_access_key: SECRET_ACCESS_KEY
```

The main benefit is to avoid having your access token visible in the command 
line, which can be retrieved by a super user with `ps` or using the /proc 
filesystem

If you are getting "Not Authorized" messages, 
you probably have one of the following problems:

* Your access key or secret key were not entered properly.  
* You did not sign up for [Alexa Top Sites](http://aws.amazon.com/alexatopsites)
* Your credit card was not valid.
