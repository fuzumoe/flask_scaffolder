from app import create_app
from app.config import get_config_name, config_by_name

config_name = get_config_name()
app = create_app(config_name=config_name)
config_class = config_by_name[config_name]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config_class.PORT, debug=app.config.get("DEBUG", True))
