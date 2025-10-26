import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Serve the frontend static files from the sibling `frontend/` directory so
# running this single backend process will host both the API and the UI.
frontend_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app = Flask(__name__, static_folder=frontend_path, static_url_path="")
CORS(app)


@app.route("/")
def root():
    # Serve the frontend index.html as the root page
    return app.send_static_file("index.html")


# Register API blueprints
try:
    from backend.routes.api import api_bp
except Exception:
    # Fallback for different import contexts
    try:
        from routes.api import api_bp
    except Exception:
        # Last resort: import via importlib if needed
        raise

app.register_blueprint(api_bp, url_prefix="/api")


@app.errorhandler(404)
def spa_fallback(e):
    """Fallback to index.html for unknown routes (useful for SPA routing).

    Note: API routes under /api/ will return normal 404s; this fallback is
    primarily for frontend paths handled client-side.
    """
    # If request was likely for an API route, return the original error
    # (flask will handle it). Otherwise, send index.html so client-side
    # router can handle the path.
    return app.send_static_file("index.html")


if __name__ == "__main__":
    # Bind to all interfaces for easy local testing inside containers if needed
    app.run(host="0.0.0.0", port=5000, debug=True)
