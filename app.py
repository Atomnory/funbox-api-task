import time
from flask import Flask, jsonify, request, abort
from service import handle_links, handle_interval

app = Flask(__name__)

# TODO: add Tests

# visited_links = {
#     'links': [
#         "https://ya.ru",
#         "https://ya.ru?q=123",
#         "funbox.ru",
#         "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
#     ]
# }

# database = {
#     1: ['ya.ru', 'google.com', 'gmail.google.com', 'bbc.co.uk'],
#     2: ['google.com', 'bbc.co.uk'],
#     10: ['ya.ru']
# }

# domains = {
#     "domains": [
#         "ya.ru",
#         "funbox.ru",
#         "stackoverflow.com"
#     ],
#     "status": "ok"
# }

# curl -i -H "Content-Type: application/json" -X POST -d '{"links":["https://ya.ru", "https://ya.ru?q=123", "funbox.ru", "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"]}' http://127.0.0.1:5000/visited_links
# curl -i -X GET 'http://127.0.0.1:5000/visited_domains?from=1642593150&to=1642593200' 
@app.route('/visited_links', methods=['POST'])
def post_visited_links():
    if not request.json:
        abort(400)
    response = handle_links(request.json['links'], int(time.time()))
    return jsonify(response)

@app.route('/visited_domains', methods=['GET'])
def get_visited_domains():
    response = handle_interval(int(request.args.get('from')), int(request.args.get('to')))
    return jsonify(response)
