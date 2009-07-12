all:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  local .... runs the webapp locally"
	@echo "  test ..... tests the webapp running on the localhost"
	@echo "  upload ... uploads the webapp to the google app engine"

local:
	dev_appserver.py .

upload:
	appcfg.py update .
