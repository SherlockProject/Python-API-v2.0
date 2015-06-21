from API.watson import WatsonService
from API import WebServer
from API.bottle import *

# Setting up a Watson service
# - url and auth(username,password) found in the credentails of a service
# - operations: found at http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/apis/
relext = WatsonService(
	url = 'https://gateway.watsonplatform.net/relationship-extraction-beta/api',
	auth = ( 'cf8a7036-0bef-4d8a-9e2e-f429c955e668', 'W0TTdcbG3CFb' ),
	operations = {
		'sire': {
			'method': 'POST',
			'path': '/v1/sire/0'
		}
	}
);

# Using the relation extraction service we defined above
# Result at: http://localhost:4242/relation-extraction
@route( '/relation-extraction' )
def relextCallback():
	result = relext.sire( params = {
		'sid': 'ie-en-news',
		'txt': 'Some text that George Bush wrote a few years ago in Washington DC',
		'rt': 'xml'
	} );

	# Type of the returned document: XML document
	response.content_type = 'text/xml';

	return result;

# Returning a string (http://localhost:4242/test1)
@route( '/test1' )
def testapp():
	# Type of the returned document: plain text
	response.content_type = 'text/plain';
	return "string";

# Returning JSON (http://localhost:4242/test2)
@route( '/test2' )
def testapp():
	json = {
		'string': '....',
		'list': [1,2,3],
		'dict': {
			'property': 1
		}
	};
	return json;

WebServer.start();