"""
Vercel serverless function entry point for Django application.
"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Get WSGI application
application = get_wsgi_application()

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler for Django.
    Converts Vercel request to WSGI and processes through Django.
    """
    # Build WSGI environ from Vercel request
    query_string = ''
    if hasattr(request, 'query_string') and request.query_string:
        if isinstance(request.query_string, bytes):
            query_string = request.query_string.decode('utf-8')
        else:
            query_string = request.query_string
    
    path_info = getattr(request, 'path', '/')
    method = getattr(request, 'method', 'GET')
    body = getattr(request, 'body', b'')
    headers = getattr(request, 'headers', {})
    
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path_info,
        'QUERY_STRING': query_string,
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)) if body else '0',
        'SERVER_NAME': headers.get('host', 'localhost').split(':')[0],
        'SERVER_PORT': headers.get('x-forwarded-port', '80'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.input': BytesIO(body) if body else BytesIO(),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers to environ
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key_upper = f'HTTP_{key_upper}'
        environ[key_upper] = value
    
    # Response data
    response_status = [200]
    response_headers = []
    
    def start_response(status, headers_list):
        response_status[0] = int(status.split()[0])
        response_headers[:] = headers_list
    
    # Process request through Django
    response_body = application(environ, start_response)
    
    # Collect response body
    body_parts = []
    try:
        for part in response_body:
            if isinstance(part, bytes):
                body_parts.append(part)
            else:
                body_parts.append(part.encode('utf-8'))
    finally:
        if hasattr(response_body, 'close'):
            response_body.close()
    
    body_result = b''.join(body_parts)
    
    # Return Vercel response
    from vercel import Response
    return Response(
        body_result,
        status=response_status[0],
        headers=dict(response_headers)
    )

