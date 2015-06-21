try:
	from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
except ImportError:
	from http.server import SimpleHTTPRequestHandler as Handler
try:
	from SocketServer import TCPServer as Server
except ImportError:
	from http.server import HTTPServer as Server

from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs, urlparse
from . import requests
from copy import copy
import inspect, os

# Instantiate a BlueMix Watson service API
class WatsonService:
	def __init__( self, **kwargs ):
		self.auth		= kwargs['auth'];
		self.api_url	= kwargs['url'];

		for name, obj in kwargs['operations'].items():
			def request(
				self,
				method = obj['method'].upper(),
				path = obj['path'],
				headers = None,
				params = None,
				files = None,
				data = None,
				name = name
			):
				# Set parameters in 'path'
				if params is not None:
					for i in params:
						path = path.replace( '{' + i + '}', params[i] );

				if( method == 'POST' ):
					data = params;
					params = None;

				response = requests.request(
					method,
					self.api_url + path,
					auth = self.auth,
					params = params,
					files = files,
					data = data );

				return response.content.decode( 'utf-8' );

			setattr( WatsonService, name, request );
"""
# Start a server, that follows the WebAPI
def StartServer( WebAPI, port = 4242 ):
	is_empty = True;

	class Response:
		def __init__( self, request, method ):
			global is_empty;

			self.request = request;
			self.method = method;
			is_empty = True;

		def write( self, string ):
			global is_empty;

			if( isinstance( string, str ) ):
				string = string.encode();

			self.request.wfile.write( string );
			is_empty = False;

	class RequestHandler( Handler ):
		def params_GET( self ):
			return parse_qs( urlparse( self.path ).query, keep_blank_values = 1 );

		def params_POST( self ):
			headers = self.headers.get( 'Content-Type' );
			hlen = int( self.headers.get( 'Content-Length' ) );
			ctype, pdict = parse_header( headers );
			params = {};

			if( ctype == 'multipart/form-data' ):
				params = parse_multipart( self.rfile, pdict );
			elif( ctype == 'application/x-www-form-urlencoded' ):
				params = parse_qs( self.rfile.read( hlen ).decode( 'utf-8' ), keep_blank_values = 1 );

			return params;

		def do_GET( self ):
			global is_empty;

			path = urlparse( self.path ).path;
			r = Response( self, 'GET' );

			for url in WebAPI:
				if( path == url and ( 'method' not in WebAPI[url] or 'GET' == WebAPI[url]['method'] or 'GET' in WebAPI[url]['method'] ) ):
					self.send_response( 200 );

					callArgs = inspect.getargspec( WebAPI[url]['callback'] ).args;
					passArgs = { 'handler': r, 'params': self.params_GET() };

					for i in copy( passArgs ):
						if( i not in callArgs ):
							del passArgs[i];

					WebAPI[url]['callback']( **passArgs );
					r.write( '\r' );

					break;

			if( is_empty ):
				return Handler.do_GET( self );

		def do_POST( self ):
			global is_empty;

			path = urlparse( self.path ).path;
			r = Response( self, 'POST' );

			# include get variables in params
			params = self.params_GET();
			# include post variables in params (overwriting get vars if collision occurs)
			params.update( self.params_POST() );

			for url in WebAPI:
				if( path == url and ( 'POST' == WebAPI[url]['method'] or 'POST' in WebAPI[url]['method'] ) ):
					self.send_response( 200 );

					callArgs = inspect.getargspec( WebAPI[url]['callback'] ).args;
					passArgs = { 'handler': r, 'params': params };

					for i in copy( passArgs ):
						if( i not in callArgs ):
							del passArgs[i];

					WebAPI[url]['callback']( **passArgs );
					r.write( '\r' );

					break;

			if( is_empty ):
				return Handler.do_POST( self );

	port = int( os.getenv( 'VCAP_APP_PORT', port ) );

	httpd = Server( ( "", port ), RequestHandler );
	try:
		print( "Server starting at port {0}\n".format( port ) );
		print( "Available at: http://localhost:{0}/\n".format( port ) );
		print( "API access at:" );

		for url in WebAPI:
			method = WebAPI[url]['method'] if 'method' in WebAPI[url] else 'GET';
			print( "- {0}:http://localhost:{1}{2}".format( method, port, url ) );

		print( "\nRequests:" );
		httpd.serve_forever();
	except KeyboardInterrupt:
		pass;
	httpd.server_close();
"""