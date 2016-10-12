import tornado.ioloop
import tornado.web
import tornado.httpserver
import uuid
import subprocess
import os, sys
import stat
from stat import *

def secure_iquery(username, password, query):
  auth_filename = '/tmp/' + str(uuid.uuid4())
  auth_file = open(auth_filename, 'w')
  auth_file.write("[security_password]\n")
  auth_file.write("user-name="+username+"\n")
  auth_file.write("user-password="+password+"\n")
  auth_file.close()
  os.chmod(auth_filename, stat.S_IRUSR)
  filename = '/tmp/' + str(uuid.uuid4())
  p = subprocess.Popen("/opt/scidb/15.12/bin/iquery" + " --auth-file=" + auth_filename  + " -anq " + " \"aio_save("+query+",'"+filename+".tsv','format=tsv')\"", stdout=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  p_status = p.wait()
  #myoutput = open(filename + '.tsv').readlines()
  with open(filename+'.tsv', 'r') as content_file:
    myoutput = content_file.read()
  os.remove(filename + ".tsv")
  os.remove(auth_filename)
  return myoutput

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<!DOCTYPE html>
<html>
<body>

<form action="/" method="post">
  username:   <input type="text" name="username" value="root"><br>
  password:   <input type="password" name="password"><br>
  iquerytxt:  <textarea id="iquerytxt" name="iquerytxt" style="width:100%; height: 70px;"></textarea><br>
  <input type="submit" value="Submit">
</form>

<p>Click on the submit button to run scidb query</p>

</body>
</html>''')
 
    def post(self):
        self.set_header("Content-Type", "text/plain")
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        query = self.get_body_argument("iquerytxt")
        print(query)
        myoutput = secure_iquery(username, password, query)
        self.write(''.join(myoutput))

class GetVariantsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<!DOCTYPE html>
<html>
<body>
Please select the genomic region
<form action="/get_variants" method="post">
  username:   <input type="text" name="username" value="root"><br>
  password:   <input type="password" name="password"><br>
  chromosome: <input type="text" name="chromosome" value="7"><br>
  start:      <input type="text" name="start"      value="123456"><br>
  end:        <input type="text" name="end"        value="234567"><br>
  limit:      <input type="text" name="limit"      value="1000000"><br>
  <input type="submit" value="Submit">
</form>
<p>Click on the submit button to run scidb query</p>
</body>
</html>''')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        chromosome = self.get_body_argument("chromosome")
        chromosome = str(int(chromosome) - 1)
        start = self.get_body_argument("start")
        end = self.get_body_argument("end")
        limit = 100000
        try:
            limit = self.get_body_argument("limit")
        except tornado.web.MissingArgumentError:
            limit = 100000 
        query = "between(GEUV_VARIANT,"+chromosome+",null,"+start+",null,"+chromosome+","+end+",null,null)"
        query = "apply("+query+", chromosome, chromosome_id+1, start_position, start)"
        query = "project("+query+", chromosome, start_position, reference, alternate, id, info)"
        if int(limit)>0:
            query = "limit("+query+","+limit+")"
        myoutput = secure_iquery(username, password, query)
        self.write(''.join(myoutput))

class ListArraysHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''<!DOCTYPE html>
<html>
<body>
Please select the genomic region
<form action="/list_arrays" method="post">
  username:   <input type="text" name="username" value="root"><br>
  password:   <input type="password" name="password"><br>
  <input type="submit" value="Submit">
</form>
<p>Click on the submit button to run scidb query</p>
</body>
</html>''')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        myoutput = secure_iquery(username, password, "project(list(), uaid, name)")
        self.write(''.join(myoutput))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/get_variants",GetVariantsHandler),
        (r"/list_arrays",ListArraysHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app, ssl_options={
        "certfile": "/home/scidb/p4scratch/scidb-restful-tornado/server.crt",
        "keyfile": "/home/scidb/p4scratch/scidb-restful-tornado/server.key",
    })
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()

