from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!" 
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola! <a href = '/hello' >Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                

                output = ""
                output += "<html><body>"
                output += "<a href = '/restaurants/new' >Make a new restaurant here</a>"
                output += "</br>"
                output += "</br>"
                for r in restaurants:
                    output += r.name
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/edit'>Edit</a>" % r.id
                    output += "</br>"
                    output += "<a href = '/restaurants/%s/delete'>Delete</a>" % r.id
                    output += "</br>"
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' >"
                output += "<input type='submit' value='Create'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split('/')[-2]
                print restaurant_id

                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<input name='newRestaurantName' type='text' placeholder = '%s' >" % restaurant.name
                output += "<input type='submit' value='Rename'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split('/')[-2]
                print restaurant_id

                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete %s?</h1>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<input type='submit' value='Delete'> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    restaurant_id = self.path.split('/')[-2]
                    print restaurant_id

                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

                    restaurant.name = messagecontent[0]                    
                    session.add(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers() 
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':

                    restaurant_id = self.path.split('/')[-2]
                    print "deleting" + restaurant_id

                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()                
                    session.delete(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers() 
            if self.path.endswith("/restaurants/new"):  
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')                   
                    
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/hello") or self.path.endswith("/hola"):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')                    

                    output = ""
                    output += "<html><body>"
                    output += "<h2> Okay, how about this: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]

                    output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>in POST</h2><input name='message' type='text' ><input type='submit' value='Submit'> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server runing on port %s" % port
        server.serve_forever()


    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()