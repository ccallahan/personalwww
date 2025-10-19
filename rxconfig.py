import reflex as rx
import os

config = rx.Config(
    app_name="personalwww",
    api_url=os.getenv("API_URL", "https://www.chancecallahan.com"),
    deploy_url=os.getenv("DEPLOY_URL", "https://www.chancecallahan.com"),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)