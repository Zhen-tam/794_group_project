import http
import ssl
import time
import json
import base64
from urllib.parse import urlparse, parse_qs
from io import BytesIO
import os

from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    #https://gist.github.com/fxsjy/5465353
    def do_AUTHHEAD(self):
        print("--------------------- send Auth Request ------------------")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers',
                         'Origin, X-Requested-With, Content-Type, Accept, Authorization')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        response1 = bytes("Authentication Failing!", 'utf-8')
        response2 = bytes("Authentication Succeeding!", 'utf-8')
        content_length = int(self.headers['Content-Length'])
        post_body = str(self.rfile.read(content_length))
        new_id, new_password = post_body.strip("b").strip("'").split("&")
        new_id = new_id.strip()
        new_password = new_password.strip()
        with open('cache.txt', 'r') as content_file:
            content_file = content_file.readlines()
            account_id, password = content_file
            account_id = account_id.strip()
            password = password.strip()

            if account_id != new_id or password != new_password:
                self.wfile.write(response1)
                return
            self.wfile.write(response2)

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        #print("Post Header = [%s]"%str(self.headers))
        #print("Post Body = [%s]"%str(body))

        print("--------- GET Path = %s -----------"% self.path)

        #Need to change login URL from GET to POST.
        #Send authorization key in response, when login work, else return error.

        #Logout - need to change Get to delete
        print("body: {}".format(str(body)))
        body = str(body).strip("b").strip("'").split('#')

        pre_train_path = body[0].strip()
        data_path = body[1].strip()
        corpus_path = body[2].strip()
        input_sentence = body[3].strip().replace(" ", "_")

        print("input_sentence: {}".format(input_sentence))
        if(urlparse(self.path).path == '/similar'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            #path = urlparse(self.path).path
            #query_components = parse_qs(urlparse(self.path).query)
            #response_str = 'path=%s query components=%s\n'%(path, query_components)
            cmd = "python" + " ../run_glue.py   " + \
                             "--model_type bert   " \
                             "--model_name_or_path bert-base-cased   " \
                             "--task_name MRPC   " \
                             "--do_eval   " \
                             "--do_lower_case   " \
                             "--data_dir " + data_path + "   " \
                             "--max_seq_length 128   " \
                             "--per_gpu_train_batch_size 32   " \
                             "--learning_rate 2e-5   " \
                             "--num_train_epochs 3.0   " \
                             "--output_dir " + pre_train_path + " " \
                             "--overwrite_output_dir   " \
                             "--paraphrase_corpus " \
                             "--input_file_path " + corpus_path +"   " \
                             "--overwrite_output_dir   " \
                             "--input_sentence   " + input_sentence
            os.system(cmd)
            output_path = os.path.join(
                data_path,
                'outfile.txt'
            )
            with open(output_path, 'r') as content_file:
                json_content = content_file.read()
                response = bytes(json_content, 'utf-8')
                self.wfile.write(response)
                print("Sending ...", json_content[:200000000000000])

        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
        self.end_headers()
            
        
httpd = HTTPServer(('0.0.0.0', 5000), SimpleHTTPRequestHandler)


httpd.serve_forever()

        

