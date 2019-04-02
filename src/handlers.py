import aiohttp
from aiohttp import web


app = web.Application()



async def websocket_handler(request):
    
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(msg.data)
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
    print('websocker connection closed')

    return ws

app.add_routes([web.get('/ws', websocket_handler)])
web.run_app(app)
