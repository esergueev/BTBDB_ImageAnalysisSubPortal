import os
from app.backend import app_flask

def runapp():
    port = int(os.environ.get('PORT', 7777))
    print ('Go to URL: http://localhost:%d' % port)
    app_flask.run(host='0.0.0.0', port=port, debug=True)
    # socketio.run(app_flask, port=port, debug=False, host='0.0.0.0')

if __name__ == '__main__':
    runapp()
