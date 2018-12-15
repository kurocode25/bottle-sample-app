class Utils():

    @classmethod
    def validate(cls, data):
        errMsg = []
        noInput = 'が未入力です。'
        if not data['name']:
            errMsg.append('書名' + noInput)
        if not data['author']:
            errMsg.append('著者' + noInput)
        if not data['publisher']:
            errMsg.append('出版社' + noInput)
        return errMsg
