import http.client
import ssl
import json
import base64
import urllib.parse
import argparse
import logging
import time

parser = argparse.ArgumentParser()
parser.add_argument(
        "--portnum",
        default=5000,
        type=int,
        help="port number of server"
        )
args = parser.parse_args()

hostname = '127.0.0.1'
portnum = args.portnum
timeout_secs = 1000000000
logger = logging.getLogger(__name__)


conn = http.client.HTTPConnection(host=hostname, port=portnum, timeout=timeout_secs)
headers = {}
# params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})

#3. Similarity request
logging.basicConfig(level = logging.INFO)
logger.info("***** Connecting server *****")
try:
    conn_flag = 1
    expect = "Authentication Succeeding!"
    # while (conn_flag):
    #     account_id = input("ID: ")
    #     password = input("Password: ")
    #     params = str(account_id + "&" + password)
    #     conn.request('POST', '', params, headers=headers)
    #     r = conn.getresponse()
    #     response_str = r.read().decode('utf-8').strip()
    #     if response_str == expect:
    #         print("Authentication Succeeding!")
    #         conn_flag = 0
    #     else:
    #         conn_flag = 1
    while(1):
        input_sentence = input('Target sentence: ').strip()
        if input_sentence == "&&Stop":
            break

        start = time.time()
        print("processing...")
        body = input_sentence
        conn.request(method='GET', url='/similar?question=what+is+vsan', body=body, headers=headers)
        r = conn.getresponse()
        response_str = r.read().decode('utf-8')
        end = time.time()
        logger.info("***** one paraphrasing time: {} *****".format(str(end-start)))
        print("ANSWERS RESPONSE = \n", response_str[:200000000000])
except http.client.HTTPException:
    print("Failed connection")


