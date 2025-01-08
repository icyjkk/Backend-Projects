from flask import Blueprint, request, jsonify, current_app
from app.url.url_service import UrlService

# Define the 'url' blueprint with a URL prefix '/url'
url_bp = Blueprint('url', __name__, url_prefix='/url')

@url_bp.route('/test', methods=['GET'])
def get_test():
    """Simple endpoint to verify service functionality."""
    return UrlService.get_test()

@url_bp.route('/shorten', methods=['POST'])
def post_shorten():
    """Simple endpoint to verify service functionality."""
    return UrlService.post_shorten(request)

@url_bp.route('/shorten/<short_code>', methods=['GET'])
def get_shorten(short_code):
    """Endpoint to retrieve original URL using a short code."""
    return UrlService.get_shorten(short_code)

@url_bp.route('/shorten/<short_code>', methods=['PUT'])
def put_shorten(short_code):
    """Endpoint to retrieve original URL using a short code."""
    return UrlService.put_shorten(short_code,request)

@url_bp.route('/shorten/<short_code>', methods=['DELETE'])
def delete_shorten(short_code):
    """Endpoint to delete a short code."""
    return UrlService.delete_shorten(short_code)

@url_bp.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
    """Endpoint to get access count for a short code."""
    return UrlService.get_stats(short_code)

