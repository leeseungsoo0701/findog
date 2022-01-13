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
from bson import ObjectId


##########################이미지 업로드 주소
UPLOAD_FOLDER = "dog-images" #이미지 저장 경로 각자 로컬로 지정해야함 나중에 aws 내 폴더로 변경
app = Flask(__name__) 
# app.config['UPLOAD_DIR'] = UPLOAD_DIR  # 이미지 저장경로
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


########################DB 연결
client = MongoClient('mongodb://test:test@localhost', 27017)   #서버 연결 시 위 코드로 진행 id:test, pw:test
#client = MongoClient('localhost', 27017)  # 로컬 진행 시 위 코드로 진행
db = client.localFindog  # db의 필드 name localFindog

######################### 이미지 업로드 레퍼런스(현재 사용 X)
# app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
# app.config['UPLOAD_FOLDER'] = "./static/profile_pics"
#SECRET_KEY = 'SPARTA'

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
# db = client.dbsparta_plus_week4

# 토큰
DOGTOKEN = 'mytoken'

def authenticated_user(request):
    token = request.cookies.get(DOGTOKEN)
    # 토큰이 존재하지 않는 경우
    if token == None:
        return None
    try:
        # print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        # print(user_info)
        return user_info['username']
    # 유효하지 않은 토큰인 경우
    except Exception:
        return None;



######################댓글 리스트 이미지 박민우
@app.route('/modal_image', methods=['POST'])
def modal_image():
    dog_id = request.form['dog_id']
    print('dog_id------------' + dog_id)
    dog_list = db.lost.find_one({'_id': ObjectId(dog_id)})
    dog_image = dog_list['dog-images']
    print(dog_image)
    return jsonify({'lostDogImage': dog_image})



# 연우 refact : 전체 삭제
######################## 이승수 이미지 업로드
# @app.route('/filesearch', methods=['POST'])
# def upload_files():
#
#         auth_user = authenticated_user(request)
#         f = request.files['file']
#         title = request.form['title']
#         dogName = request.form['dogName']
#         lostAddress = request.form['lostAddress']
#         contentArea = request.form['contentArea']
#         contentArea2 = request.form['contentArea2']
#         callArea = request.form['callArea']
#         locationx = request.form['locationx']
#         locationy = request.form['locationy']
#         print('location—————'+locationx)
#         print('location—————'+locationy)
#
#
#         fname = secure_filename(f.filename)
#         path = os.path.join(os.path.join(app.root_path, 'static/missing'))
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         path = os.path.join(path, fname)
#         split_path = path.split('/')
#         print(split_path)
#         img_length = len(split_path)
#         real_path = str(split_path[img_length-3] +'/'+ split_path[img_length-2] +'/'+ split_path[img_length-1])  # 경로는 동일하다.
#         f.save(path)
#
#
#         doc = {
#             "dog-images": real_path,
#             "callArea": callArea,
#             'title' : title,
#             'dogName': dogName,
#             'lostAddress': lostAddress,
#             'contentArea': contentArea,
#             'contentArea2': contentArea2,
#             'locationx':locationx,
#             'locationy':locationy
#         }
#         db.post.insert_one(doc)
#         return render_template('index.html',username=auth_user)


############### 
######################## 이승수 modal POST
@app.route('/uploadmodal', methods=['POST'])
def upload_modal():
        page_id = request.form['page_id']

        findArea = request.form['findArea']
        dogFace = request.form['dogFace']
        dog_img = request.files['dog_img']
        nickname = request.form['nickname']
        

        fname = secure_filename(dog_img.filename)
        path = os.path.join(os.path.join(app.root_path, 'static/lost'))
        if not os.path.isdir(path):
            os.mkdir(path)
        path = os.path.join(path, fname)
        split_path = path.split('/')
        print(split_path)
        img_length = len(split_path)
        real_path = str(split_path[img_length-3] +'/'+ split_path[img_length-2] +'/'+ split_path[img_length-1])  # 경로는 동일하다.
        print(real_path)
        dog_img.save(path)


        doc = {
            "nickname": nickname,
            "page_id": page_id,
            'findArea': findArea,
            'dogFace': dogFace,
            'dog-images': real_path
        }
        db.lost.insert_one(doc)
        list_dog = list(db.lost.find({'page_id':page_id}))
        # list_dog_list = objectIdDecoder(list_dog)
        # print(list_dog_list)
        dog = db.post.find_one({'_id':ObjectId(page_id)})
        redirect_url = '/watchdog/'+str(page_id) # 연우 refact : redirect url 추가
        return redirect(redirect_url) # 연우 refact : redirect 로 변경
        # return render_template('watchdog.html', dog=dog, list_dog=list_dog) # 연우 refact : 삭제




######################
@app.route('/getlocation', methods = ['GET'])
def get_location():
    main_location = list(db.post.find({},{'_id': False}))
    return jsonify({'main_location': main_location})



# ######################## 이승수 이미지 업로드
# @app.route('/filesearch', methods=['POST'])
# def upload_files():
#     f = request.files['file'] 
#     fname = secure_filename(f.filename) 
#     path = os.path.join(app.config['UPLOAD_FOLDER'], fname) 
#     f.save(path)
#     print(path)
#     return 'File upload complete (%s)' % path


