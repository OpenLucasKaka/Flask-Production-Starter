from app import create_app
from app.extensions.extensions import db
from app.utils.env_validator import EnvironmentValidator
import click

# 在应用启动前验证环境变量
EnvironmentValidator.set_defaults()
EnvironmentValidator.validate()

app = create_app()
@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

# @app.cli.command
# @click.argument('test_name', nargs=1)
# def test(test_name):
#     return

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

