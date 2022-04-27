from flask import Flask, jsonify, send_from_directory
import apis as api

# общие настройки
app = Flask(__name__, static_folder='templates/static')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
error_404 = {'status': {'message': 'Not Found', 'status_code': 404}}
error_500 = {'status': {'message': 'Internal Server Error', 'status_code': 500}}
error_503 = {'status': {'message': 'Service Unavailable', 'status_code': 503}}

# чтение файлов на хосте
@app.route('/<path:name>')
async def download_file(name):
    return send_from_directory("./data/", name, as_attachment=False)

# трекеры ошыбок
@app.errorhandler(404)
async def page_not_found(e):
    return jsonify(error_404)

@app.errorhandler(500)
async def page_not_found(e):
    return jsonify(error_500)

@app.errorhandler(503)
async def page_not_found(e):
    return jsonify(error_503)

# ссылки
@app.route('/')
async def welcome():
    return await api.as_welcome()

@app.route('/docs')
async def docs():
    return await api.as_docs()

@app.route('/apis')
async def apis():
    return await api.as_apis()

@app.route('/gif/<string:id>')
async def get_gif(id):
    return await api.as_get_gif(id)

@app.route('/nsfw/<string:id>')
async def get_nsfw(id):
    return await api.as_get_nsfw(id)

@app.route('/meme/random')
async def get_meme():
    return await api.as_get_meme()

@app.route('/anime/random')
async def get_anime():
    return await api.as_get_anime()

@app.route('/hentai/random')
async def get_hentai():
    return await api.as_get_hentai()

@app.route('/anime/<string:type>/<string:id>')
async def get_anime_type(type, id):
    return await api.as_get_anime_type(type, id)

@app.route('/hentai/<string:type>/<string:id>')
async def get_hentai_type(type, id):
    return await api.as_get_hentai_type(type, id)

@app.route('/anime/find/<string:lang>/<string:id>')
async def get_anime_find(lang, id):
    return await api.as_get_anime_find(lang, id)

@app.route('/hentai/find/<string:id>')
async def get_hentai_find(id):
    return await api.as_get_hentai_find(id)

# @app.after_request
# async def add_header(response):
#     return await api.as_requests(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')