# @app.route('/upload') 
# def upload_main(): 
#     return render_template('img_upload.html')
# ############################



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
    username= authenticated_user(request)
    return render_template('index.html',username=username)
    # 연우 refact : 남아있던 주석들 모두 삭제

# 연우 refact : 함수 추가 ( 위에 함수를 삭제 했으니 이 함수를 그대로 살려주세요 )
# redirect into '/'
@app.route('/filesearch',methods=['POST'])
def upload_file():
    auth_user = authenticated_user(request)
    f = request.files['file']
    title = request.form['title']
    dogName = request.form['dogName']
    lostAddress = request.form['lostAddress']
    contentArea = request.form['contentArea']
    contentArea2 = request.form['contentArea2']
    callArea = request.form['callArea']
    locationx = request.form['locationx']
    locationy = request.form['locationy']
    print('location—————' + locationx)
    print('location—————' + locationy)

    fname = secure_filename(f.filename)
    path = os.path.join(os.path.join(app.root_path, 'static/missing'))
    if not os.path.isdir(path):
        os.mkdir(path)
    path = os.path.join(path, fname)
    split_path = path.split('/')
    print(split_path)
    img_length = len(split_path)
    real_path = str(
        split_path[img_length - 3] + '/' + split_path[img_length - 2] + '/' + split_path[img_length - 1])  # 경로는 동일하다.
    f.save(path)

    doc = {
        "dog-images": real_path,
        "callArea": callArea,
        'title': title,
        'dogName': dogName,
        'lostAddress': lostAddress,
        'contentArea': contentArea,
        'contentArea2': contentArea2,
        'locationx': locationx,
        'locationy': locationy
    }
    db.post.insert_one(doc)
    return redirect('/')







@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)





@app.route('/post')
def post():
    auth_member = authenticated_user(request)
    if auth_member is None:
        return redirect(url_for("login",msg="유효한 세션이 없습니다."))
    else :
        return render_template("post.html",username=auth_member)
    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.users.find_one({"username": payload["id"]})
    #     print(user_info)
    #     return render_template("post.html", user_info=user_info)
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    # msg = request.args.get("msg")
    # return render_template('post.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/watchdog/<path:subpath>')
def watchdog(subpath):
    auth_member = authenticated_user(request)
    dog = db.post.find_one({'_id': ObjectId(subpath)})
    print('dog             ' + str(dog))
    list_dog = list(db.lost.find({'page_id': subpath}))
    return render_template("watchdog.html", dog=dog, list_dog=list_dog, username=auth_member)



###############################
# @app.route('/card_id', methods=['POST'])
# def card_id():
#     dog_id = request.form['dog_id']
#     print(dog_id)
#     select_card = db.post.find({'_id': ObjectId(dog_id)})
#     articles = objectIdDecoder(select_card)
#     return render_template('watchdog.html', articles=articles)







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
        'exp': datetime.utcnow() + timedelta(seconds=60*60*1),  # 로그인 24시간 유지


        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')   ##### 왜 HS256?

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
    auth_user = authenticated_user(request)
    if auth_user is None:
        return redirect(url_for("home"),username=auth_user)
    else:
        user_info = auth_user
        comment_receive = request.form["comment_give"]
        date_receive = request.form["date_give"]
        doc = {
            "username": user_info["username"],
            "profile_name": user_info["profile_name"],
            "profile_pic_real": user_info["profile_pic_real"],
            "comment": comment_receive,
            "date": date_receive
        }
        db.posts.insert_one(doc)
        return jsonify({"result": "success", 'msg': '포스팅 성공'})

    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     # 포스팅하기
    #     user_info = db.users.find_one({"username": payload["id"]})
    #     comment_receive = request.form["comment_give"]
    #     date_receive = request.form["date_give"]
    #     print(type(date_receive))
    #     doc = {
    #         "username": user_info["username"],
    #         "profile_name": user_info["profile_name"],
    #         "profile_pic_real": user_info["profile_pic_real"],
    #         "comment": comment_receive,
    #         "date": date_receive
    #     }
    #     db.posts.insert_one(doc)
    #     return jsonify({"result": "success", 'msg': '포스팅 성공'})
    # except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
    #     return redirect(url_for("home"))




#############################메인 페이지 강아지 카드 내용 GET, map 마커들 내용 보내기
@app.route('/api/mainpage', methods=['GET'])
def main_card():
    main_card = objectIdDecoder(list(db.post.find().sort('_id', -1)))   ##### table명 Card 최신순

    return jsonify({'main_card': main_card})


############################ 메인 페이지 강아지 검색 기능
@app.route('/api/mainpage/search', methods=['POST'])
def search_dog():
    search_dog = request.form['search_dog']
    search_list = objectIdDecoder(list(db.post.find({'dogName': search_dog}).sort("_id",-1))) ###Card 최신순

    return jsonify({'search_list': search_list})


########################### 카드에 해당하는 ID 변환
def objectIdDecoder(list):
    results = []
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results


############################### 변환된 ID를 부르는 곳
@app.route('/memo', methods=['GET'])
def delete_get():
    articles = objectIdDecoder(list(db.post.find({})))
    #all_alti = str(articles)
    print(articles)
    return jsonify({'all_articles': articles})





####################### 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
