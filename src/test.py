import animeface
import PIL.Image
import cv2
import numpy as np
import sys

im = PIL.Image.open(sys.argv[1])
resize_rate = float(sys.argv[2])

faces = animeface.detect(im)
# print(faces)
# fp = faces[0].face.pos
# print(fp.x, fp.y, fp.width, fp.height)

# im.show()

im_cv2_retangle = np.asarray(im)
im_cv2_retangle = cv2.cvtColor(im_cv2_retangle, cv2.COLOR_BGR2RGB)

for face in faces:
    face_start = (face.face.pos.x, face.face.pos.y)
    face_end = (face.face.pos.x + face.face.pos.width, face.face.pos.y + face.face.pos.height)
    im_cv2_retangle = cv2.rectangle(im_cv2_retangle, face_start,face_end,(0, 50, 255), 3)
    for eye in (face.left_eye, face.right_eye):
        eye_start = (eye.pos.x, eye.pos.y)
        eye_end = (eye.pos.x + eye.pos.width, eye.pos.y + eye.pos.height)
        im_cv2_retangle = cv2.rectangle(im_cv2_retangle, eye_start,eye_end,(0, 50, 255), 3)

resize_size = tuple(map(lambda x:int(x*resize_rate), reversed(im_cv2_retangle.shape[:2])))
im_cv2_retangle = cv2.resize(im_cv2_retangle, resize_size)
cv2.imshow('test',im_cv2_retangle)
cv2.waitKey(0)
cv2.destroyAllWindows()
