# Python API v2.0
Using Watson Services from BlueMix (online and locally) through a web server

## Usage
The main file is `server.py`. The name could be changed. However in case you need to upload ("push") the app online, you need to indicate the name of the file in `Procfile`.

Running `server.py` will create a simple HTTP server, which will then be accessible through your web browser. The default address is `http://localhost:4242/` where you will see a static web page.


## To run a server

To run a the server you need to import two packages from the API folder: `bottle` and `WebServer`. Then you need to call `WebServer.start();`. It is important that WebServer.start(); is called at the _end_ of the file.

~~~ python
from API import WebServer
from API.bottle import *

# Your code goes here

WebServer.start();
~~~


#### WebServer.start( host=[host], port=[port] )

The `start` method of WebServer can take two named arguments.
* The default value of `host` is 'localhost'.
* The default value of `port` is 4242.


## Routing the server

In order to have parts of the Python program accessible through the web browser you need to assign URL addresses at which Python will respond. Routing is implemented using the [Bottle Python Framework](http://bottlepy.org/). So - you also need to import the `bottle` package from the API folder.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

@route( '/test-url-1' )
def test1():
  return "Hello world!";

WebServer.start();
~~~

Once the server is started you can run the `test1` function through address `http://localhost:4242/test-url-1` (assuming you use the default host and port). The response to the web browser is returned. In this case it is a string "Hello world!".

Names of the functions **don't** matter. It makes no difference if you use _'def test1():'_ or _'def banana():'_.

## Content Types

You can return several content types to the browser. The default one is `text/html`. This means that the browser will interpret the result as HTML code. This could cause problems if you want to use some characters which are considered special in HTML, e.g. <, >, &.

In order to avoid this, you could explicitly set a content type by setting a value to `response.content_type` inside the function.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

@route( '/problem' )
def test1():
  return "<banana>";

@route( '/no-problem' )
def test2():
  response.content_type = 'text/plain';
  return "<banana>";

WebServer.start();
~~~

Opening `http://localhost:4242/problem` will output an empty string, whereas `http://localhost:4242/no-problem` will output `<banana>`.

In order to return JSON code you can explicitly set `request.content_type` to `application/json`. However the server automatically assumes JSON if you return a dictionary.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

@route( '/json' )
def test1():
	json = {
		'string': '....',
		'list': [1,2,3],
		'dict': {
			'property': 1
		}
	};

	return json;

WebServer.start();
~~~

`http://localhost:4242/json` will return JSON code.

A list of interesting content types (`request.content_type='...';`):
* text/plain (text)
* text/xml (XML code)
* application/json (JSON code)
* text/html (HTML code)


## Managing Requests

Except for the `@route('/...')` descriptor you can also use specific descriptors like `@get('/...')` and `@post('/...')` to specify the request method.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

@get( '/test' )
def test():
	json = { 'method': 'GET' };

	for i in request.GET:
		json[i] = request.GET[i];

	return json;

@post( '/test' )
def test():
	json = { 'method': 'POST' };

	for i in request.POST:
		json[i] = request.POST[i];

	return json;

WebServer.start();
~~~

Going to `http://localhost:4242/test?var1=value1&var2=value2` (this is a GET request) will output:
~~~ json
{"method": "GET", "var2": "value2", "va1": "value1"}
~~~

This way you pass variables to the URL `http://localhost:4242/test`

Similarly doing a POST request with two variables to `http://localhost:4242/test` will output:
~~~ json
{"method": "POST", "var2": "value2", "va1": "value1"}
~~~

You can also access `request.files` if files are being sent. For detailed information see [Bottle HTTP Request Methods](http://bottlepy.org/docs/dev/tutorial.html#http-request-methods) manual.


## Using Watson Services

You can setup and use Watson Services by importing `WatsonService` from the `API` folder.

### Setup a service

The following is an example of setting up the `Relationship Extraction` service.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

relext = WatsonService(
	url = 'https://gateway.watsonplatform.net/relationship-extraction-beta/api',
	auth = ( 'username', 'password' ),
	operations = {
		'sire': {
			'method': 'POST',
			'path': '/v1/sire/0'
		}
	}
);

WebServer.start();
~~~

##### `service = WatsonService( url=<string>, auth=(<username>, <password>), operations = {...} )`

The `WatsonService` class has three required named arguments: `url`, `auth` and `operations`. `service` is a variable that stores the API to this service from now on.

In order to get this code to run you need to:
* create an Application in BlueMix
* create a service (in this case Relationship Extraction)
* bind the Application to the service (in BlueMix)

This could be done using the web interface of BlueMix.

The `url`, `username` and `password` can be found in the credentials variable of the service.

![Credentails](http://i.imgur.com/L3K1A2u.png "Credentails 1")

After you open the credentials you will see JSON code. You don't need most of it. Just copy `url`, `username` and `password`.

![Credentails](http://i.imgur.com/NHqkDs4.png "Credentails 2")

In order to set up the `operations` argument, you need to lookup this address:
http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/apis/

Each service has an API. In this API, possible operations are enumerated. You can see them by clicking at "List Operations" at the right of each service. Each operation has two parameters - `method` and `path`.

![Credentails](http://i.imgur.com/NraOeAy.png "Services")

The method could be one of GET, POST, PUT and DELTETE. You need to specify this in the code.
The path is given on the right of the method.

### Setting up service with multiple operations

You can add more than one operation. Here is an example with the `Concept Expansion` service.

~~~ python
from API.watson import WatsonService
from API import WebServer
from API.bottle import *

conexp = WatsonService(
	url = 'https://gateway.watsonplatform.net/concept-expansion-beta/api',
	auth = ( 'username', 'password' ),
	operations = {
		'ping': {
			'method': 'GET',
			'path': '/v1/ping'
		},
		'upload': {
			'method': 'POST',
			'path': '/v1/upload'
		},
		'status': {
			'method': 'GET',
			'path': '/v1/status'
		},
		'result': {
			'method': 'PUT',
			'path': '/v1/result'
		}
	}
);

WebServer.start();
~~~

### Using a service

To use a service you need to call `service_instance`.`operation_name`(); Example using the code above:

~~~ python
...

result = conexp.ping();
print( result );

...
~~~

Sometimes the operations require certain parameters to be passed to the server. These parameters are described in the APIs page. You can take a look by clicking `Expand Operations`

![operations](http://i.imgur.com/fPs1qEU.png "Operation Parameters")

Here you need to pass three arguments: `seeds`, `dataset` and `label`.

~~~ python
...

result = conexp.upload( params = {
  'seeds': '{ "seeds": [ "term1", "term2" ] }',
  'dataset': 'twitter',
  'label': 'terms'
} );
print( result );

...
~~~

You can also pass files by using `files` instead of `params`.
