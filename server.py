import os, json, argparse, random, string, collections
import asyncio
from aiohttp.web import Application, Response, MsgType, WebSocketResponse

DIR = os.path.dirname(__file__)
WS_FILE = os.path.join(DIR, 'client.html')
SPEC_FILE = os.path.join(DIR, 'static', 'games', 'hanabi.json')

USERMAP = collections.OrderedDict()

def restart_game():
    with open(SPEC_FILE) as fp:
        global GAME
        GAME = json.load(fp)
        USERMAP.clear()

def update_id_info(sockets):
    n = len(sockets)
    for i, (k, ws) in enumerate(USERMAP.items(), 1):
        info = [i, n, k]
        try:
            ws.send_str(json.dumps({"info":info}))
        except RuntimeError:
            pass


@asyncio.coroutine
def wshandler(request):

    resp = WebSocketResponse()
    ok, protocol = resp.can_start(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return Response(body=fp.read(), content_type='text/html')

    sockets = request.app['sockets']
    if len(sockets) == 0: restart_game()
    sockets.append(resp)
    resp.start(request)

    # login
    msg = yield from resp.receive()
    keycode = msg.data
    existing = USERMAP.get(keycode)
    if not existing or not existing.closed:
        random.seed(random.SystemRandom())
        keycode = ''.join(random.sample(string.ascii_letters, 32))
    USERMAP[keycode] = resp

    # communicate
    update_id_info(sockets)
    resp.send_str(json.dumps(GAME))

    while True:
        msg = yield from resp.receive()

        if msg.tp == MsgType.text:

            move = json.loads(msg.data)+[len(GAME["moves"])]
            GAME["moves"].append(move)
            for ws in sockets:
                ws.send_str(json.dumps({"moves": [move]}))

        else:
            break

    sockets.remove(resp)
    update_id_info(sockets)
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
