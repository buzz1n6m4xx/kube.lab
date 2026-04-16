FROM nginx:latest

# Copy Nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy static website
COPY public/ /usr/share/nginx/html/
