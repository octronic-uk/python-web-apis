from octronic.webapis.user import UserAPI
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UserAPI.app.run(debug=True)
