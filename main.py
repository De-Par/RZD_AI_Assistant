import flet
from core.frontend import app


if __name__ == '__main__':
    flet.app(
        target=app,
        assets_dir="./core/frontend/assets"
    )
