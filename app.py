import requests
from flask import Flask, render_template, request
import redis
import os
import re
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html',hostname=HOSTNAME)


@app.route('/result/', methods = ['POST','GET'])
def show_result():
	if request.method == 'POST':

		###############################################################
		# Checking Ip is Valid
		###############################################################

		ip = request.form['ip']

		pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		isip = pattern.match(ip.strip())


		if isip:

			try:

				redis_server = redis.StrictRedis(host=REDIS_HOST,
            							port=REDIS_PORT,
										charset="utf-8",
										decode_responses=True)
				redis_status = redis_server.get(ip)


			except:
				return render_template('error.html',reason='Redis Connection Error')

			##########################################################################

			try:

				if redis_status:

					start_time = time.time()
					country = redis_server.get(ip)
					ttl = redis_server.ttl(ip)
					end_time = time.time()

					total_time = end_time - start_time

					return render_template('result.html',cache_status=True,time_taken='{:.2f}'.format(total_time),ttl_time=ttl,ip=ip,country=country)
				
				else:
					start_time = time.time()

					url = 'http://api.ipstack.com/{}?access_key={}'.format(ip,IPSTACK_KEY)
					country = requests.get(url).json()['country_name']
					redis_server.set(ip,country,ex=REDIS_CACHE)

					end_time = time.time()

					total_time = end_time - start_time
					return render_template('result.html',cache_status=False,time_taken='{:.2f}'.format(total_time),ttl_time=REDIS_CACHE,ip=ip,country=country)

			except:
				return render_template('error.html',reason=' Ipstack is not reachable')	
		else:

			return render_template('error.html',reason=' {} Not a vaild ipv4 address'.format(ip))



	

if __name__ == '__main__':

	HOSTNAME = os.getenv('HOSTNAME' ,'Unable to find hostname')
	
	REDIS_HOST = os.getenv('REDIS_HOST')
	REDIS_PORT = os.getenv('REDIS_PORT',6379)
	REDIS_CACHE = os.getenv('REDIS_CACHE',300)
	FLASK_PORT = os.getenv('FLASK_PORT',8080) 
	IPSTACK_KEY = os.getenv('IPSTACK_KEY')
	app.run(host='0.0.0.0',port=FLASK_PORT,debug=True)
    