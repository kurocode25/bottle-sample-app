from bottle import Bottle, route, run, jinja2_template as template, static_file, request,redirect
from bottle import response
from models import session, Books
from sqlalchemy import text
from utils.util import Utils

app = Bottle()

@app.get('/static/<filePath:path>')
def index(filePath):
    return static_file(filePath, root='./static')

@app.route('/', method='GET')
def index():
    redirect('/list')

@app.route('/add', method=['GET', 'POST'])
def add():
    view = ""
    registId = ""
    form = {}
    kind = "登録"
    if request.method == 'GET':
        # id指定された場合
        if request.query.get('id') is not None:
            book = session.query(Books).filter(Books.id_==request.query.get('id')).first()
            form['name'] = book.name
            form['volume'] = book.volume
            form['author'] = book.author
            form['publisher'] = book.publisher
            form['memo'] = book.memo
            registId = book.id_

            kind = "編集"

        # 表示処理
        return template('add.html'
                , form = form
                , kind=kind
                , registId=registId)
    # POSTされた場合
    elif request.method == 'POST':
        # POST値の取得
        form['name'] = request.forms.decode().get('name')
        form['volume'] = request.forms.decode().get('volume')
        form['author'] = request.forms.decode().get('author')
        form['publisher'] = request.forms.decode().get('publisher')
        form['memo'] = request.forms.decode().get('memo')
        registId = ""
        # idが指定されている場合
        if request.forms.decode().get('id') is not None:
            registId = request.forms.decode().get('id')

        # バリデーション処理
        errorMsg = Utils.validate(data=form)
        # 表示処理
        print(errorMsg)
        if request.forms.get('next') == 'back':
            return template('add.html'
                    , form=form
                    , kind=kind
                    , registId=registId)

        if errorMsg == []:
            headers = ['著書名', '巻数', '著作者', '出版社', 'メモ']
            return template('confirm.html'
                    , form=form
                    , headers=headers
                    , registId=registId)
        else:
            return template('add.html'
                    , error=errorMsg
                    , kind=kind
                    , form=form
                    , registId=registId)

@app.route('/regist', method='POST')
def regist():

    # データ受取
    name = request.forms.decode().get('name');
    volume = request.forms.decode().get('volume');
    author = request.forms.decode().get('author');
    publisher = request.forms.decode().get('publisher');
    memo = request.forms.decode().get('memo');
    registId = request.forms.decode().get('id')

    if request.forms.get('next') == 'back':
        response.status = 307
        response.set_header("Location", '/add')
        return response
    else:
        if registId is not None:
            # 更新処理
            books = session.query(Books).filter(Books.id_==registId).first()
            books.name = name
            books.volume = volume
            books.author = author
            books.publisher = publisher
            books.memo = memo
            session.commit()
            session.close()
        else:
            # データの保存処理
            books = Books(
                    name = name,
                    volume = volume,
                    author = author,
                    publisher = publisher,
                    memo = memo)
            session.add(books) 
            session.commit()
            session.close()
        redirect('/list') # 一覧画面に遷移

# パスワードのリスト表示する
@app.route('/list')
def passList():
    # DBから書籍リストの取得
    bookList = session.query(Books.name, Books.volume, Books.author, Books.publisher, Books.memo, Books.id_)\
            .filter(Books.delFlg == 0).all()
    headers = ['書名', '巻数', '著者', '出版社', 'メモ','操作']
    return template('list.html', bookList=bookList, headers=headers)

@app.route('/delete/<dataId>')
def delete(dataId):
    # 論理削除を実行
    book = session.query(Books).filter(Books.id_==dataId).first()
    book.delFlg = 1
    session.commit()
    session.close()
    redirect('/list')

