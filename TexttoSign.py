from PIL import Image
import string

text={
    'A':'A.png',  'B': 'B.png', 'C': 'C.png', 'D': 'D.png',
    'E': 'E.png', 'F': 'F.png', 'G': 'G.png', 'H': 'H.png',
    'I': 'I.png', 'J': 'J.png', 'K': 'K.png', 'L': 'L.png',
    'M': 'M.png', 'N': 'N.png', 'O': 'O.png', 'P': 'P.png',
    'Q': 'Q.png', 'R': 'R.png', 'S': 'S.png', 'T': 'T.png',
    'U': 'U.png', 'V': 'V.png', 'W': 'W.png', 'X': 'X.png',
    'Y': 'Y.png', 'Z': 'Z.png'
}

def image(input_text):
    input_text=input_text.upper()

    for char in input_text:
        if char not in string.ascii_uppercase:
            continue
        file=text.get(char)

        if file is None:
            continue

        image_path=file
        i=Image.open(image_path)
        i.show()

user=input("문장을 입력하세요: ")

image(user)
