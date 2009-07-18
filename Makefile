all:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  local .... runs the webapp locally"
	@echo "  test ..... tests the webapp running on the localhost"
	@echo "  test-remote ..... tests the webapp on the web"
	@echo "  upload ... uploads the webapp to the google app engine"

local:
	python2.5 manage.py runserver

test:
	python test_app.py localhost:8000

test-remote:
	python test_app.py sympy2.appspot.com

upload:
	python2.5 .google_appengine/appcfg.py update .
