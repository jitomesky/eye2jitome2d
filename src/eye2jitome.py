import animeface
import PIL.Image
import cv2
import numpy as np
import sys

im_pil = PIL.Image.open(sys.argv[1])
faces = animeface.detect(im_pil)

jitome = PIL.Image.open("jitome.png")

# PILに変換
im_pil = im_pil.convert('RGBA')

# 透過キャンパスを生成
c = PIL.Image.new('RGBA', im_pil.size, (255, 255,255, 0))

# 目をじとめに置き換え
for face in faces:
    y_pos = (face.left_eye.pos.y + face.right_eye.pos.y) / 2
    width = (face.left_eye.pos.width + face.right_eye.pos.width) / 2
    height =  (face.left_eye.pos.height + face.right_eye.pos.height) / 2
    size_arrange = (1.5, 1.3)
    eye_wh = (int(width * size_arrange[0]), int(height * size_arrange[1]))
    # # じとめをリサイズ
    jitome_resize = jitome.resize(eye_wh)
    for eye in (face.left_eye, face.right_eye):
        pos_arrange = 0.99
        eye_start = (int(eye.pos.x * pos_arrange ), int(y_pos * pos_arrange))
        # 透過キャンパスにじとめを貼り付け
        c.paste(jitome_resize, eye_start)
    
# 合成
im_pil = PIL.Image.alpha_composite(im_pil, c)

# RGBA -> RGB
im_pil = im_pil.convert('RGB')

# OpenCVオブジェクトに変換
im = np.asarray(im_pil)
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

resize_size = tuple(map(lambda x:int(x*0.5), reversed(im.shape[:2])))
im = cv2.resize(im, resize_size)
# 画像表示
cv2.imshow("Show Image",im)

# キー入力待機
cv2.waitKey(0)

cv2.destroyAllWindows()
