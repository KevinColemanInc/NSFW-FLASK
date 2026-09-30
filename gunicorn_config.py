import os


# Coolify provides the port through the PORT environment variable. Keep 8080 as
# the default so the app also works with the existing Fly and local setup.
bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"

# Each Gunicorn worker loads its own TensorFlow model. A single worker is the
# safest default for the 2 GB deployments documented by this project; increase
# WEB_CONCURRENCY only when the host has sufficient memory.
workers = int(os.environ.get("WEB_CONCURRENCY", "1"))
