from flask import Flask, render_template, request, redirect
from utils import *
from json import JSONDecodeError

# Key variables
POSTS = 'data/data.json'
COMMENTS = 'data/comments.json'
BOOKMARKS = 'data/bookmarks.json'

# Initiate Flask app
app = Flask(__name__, static_folder='static')
app.debug = True


# Key post views
@app.route("/")
def main():
    """Main page with all the posts"""
    posts = get_data(POSTS)
    bookmarks = get_data(BOOKMARKS)
    return render_template('index.html', posts=posts, bookmarks=bookmarks)


@app.route("/posts/<int:post_id>")
def post_by_id(post_id):
    """Page with a specific post"""
    post = get_post_by_id(POSTS, post_id)
    tagged_post = format_post_tags(post)
    comments = get_comments_by_post_id(COMMENTS, post_id)
    return render_template('post.html', post=tagged_post, comments=comments)

# Views by user, tag, search by word
@app.route("/users/<user_name>")
def posts_by_user(user_name):
    """Page with all the posts of the user"""
    posts = get_posts_by_user(POSTS, user_name)
    return render_template('user-feed.html', posts=posts, user_name=user_name)


@app.route("/tag/<tag_name>")
def posts_by_tag(tag_name):
    """Page with all the posts containing the tag"""
    posts_found = get_posts_for_word(POSTS, f'#{tag_name}')
    return render_template('tag.html', posts=posts_found, tag_name=tag_name.capitalize())


@app.route("/search")
def posts_search():
    """Page with all the posts containing some word"""
    searched_word = request.args.get('s')
    posts_found = get_posts_for_word(POSTS, searched_word)
    return render_template('search.html', posts=posts_found)


# Views for bookmarks
@app.route("/bookmarks")
def bookmarks():
    """Page with all posts added to bookmarks"""
    posts = get_data(BOOKMARKS)
    return render_template('bookmarks.html', posts=posts)


@app.route("/bookmarks/add/<int:post_id>")
def bookmarks_add(post_id):
    """Add the post to bookmarks"""
    try:
        bookmarks = get_data(BOOKMARKS)
    except JSONDecodeError:
        # If bookmarks.json is empty, declare empty variable
        bookmarks =[]
    else:
        # Add post to bookmarks if it isn't added already
        post_check = get_post_by_id(BOOKMARKS, post_id)
        if post_check == None:
            post_to_add = get_post_by_id(POSTS, post_id)
            bookmarks.append(post_to_add)
            write_data(BOOKMARKS, bookmarks)
    finally:
        return redirect("/", code = 302)


@app.route("/bookmarks/remove/<int:post_id>")
def bookmarks_remove(post_id):
    """Remove the post from the bookmarks"""
    post_to_remove = get_post_by_id(BOOKMARKS, post_id)
    bookmarks = get_data(BOOKMARKS)
    bookmarks.remove(post_to_remove)
    write_data(BOOKMARKS, bookmarks)
    return redirect("/", code = 302)


# Add a route to display images from uploads folder
# @app.route("/resources/uploads/<path:path>")
# def static_dir(path):
#     return send_from_directory("/resources/uploads/", path)

if __name__ == '__main__':
    app.run()