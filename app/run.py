#   runs the Flask application instance created by __init__.py
from app import create_app
from app.configs import set_config
from devkit import func_speedtest
from app.main.machine_learning_pipeline import TweetsClassificationPipeline

app = func_speedtest(create_app, config=set_config(select=False), iterations=1, cl_label='APP READY IN')

if __name__ == '__main__':
	app.run()
