# youtube_django_app

# Docker Instructions

1. docker build -t youtube-selective-dashboard -f Dockerfile .
2. docker run -it -p 8888:8888 youtube-selective-dashboard


# API URLS


1. Fetch all videos with pagination: http://127.0.0.1:8888/api
2. Search API with pagination: http://127.0.0.1:8888/search_api?title=cricket&description=england
