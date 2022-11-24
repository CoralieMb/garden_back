from garden_api import create_app
from garden_api.models import db
from werkzeug.middleware.profiler import ProfilerMiddleware

app = create_app()
db.init_app(app)
if __name__ == "__main__":
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [10])
    app.run(debug = True)





 

