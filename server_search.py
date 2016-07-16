# This file provided by Facebook is for non-commercial testing and evaluation
# purposes only. Facebook reserves all rights not expressly granted.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import os
import time
import requests
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('search.html'))


def with_read():
    datas = []
    with open('comments.json', 'r') as f:
        datas = json.loads(f.read())
    return datas

def with_write(datas):
    with open('comments.json', 'w') as f:
        f.write(json.dumps(datas, indent=4, separators=(',', ': ')))

def star_gte_8(data):
    return int(float(data.get('rating',{}).get('average',0))) >= 8

def format_data(books):
    datas = []
    for b in books:
        datas.append({
            'name': b.get('title', ''),
            'author': ', '.join(b.get('author', [])),
            'star': b.get('rating', {}).get('average', 0),
            'image': b.get('image', ''),
        })
    return datas


@app.route('/api/comments', methods=['GET', 'POST'])
def comments_handler():
    comments = with_read()

    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['id'] = int(time.time() * 1000)
        new_comment.setdefault('nowTime', time.strftime('%Y-%m-%d %H:%M:%S'))
        comments.append(new_comment)
        with_write(comments)

    return Response(
        json.dumps(comments),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

@app.route('/api/db_book_search', methods=['GET', 'POST'])
def db_book_search():
    books = []

    if request.method == 'POST':
        form_data = request.form.to_dict()
        print form_data
        payload = {'q': form_data.get('filterText', ''), 'count': 10}

        try:
            r = requests.get('https://api.douban.com/v2/book/search', params=payload)
            books = r.json().get('books',[])
            if form_data.get('in8StarOnly', 'false') == 'true':
                books = filter(star_gte_8, books)
            print books
            books = format_data(books)
            print books
        except Exception, e:
            print e

    return Response(
        json.dumps(books),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get("PORT", 3000)))
