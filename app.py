from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import db

def getMenu():
    menuList=[]
    cur = db.getConnection()
    query = cur.execute("SELECT label, `type`, pageKey, externalURL FROM `menu` WHERE menuName = 'main' ORDER by `order`")    
    results = cur.fetchall()
    db.closeConn(cur)   
    for result in results:
        menuList.append(result[0])
    return menuList

@view_config(
    route_name='home',
    renderer="templates/home.jinja2"
) 
def home(request):
    items=getMenu()
    return{"items":items}
    

if __name__ == '__main__':
    
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_debugtoolbar')
        # config.add_static_view()

        config.add_route('home', '/')

        config.scan()

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6500, app)

    server.serve_forever()  
