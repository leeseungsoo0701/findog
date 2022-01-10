from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

#client = MongoClient('mongodb://test:test@localhost', 27017)   서버 연결 시 위 코드로 진행 id:test, pw:test
client = MongoClient('localhost', 27017)  # 로컬 진행 시 위 코드로 진행
db = client.dogFind  # db의 필드 name dogFind


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')

# @app.route('/memo', methods=['GET'])
# def listing():
#     # sample_receive = request.args.get('sample_give')
#     articles = list(db.spartatest.find({},{'_id': False}))

#     return jsonify({'all_articles': articles})

# ## API 역할을 하는 부분
# @app.route('/memo', methods=['POST'])
# def saving():
#     url_receive = request.form['url_give']
#     comment_receive = request.form['comment_give']

#     # url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=171539'

#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#     data = requests.get(url_receive, headers=headers)

#     soup = BeautifulSoup(data.text, 'html.parser')


#     image = soup.select_one('meta[property="og:image"]')['content']
#     title = soup.select_one('meta[property="og:title"]')['content']
#     desc = soup.select_one('meta[property="og:description"]')['content']

#     doc = {
#         'image' : image,
#         'title' : title,
#         'desc' : desc,
#         'url' : url_receive,
#         'comment' : comment_receive
#     }

#     db.spartatest.insert_one(doc)
#     return jsonify({'msg': '저장이 완료되었습니다.'})

# @app.route('/memo/delete', methods=['POST'])
# def delete_star():
#     url_receive = request.form['url_give']
#     db.spartatest.delete_one({'url': url_receive})
#     return jsonify({'msg': '삭제 완료되었습니다!'})


#port 5000으로 웹 보여주기
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)