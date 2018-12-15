import bottle
import routes

app = routes.app

if __name__ == '__main__':
    # this setting is running for development.
    bottle.run(app=app, host='0.0.0.0',port=8080, reloader=True, debug=True)
