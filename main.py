import webapp2
from views import (
    MainPage,
    Results,
    History
)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/compare', Results),
    ('/history', History)], debug=True
)


def main():
    application.RUN()


if __name__ == '__main__':
    main()
