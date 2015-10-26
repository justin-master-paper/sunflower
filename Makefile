default:
	gunicorn -w 4 -b 0.0.0.0:8080 index:application

debug:
	gunicorn -w 4 -b 0.0.0.0:8080 index:application --log-level debug --reload 
