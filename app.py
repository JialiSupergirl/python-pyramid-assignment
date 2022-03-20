from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import db

def getMenu():
    menuList=[]
    cur = db.getConnection()
    query = cur.execute("SELECT `menuTexte`,`order` FROM `menuitem` where `menu` = 'main' order by `order`")    
    results = cur.fetchall()
    db.closeConn(cur)   
    for result in results:
        menuList.append(result[0])
    return menuList

def getPage():
    page ={"title":[], "content":[]}
    cur = db.getConnection()
    query = cur.execute("SELECT `pageId`,`title`,`content`,`pageName`,`script` FROM `page`")    
    results = cur.fetchall()
    db.closeConn(cur) 
    for result in results:
        page["title"].append(result[1])
        page["content"].append(result[2])
    return page

@view_config(
    route_name='home',
    renderer="templates/home.jinja2"
) 
def home(request):
    items=getMenu()
    page = getPage()
    pageTitle = page.get("title")[0]
    return{"items":items,"title":pageTitle}
   
@view_config(
    route_name='destination',
    renderer="templates/destination.jinja2"
)
def destination(request):
    items=getMenu()
    page = getPage()
    pageTitle = page.get("title")[1]
    return{"items":items,"title":pageTitle}

if __name__ == '__main__':
    
    with Configurator() as config:
        config.include('pyramid_jinja2')
        config.include('pyramid_debugtoolbar')
        config.add_static_view(name='static',
            path='static')

        config.add_route('home', '/Home')
        config.add_route('destination', '/Destination')

        config.scan()

        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6540, app)

    server.serve_forever()  
