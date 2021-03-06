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
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


def with_read():
    datas = []
    with open('comments.json', 'r') as f:
        datas = json.loads(f.read())
    return datas

def with_write(datas):
    with open('comments.json', 'w') as f:
        f.write(json.dumps(comments, indent=4, separators=(',', ': ')))


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
    pass


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))
