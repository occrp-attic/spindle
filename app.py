from schwifty.core import app
from schwifty.settings import DEBUG, HTTP_HOST, HTTP_PORT

if __name__ == '__main__':
    print "Getting Schwifty!"
    app.run(debug=True, host=HTTP_HOST, port=HTTP_PORT)
    print "I like what you've got!"
