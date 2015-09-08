import os, json, argparse, random
import asyncio
from aiohttp.web import Application, Response, MsgType, WebSocketResponse

DIR = os.path.dirname(__file__)
WS_FILE = os.path.join(DIR, 'client.html')


# define game tokens
suits = ["red", "green", "blue", "yellow", "white"]
values = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]

DEFAULT = []
i = 0
for suit in suits:
    for value in values:
        i += 1
        label = "card{}".format(i)
        DEFAULT += [[label, 250, 10, "draggable card "+suit+" facedown", str(value)]]
random.shuffle(DEFAULT)
DEFAULT+= [["b"+n, 260, 100, "draggable blue token", ""] for n in "12345678"]
DEFAULT+= [["r"+n, 260, 200, "draggable red token", ""] for n in "123"]
DEFAULT+= [["stash"+str(n), 0, 0, "stash", "Player "+str(n+1)] for n in range(5)]
DEFAULT+= [["scored", 0, 0, "stash", "Score Area"] for n in range(1, 6)]
STATE = DEFAULT[:]


@asyncio.coroutine
def wshandler(request):
    global STATE

    resp = WebSocketResponse()
    ok, protocol = resp.can_start(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return Response(body=fp.read(), content_type='text/html')

    sockets = request.app['sockets']
    sockets.append(resp)

    resp.start(request)
    resp.send_str( str(sockets.index(resp)) + json.dumps(STATE) )

    while True:
        msg = yield from resp.receive()

        if msg.tp == MsgType.text:
            STATE += json.loads(msg.data)
            for i, ws in enumerate(sockets):
                ws.send_str(str(i)+msg.data)
        else:
            break

    sockets.remove(resp)

    if len(sockets) == 0:
        STATE = DEFAULT[:]

    return resp


@asyncio.coroutine
def init(loop, host, port):
    app = Application(loop=loop)
    app['sockets'] = []
    app.router.add_route('GET', '/', wshandler)
    app.router.add_static('/static', 'static/')

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, host, port)
    print("Server started at http://{}:{}".format(host, port))
    return app, srv, handler


@asyncio.coroutine
def finish(app, srv, handler):
    for ws in app['sockets']:
        ws.close()
    app['sockets'].clear()
    yield from asyncio.sleep(0.1)
    srv.close()
    yield from handler.finish_connections()
    yield from srv.wait_closed()


parser = argparse.ArgumentParser(description='Teburu Server')
parser.add_argument("-t", "--host", type=str, default='0.0.0.0', required=False)
parser.add_argument("-p", "--port", type=int, default=8080, required=False)
opts = parser.parse_args()


loop = asyncio.get_event_loop()
app, srv, handler = loop.run_until_complete(init(loop, opts.host, opts.port))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(finish(app, srv, handler))
