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

# Initialize Django application lazily
_application = None
_init_error = None

def get_application():
    """Lazy initialization of Django application."""
    global _application, _init_error
    if _application is None and _init_error is None:
        try:
            # Import Django WSGI application
            from django.core.wsgi import get_wsgi_application
            _application = get_wsgi_application()
            print("Django application initialized successfully")
        except Exception as e:
            import traceback
            _init_error = (e, traceback.format_exc())
            print(f"Error initializing Django: {e}")
            print(traceback.format_exc())
    if _init_error:
        raise _init_error[0]
    return _application

# Vercel handler function
def handler(request):
    """
    Vercel serverless function handler for Django.
    """
    try:
        # Get Django application (with error handling)
        try:
            application = get_application()
        except Exception as init_error:
            error_msg = f"Failed to initialize Django application: {str(init_error)}"
            print(error_msg)
            if _init_error:
                print(_init_error[1])  # Print full traceback
            
            # Return a helpful error message
            error_body = (
                f"Application Initialization Error\n\n"
                f"{error_msg}\n\n"
                f"Common causes:\n"
                f"- Missing DATABASE_URL environment variable (required for Vercel)\n"
                f"- Database connection issues\n"
                f"- Missing environment variables\n\n"
                f"Please check the Vercel function logs for detailed error information."
            )
            try:
                from vercel import Response
                return Response(
                    error_body.encode('utf-8'),
                    status=500,
                    headers={'Content-Type': 'text/plain; charset=utf-8'}
                )
            except ImportError:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'text/plain; charset=utf-8'},
                    'body': error_body
                }
        
        # Extract request properties
        path = getattr(request, 'path', '/')
        method = getattr(request, 'method', 'GET')
        
        # Get query string
        query_string = ''
        if hasattr(request, 'query_string'):
            qs = request.query_string
            if qs:
                query_string = qs.decode('utf-8') if isinstance(qs, bytes) else str(qs)
        elif hasattr(request, 'url') and '?' in request.url:
            query_string = request.url.split('?', 1)[1]
        
        # Get body
        body = b''
        if hasattr(request, 'body'):
            body = request.body if request.body else b''
        elif hasattr(request, 'get_body'):
            body = request.get_body() or b''
        
        # Get headers
        headers = {}
        if hasattr(request, 'headers'):
            headers = request.headers
        elif hasattr(request, 'get_headers'):
            headers = request.get_headers()
        
        # Build WSGI environ
        host = headers.get('host', 'localhost')
        if ':' in str(host):
            server_name, server_port = str(host).split(':', 1)
        else:
            server_name = str(host)
            server_port = headers.get('x-forwarded-port', '80')
        
        environ = {
            'REQUEST_METHOD': str(method),
            'SCRIPT_NAME': '',
            'PATH_INFO': str(path),
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'SERVER_NAME': server_name,
            'SERVER_PORT': str(server_port),
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
            environ[key_upper] = str(value)
        
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
                    body_parts.append(str(part).encode('utf-8'))
        finally:
            if hasattr(response_body, 'close'):
                try:
                    response_body.close()
                except:
                    pass
        
        body_result = b''.join(body_parts)
        
        # Return Vercel response
        try:
            from vercel import Response
            return Response(
                body_result,
                status=response_status[0],
                headers=dict(response_headers)
            )
        except ImportError:
            # Fallback format
            return {
                'statusCode': response_status[0],
                'headers': dict(response_headers),
                'body': body_result.decode('utf-8', errors='ignore')
            }
            
    except Exception as e:
        # Error handling with detailed logging
        import traceback
        error_trace = traceback.format_exc()
        error_msg = f"Handler error: {str(e)}"
        print(error_msg)
        print(error_trace)
        
        # Return error response
        error_body = f"Internal Server Error\n\n{error_msg}\n\nPlease check the function logs for details."
        try:
            from vercel import Response
            return Response(
                error_body.encode('utf-8'),
                status=500,
                headers={'Content-Type': 'text/plain; charset=utf-8'}
            )
        except ImportError:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain; charset=utf-8'},
                'body': error_body
            }
