# Tech Support Bot

A [TG bot](https://t.me/across_tech_bot) for creating tickets, viewing ticket status for Technical Support Service and fetching articles from Knowledge Base from HelpDeskEddy.

## FEATURES

- Receive tech support requests
- Provide contact info to users
- Send support tickets to HelpDeskEddy via API
- Receive ticket status update from HelpDeskEddy via API
- Receive FAQ articles from HelpDeskEddy via API (in progress)

## DEPENDENCIES

- [aiogram](https://github.com/aio-libs/aiohttp)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [aiosqlite](https://github.com/aiosqlite/aiosqlite)
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- [flask](https://github.com/pallets/flask)
- [nginx](https://www.nginx.com/)

## INSTALLATION

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install nginx
```

## NGINX server configuration

1. Add the following to `/etc/nginx/sites-available/default`:

```nginx
server {
    listen 80;
    server_name {input public IP address here};

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. Restart Nginx: ```sudo systemctl restart nginx```