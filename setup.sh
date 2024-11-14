#!/bin/bash

# Update and install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y nginx apache2-utils docker docker-compose python3-venv nginx

# Setup Python virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Docker services
sudo systemctl start docker
sudo systemctl enable docker

# Configure /etc/nginx/.htpasswd
echo "Enter password for ftp.across.ru webhook access:"
sudo htpasswd -c /etc/nginx/.htpasswd across

# Test the configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

echo "Setup completed successfully!"