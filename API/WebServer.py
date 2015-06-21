from API.bottle import *;
import os;

def start( host = 'localhost', port = 4242 ):
	host = os.getenv( 'VCAP_APP_HOST', host );
	port = int( os.getenv( 'PORT', port ) );

	# Set up index page
	@route( '/' )
	def index_page():
		return static_file( 'index.html', root='./static' );

	# Static files
	@route('/<filepath:path>')
	def server_static(filepath):
		return static_file(filepath, root='./static');

	run( host = host, port = port );