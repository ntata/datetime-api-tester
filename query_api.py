import json, requests, time, datetime
import sched
import signal
import sys

api_base_url = 'http://127.0.0.1:5000/'
headers = {'Content-Type': 'application/json'}
scheduler = sched.scheduler()


def display_current_time():
    api_url = '{0}api/v1/timenow'.format(api_base_url)
    start = datetime.datetime.now()
    response = requests.get(api_url, headers=headers)
    end = datetime.datetime.now()
    return {
            'response': json.loads(response.content.decode('utf-8')),
            'ttfb': str(response.elapsed),
            'ttlb': str(end-start),
            'status': response.status_code
            }

def display_current_time_with_tz():
    api_url = '{0}api/v2/timenow'.format(api_base_url)
    start = datetime.datetime.now()
    response = requests.get(api_url, headers=headers)
    end = datetime.datetime.now()
    return {
            'response': json.loads(response.content.decode('utf-8')),
            'ttfb': str(response.elapsed),
            'ttlb': str(end-start),
            'status': response.status_code
            }

def timed_call(calls_per_second, func):
    period = 1.0/calls_per_second
    def query_api():
        print(func())
        scheduler.enter(period, 0, query_api)
    scheduler.enter(period, 0, query_api)


def signal_handler(sig, frame):
    print('bye! have a good day!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    timed_call(4, display_current_time)
    #timed_call(4, display_current_time_with_tz)
    scheduler.run()

main()

