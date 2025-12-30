"""
Vercel serverless function for Django application
This file handles all HTTP requests and routes them to Django using WSGI
"""

import os
import sys
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse, parse_qs

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

# Initialize Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Get WSGI application
application = get_wsgi_application()

def handler(request):
    """
    Vercel serverless function handler
    Converts Vercel request to WSGI environment and processes Django response
    """
    # Handle both dict and object-style requests
    if isinstance(request, dict):
        method = request.get('method', 'GET')
        url = request.get('url', '/')
        headers = request.get('headers', {})
        body = request.get('body', '')
        query_string = request.get('queryStringParameters', {})
    else:
        method = getattr(request, 'method', 'GET')
        url = getattr(request, 'url', '/')
        headers = getattr(request, 'headers', {})
        body = getattr(request, 'body', '')
        query_string = getattr(request, 'queryStringParameters', {})
    
    # Parse URL to get path
    parsed_url = urlparse(url if url.startswith('http') else f'http://localhost{url}')
    path = parsed_url.path
    
    # Build query string
    if query_string:
        if isinstance(query_string, dict):
            qs_parts = []
            for k, v in query_string.items():
                if isinstance(v, list):
                    qs_parts.extend([f'{k}={val}' for val in v])
                else:
                    qs_parts.append(f'{k}={v}')
            qs = '&'.join(qs_parts)
        else:
            qs = str(query_string)
    else:
        qs = parsed_url.query
    
    # Convert headers to dict if needed
    if not isinstance(headers, dict):
        headers = dict(headers) if headers else {}
    
    # Convert body to bytes if needed
    if isinstance(body, str):
        body_bytes = body.encode('utf-8')
    elif body is None:
        body_bytes = b''
    else:
        body_bytes = body
    
    # Get host from headers
    host = headers.get('host', 'localhost')
    if ':' in host:
        server_name, server_port = host.split(':', 1)
    else:
        server_name = host
        server_port = '80'
    
    # Build WSGI environment
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': path,
        'QUERY_STRING': qs,
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body_bytes)),
        'SERVER_NAME': server_name,
        'SERVER_PORT': server_port,
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.input': BytesIO(body_bytes),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add HTTP headers to environ
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value
    
    # Collect response
    response_status = []
    response_headers = []
    response_body = []
    
    def start_response(status, headers):
        response_status.append(status)
        response_headers.extend(headers)
    
    # Process request through Django
    try:
        result = application(environ, start_response)
        
        # Collect response body
        for chunk in result:
            response_body.append(chunk)
        
        if hasattr(result, 'close'):
            result.close()
        
        # Parse status code
        status_code = int(response_status[0].split()[0]) if response_status else 200
        
        # Convert headers to dict
        headers_dict = {}
        for header in response_headers:
            if len(header) == 2:
                headers_dict[header[0]] = header[1]
        
        # Combine body chunks
        body_bytes = b''.join(response_body)
        
        # Return response in Vercel format
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': body_bytes.decode('utf-8', errors='replace')
        }
    except Exception as e:
        # Return error response
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Internal Server Error: {error_msg}'
        }

