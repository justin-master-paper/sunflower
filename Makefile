default:
	gunicorn -w 4 -b 127.0.0.1:8000 index:application

debug:
	gunicorn -w 4 -b 127.0.0.1:8000 index:application --log-level debug --reload 
