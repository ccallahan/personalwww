import reflex as rx
import os

config = rx.Config(
    app_name="personalwww",
    api_url=os.getenv("API_URL", "https://www.chancecallahan.com"),
    deploy_url=os.getenv("DEPLOY_URL", "https://www.chancecallahan.com"),
    backend_port=8080,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
