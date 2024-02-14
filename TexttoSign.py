from flask import Flask, request, jsonify
from PIL import Image
import string

app = Flask(__name__)

# 이미지 파일이름과 알파벳 매칭
alphabet_images = {
    'A': 'A.png',
    'B': 'B.png',
    'C': 'C.png',
    'D': 'D.png',
    'E': 'E.png',
    'F': 'F.png',
    'G': 'G.png',
    'H': 'H.png',
    'I': 'I.png',
    'J': 'J.png',
    'K': 'K.png',
    'L': 'L.png',
    'M': 'M.png',
    'N': 'N.png',
    'O': 'O.png',
    'P': 'P.png',
    'Q': 'Q.png',
    'R': 'R.png',
    'S': 'S.png',
    'T': 'T.png',
    'U': 'U.png',
    'V': 'V.png',
    'W': 'W.png',
    'X': 'X.png',
    'Y': 'Y.png',
    'Z': 'Z.png',
}


def get_image_path(char):
    # 알파벳이 아니면 None 반환
    if char not in string.ascii_uppercase:
        return None

    # 이미지 파일명 가져오기
    image_filename = alphabet_images.get(char)

    # 이미지가 없으면 None 반환
    if image_filename is None:
        return None

    # 이미지 파일 경로 반환
    return image_filename


@app.route('/show_images', methods=['POST'])
def show_images():
    # POST 요청에서 단어 가져오기
    data = request.get_json()
    word = data.get('word', '')

    # 이미지를 담을 리스트 생성
    images = []

    # 단어의 각 알파벳에 대해 이미지 추가
    for char in word.upper():
        image_path = get_image_path(char)
        if image_path:
            images.append(image_path)

    return jsonify(images)


if __name__ == '__main__':
    app.run(debug=True)
