from aiohttp import web
import json
import random
import string
import os


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


async def home(request):
    s = open('main_page.html', 'r')
    return web.Response(text=s.read(), content_type='text/html')


async def make_link(request):
    data = await request.post()
    link = data['link']
    characters = string.ascii_letters + string.digits
    new_link = ''.join(random.choice(characters) for i in range(6))
    new_data = {new_link: link}
    if not is_non_zero_file('links.json'):
        with open('links.json', 'w') as f:
            json.dump(new_data, f, indent=4)
    else:
        with open('links.json', 'r+') as f:
            file_data = json.load(f)
            file_data.update(new_data)
            f.seek(0)
            json.dump(file_data, f, indent=4)
    return web.Response(text=f'http://127.0.0.1:8080/{new_link}')


async def redirect_handler(request):
    new_link = request.match_info['new_link']
    if not is_non_zero_file('links.json'):
        raise web.HTTPNotFound(text=f'No original link for {new_link} found!!!')
    with open('links.json', 'r') as f:
        file_data = json.loads(f.read())
    orig_url = file_data.get(new_link)
    if orig_url is None:
        raise web.HTTPNotFound(text=f'No original link for {new_link} found!')
    raise web.HTTPFound(orig_url)


app = web.Application()
app.add_routes([web.get('/', home)])
app.add_routes([web.post('/', make_link)])
app.add_routes([web.get('/{new_link}', redirect_handler)])
web.run_app(app, host="127.0.0.1")
