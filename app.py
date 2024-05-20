import json

from flask import Flask, jsonify, abort
from typing import Tuple

app = Flask(__name__)


def data_loader() -> Tuple[dict, dict]:
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as file:
            posts_data = json.load(file)['posts']
    except FileNotFoundError:
        posts_data = {}
    try:
        with open('data/comments.json', 'r', encoding='utf-8') as file:
            comments_data = json.load(file)['comments']
    except FileNotFoundError:
        comments_data = {}
    return posts_data, comments_data


@app.route("/")
def get_posts():
    posts, comments = data_loader()

    comments_count = {}
    for comment in comments:
        try:
            comments_count[comment['post_id']] += 1
        except KeyError:   # Либо проверить на наличие ключа через in
            comments_count[comment['post_id']] = 1

    result_posts = []
    for post in posts:
        result_posts.append({
            "id": post['id'],
            "title": post['title'],
            "body": post['body'],
            "author": post['author'],
            "created_at": post['created_at'],
            "comments_count": comments_count.get(post['id'], 0)
        })

    output = {"posts": result_posts,
              "total_results": len(result_posts)}

    return jsonify(output)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    posts, comments = data_loader()

    posts_dict = {post['id']: post for post in posts}
    if posts_dict.get(post_id):
        post = posts_dict[post_id]
        response = {
            "id": post['id'],
            "title": post['title'],
            "body": post['body'],
            "author": post['author'],
            "created_at": post['created_at'],
            "comments": [comment for comment in comments if comment['post_id'] == post['id']]
        }
        return jsonify(response)
    else:
        return abort(404)
