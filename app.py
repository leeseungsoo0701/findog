from pymongo import MongoClient
import requests
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename #filename_secure 
from datetime import datetime, timedelta #datetime
from werkzeug.utils import secure_filename #imageupload 라이브러리
from flask_pymongo import PyMongo #pymongo 
import os  #OS
from pymongo import MongoClient
import requests

##########################이미지 업로드 주소
UPLOAD_DIR = "/Users/seungsoo/Documents/GitHub/findog/dog-images" #이미지 저장 경로 각자 로컬로 지정해야함 나중에 aws 내 폴더로 변경
app = Flask(__name__) 
app.config['UPLOAD_DIR'] = UPLOAD_DIR  # 이미지 저장경로


########################DB 연결
#client = MongoClient('mongodb://test:test@localhost', 27017)   서버 연결 시 위 코드로 진행 id:test, pw:test
client = MongoClient('localhost', 27017)  # 로컬 진행 시 위 코드로 진행
db = client.localFindog  # db의 필드 name localFindog

######################### 이미지 업로드 레퍼런스(현재 사용 X)
# app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
#SECRET_KEY = 'SPARTA'

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# db = client.dbsparta_plus_week4


######################## 이승수 이미지 업로드
@app.route('/filesearch', methods=['POST'])
def upload_files():
    f = request.files['file'] 
    fname = secure_filename(f.filename) 
    path = os.path.join(app.config['UPLOAD_DIR'], fname) 
    f.save(path)
    
    db.dogimages.insert_one({'dog-images': path}) 
    return 'File upload complete (%s)' % path


@app.route('/fileupload') 
def upload_main(): 
    return render_template('img_upload.html')
############################



###########################연우님 map
@app.route('/api/map',methods=['GET'])
def print_map():
    return render_template('prac_map2.html')

@app.route('/api/map',methods=['POST'])
def print_location():
    loc = request.form['location']
    print(loc)



############################### 민우님 map(잘 보임 지정 마커 하나는 잘 보임)
@app.route('/map')
def map():
    return render_template('prac_map.html')


# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'dogFind'

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^; 
# 비밀번호 암호화 해쉬 사용
import hashlib



#################################
##  HTML을 주는 부분             ##
#################################

######################################
@app.route('/')
def home():
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html')
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)





@app.route('/post')
def post():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        print(user_info)
        return render_template("post.html", user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    # msg = request.args.get("msg")
    # return render_template('post.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()   #sha256
    doc = {
        "username": username_receive,
        "password": password_hash,
        # "profile_name": username_receive,
        # "profile_pic": "",
        # "profile_pic_real": "profile_pics/profile_placeholder.png",
        # "profile_info": ""
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


############## 로그인 후의 글쓰기가 가능하므로 그 때 적용해보자.
# @app.route('/user/<username>')
# def user(username):
#     # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False


#         user_info = db.users.find_one({"username": username}, {"_id": False})

#         db.user.insert_one({'id': id_receive, 'pw': pw_hash})


#         return render_template('user.html', user_info=user_info, status=status)
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


############## 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {

        'id': username_receive,
        'exp': datetime.utcnow() + timedelta(seconds=1000),  # 로그인 24시간 유지


        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') #.decode('utf-8')   ##### 왜 HS256?

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


############# id 중복 체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    # print(value_receive, type_receive, exists)
    return jsonify({'result': 'success', 'exists': exists})





################# 작성 완료 API
@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        user_info = db.users.find_one({"username": payload["id"]})
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        print(type(date_receive))
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))




########################  게시판 보여주기
# @app.route("/get_posts", methods=['GET'])
# def get_posts():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         my_username = payload["id"]
#         username_receive = request.args.get("username_give")
#         if username_receive=="":
#             posts = list(db.posts.find({}).sort("date", -1).limit(20))
#         else:
#             posts = list(db.posts.find({"username":username_receive}).sort("date", -1).limit(20))


#         for post in posts:
#             post["_id"] = str(post["_id"])

#             post["count_heart"] = db.likes.count_documents({"post_id": post["_id"], "type": "heart"})
#             post["heart_by_me"] = bool(db.likes.find_one({"post_id": post["_id"], "type": "heart", "username": my_username}))

#             post["count_star"] = db.likes.count_documents({"post_id": post["_id"], "type": "star"})
#             post["star_by_me"] = bool(db.likes.find_one({"post_id": post["_id"], "type": "star", "username": my_username}))

#             post["count_like"] = db.likes.count_documents({"post_id": post["_id"], "type": "like"})
#             post["like_by_me"] = bool(db.likes.find_one({"post_id": post["_id"], "type": "like", "username": my_username}))

#         return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("home"))


#############################메인 페이지 강아지 카드 내용 GET, map 마커들 내용 보내기
@app.route('/api/mainpage', methods=['GET'])
def main_page():
    main_page = list(db.dog.find({},{'_id': False})) ##### table명 Card
    return jsonify({'main_page': main_page})


############################ 메인 페이지 강아지 검색 기능
@app.route('/api/mainpage/search', methods=['POST'])
def search_dog():
    search_dog = request.form['search_dog']
    search_list = list(db.dog.find({'dogname': search_dog},{'_id': False}))
    return jsonify({'search_list': search_list})



############################




####################### 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)