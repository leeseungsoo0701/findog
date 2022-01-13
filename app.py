from pymongo import MongoClient   #pymongo 연결을 위한 패키지
import requests
import jwt   # JWT 사용을 위한 패키지
import datetime #토큰 유지 기간을 위한 패키지
import hashlib 
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename #filename_secure 
from datetime import datetime, timedelta #datetime
from werkzeug.utils import secure_filename #imageupload 라이브러리
from flask_pymongo import PyMongo #pymongo 
import os  #OS
from bson import ObjectId

app = Flask(__name__) 



######################## mongoDB 연결
client = MongoClient('mongodb://test:test@localhost', 27017)   #서버 연결 시 위 코드로 진행 id:test, pw:test 
#client = MongoClient('localhost', 27017)  # 로컬 진행 시 위 코드로 진행
db = client.localFindog  # db의 필드 name localFindog

# 토큰
DOGTOKEN = 'mytoken'

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'dogFind'

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^; 
# 비밀번호 암호화 해쉬 사용
import hashlib

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
    }
    db.users.insert_one(doc)    #userDB에 저장
    return jsonify({'result': 'success'})


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
        'exp': datetime.utcnow() + timedelta(seconds=60*60*1),  # 로그인 1시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')   ##### 왜 HS256??? 로컬일때와 서버일때의 차이점
        return jsonify({'result': 'success', 'token': token})

    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


############# id 중복 체크
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive})) #bool 판단으로 id 중복 체크
    return jsonify({'result': 'success', 'exists': exists})


########################## 사용자 인증 부분(항상 불러온다.)
# 세션이 유효한 경우(try) return username 을 주고 다른 경우 return None을 준다.
def authenticated_user(request):
    token = request.cookies.get(DOGTOKEN)
    # 토큰이 존재하지 않는 경우
    if token == None:
        return None        
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return user_info['username']
    # 유효하지 않은 토큰인 경우 
    except Exception:
        return None;


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




###################### 메인 페이지 map에서 위치 정보 넘기기
@app.route('/getlocation', methods = ['GET'])
def get_location():
    main_location = list(db.post.find({},{'_id': False}))
    return jsonify({'main_location': main_location})












######################댓글 리스트 클릭 시 이미지 modal 출력
@app.route('/modal_image', methods=['POST'])
def modal_image():
    dog_id = request.form['dog_id']
    dog_list = db.lost.find_one({'_id': ObjectId(dog_id)})  #str 형태의 dog_id를 ObjectID 형태로 만들어서 비교하고 dog_list에 저장.
    dog_image = dog_list['dog-images']
    return jsonify({'lostDogImage': dog_image})


######################## 댓글(modal)창의 입력 텍스트 및 사진 lost DB 저장
@app.route('/uploadmodal', methods=['POST'])
def upload_modal():
        page_id = request.form['page_id']  #카드 해당 ID
        find_area = request.form['findArea']
        dog_face = request.form['dogFace'] 
        dog_img = request.files['dog_img']
        nickname = request.form['nickname']
        

        fname = secure_filename(dog_img.filename)
        path = os.path.join(os.path.join(app.root_path, 'static/lost'))    #static/lost/~~.png 
        
        #디렉토리가 없다면 디렉토리를 만들어준다
        if not os.path.isdir(path):   
            os.mkdir(path)
        path = os.path.join(path, fname)

        #path가 절대경로이므로 상대경로로 만들어 DB에 주소를 넣어주기 위한 작업.
        split_path = path.split('/')
        img_length = len(split_path) #DB 칼럼의 길이
        real_path = str(split_path[img_length-3] +'/'+ split_path[img_length-2] +'/'+ split_path[img_length-1])  # 경로는 동일하다. static/lost/~~.png (윈도우 제외)
        dog_img.save(path)  # 위 경로에 이미지를 저장한다.

        #lostDB에 저장하기 위한 칼럼 및 데이터들
        doc = {
            "nickname": nickname,
            "page_id": page_id,
            'findArea': find_area,
            'dogFace': dog_face,
            'dog-images': real_path
        }
        db.lost.insert_one(doc) #DB에 저장한다.(한줄)

        list_dog = list(db.lost.find({'page_id':page_id}))   #page_id-> 카드의 고유 id를 비교하여 lost에 들어있는 모든 list를 가져온다. 글 하단의 댓글리스트에 뿌려준다.

        dog = db.post.find_one({'_id':ObjectId(page_id)}) # page_id를 objectid로 바꿔서 post의 id와 비교하여 찾는다.

        redirect_url = '/watchdog/'+str(page_id) # redirect url을 설정

        return redirect(redirect_url) # redirect 로 이동한다.











#################################
##  HTML을 주는 부분             ##
#################################

###################################### 메인 페이지
@app.route('/')
def home():
    username= authenticated_user(request)
    return render_template('index.html',username=username)

###################################### 로그인으로 이동
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

############################### 회원 가입 이동 
@app.route('/register')
def register():
    return render_template('register.html')



########################################## 작성 완료 API POST , redirect '/'
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















@app.route('/watchdog/<path:subpath>')
def watchdog(subpath):
    auth_member = authenticated_user(request)
    dog = db.post.find_one({'_id': ObjectId(subpath)})
    list_dog = list(db.lost.find({'page_id': subpath}))
    return render_template("watchdog.html", dog=dog, list_dog=list_dog, username=auth_member)



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








####################### 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
