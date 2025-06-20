# Web Starter Template

A modern Python web application starter template built with Werkzeug and Jinja2.

## Features

- 🚀 Modern Python 3.13+ codebase
- 🛡️ Proper error handling (404, 405, 500 responses)
- 📝 Comprehensive logging system
- ⚙️ Environment-based configuration
- 🧪 Full test coverage with pytest
- 🎨 Jinja2 templating with autoescape
- 🔧 Clean, modular architecture

## Requirements

- Python >= 3.13
- Dependencies are managed in `requirements.txt` and `pyproject.toml`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd web_starter_template
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install test dependencies (optional):
```bash
pip install -e ".[test]"
```

## Project Structure

```
web_starter_template/
├── webapp/                    # Main application code
│   ├── __init__.py
│   ├── webapp.py             # Application entry point
│   ├── urls.py               # URL routing configuration
│   ├── config.py             # Configuration management
│   ├── lib/                  # Core libraries
│   │   ├── __init__.py
│   │   ├── baseapp.py        # WSGI application base
│   │   └── render.py         # Jinja2 template renderer
│   └── endpoint/             # Request handlers
│       ├── __init__.py
│       └── home.py           # Homepage endpoint
├── site_content/             # Static content and templates
│   ├── static/               # Static files (CSS, JS, images)
│   └── templates/            # Jinja2 templates
│       └── html/
│           └── landing.html  # Homepage template
├── tests/                    # Test suite
│   ├── test_baseapp.py
│   ├── test_config.py
│   ├── test_home.py
│   ├── test_integration.py
│   ├── test_render.py
│   └── test_urls.py
├── requirements.txt          # Python dependencies
└── pyproject.toml           # Project configuration

```

## Usage

### Running the Development Server

```bash
cd webapp
python webapp.py
```

The server will start on `http://localhost:8080` with auto-reloading and debugging enabled.

### Configuration

The application supports environment-based configuration through the `WEBAPP_ENV` variable:

```bash
# Development mode (default)
python webapp.py

# Production mode
WEBAPP_ENV=production python webapp.py
```

Configuration options:
- **Development**: Debug mode, localhost, port 8080, DEBUG logging
- **Production**: No debug, 0.0.0.0, port 8080, WARNING logging

### Adding New Endpoints

1. Create a new endpoint file in `webapp/endpoint/`:
```python
from werkzeug.wrappers import Response
from webapp.lib.render import renderer

def my_endpoint(req):
    return Response(renderer.render('html/my_template.html'), mimetype='text/html')
```

2. Add the route in `webapp/urls.py`:
```python
from webapp.endpoint.my_endpoint import my_endpoint

def make_url_map():
    return Map([
        Rule('/', endpoint=homepage, strict_slashes=False),
        Rule('/my-route', endpoint=my_endpoint),
    ])
```

## Testing

Run all tests:
```bash
python -m pytest
```

Run with coverage:
```bash
python -m pytest --cov=webapp
```

Run specific test file:
```bash
python -m pytest tests/test_baseapp.py -v
```

## Deployment

For production deployment:

1. Set environment variable:
```bash
export WEBAPP_ENV=production
```

2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn webapp.webapp:application
```

3. Place behind a reverse proxy (nginx, Apache) for static file serving and SSL termination.

## Development

### Code Style

The project uses `ruff` for linting and formatting. Format code with:
```bash
ruff check --fix .
ruff format .
```

### Adding Dependencies

Add new dependencies to `requirements.txt`:
```bash
echo "package-name" >> requirements.txt
pip install -r requirements.txt
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]