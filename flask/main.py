

from flask_methods import create_app


if __name__ == "__main__":
    local_app = create_app()
    local_app.run(host='0.0.0.0')  # listens on public network interface
