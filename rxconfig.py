import reflex as rx
import os

config = rx.Config(
    app_name="personalwww",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    show_built_with_reflex=False,
)
