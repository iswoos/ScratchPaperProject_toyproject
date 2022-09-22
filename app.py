from pymongo import MongoClient
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import jwt
import datetime
from hashlib import sha256
import hashlib

app = Flask(__name__)

m = sha256()
m.update('Life is too short'.encode('utf-8'))

m.update(', you need python'.encode('utf-8'))

client = MongoClient('mongodb+srv://text:sparta@cluster0.44vwqnl.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.teamProject_grimpan_week1

SECRET_KEY = 'asdf'

# 완료!
@app.route('/')
def home():
    token_receive = request.cookies.get('coin')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('main.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login" , msg="로그인 유효하지않아.."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/main')
def main_page():
    return render_template('/main.html')


@app.route('/post')
def post_page():
    return render_template('/index.html')


@app.route('/api/member/ship', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

    return jsonify({'result': 'success', 'msg': '회원가입 완료!'})


@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 20)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('coin')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# 상세페이지
@app.route("/user/<keyword>")
def show_userpostings(keyword):
    keywords = int(float(keyword))
    user_postings_list = db.pic.find_one({'post_num': keywords})
    return render_template('/index2.html', row=user_postings_list)


@app.route('/save_post', methods=["POST"])
def save_post():
    token_receive = request.cookies.get('coin')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    id_receive = payload['id']
    title_receive = request.form['title']
    content_receive = request.form['text']
    picture_receive = request.form.get('picture')

    user_posting_list = list(db.pic.find({}, {'_id': False}))
    count = len(user_posting_list) + 1
    likecount = 0
    # likeid = []

    doc = {
        'post_num': count,
        'title': title_receive,
        'content': content_receive,
        'likecount': likecount,
        'picture': picture_receive,
        'id': id_receive
        # 'likeid' : (title_receive,content_receive)
    }

    db.pic.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '일기장 저장 완료!'})


@app.route("/show_post", methods=["GET"])
def show_post():
    pic_list = list(db.pic.find({}, {'_id': False}))
    return jsonify({'pic': pic_list})


@app.route("/like_post", methods=["POST"])
def like_post():
    postnums = request.form['postnum_give']
    postnum = int(postnums)

    target_like = db.pic.find_one({'post_num': postnum})

    current_like = target_like['likecount']
    new_like = current_like + 1

    db.pic.update_one({'post_num': postnum}, {'$set': {'likecount': new_like}})
    return jsonify({'result': 'success', 'msg': '좋아요완료! ❤'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)