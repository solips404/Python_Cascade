import pytesseract
from PIL import Image
import cv2
import glob

imgFiles = glob.glob("realPlate/*.bmp") #取得圖片的路徑
Cascade = cv2.CascadeClassifier("myPlateDetector.xml") #訓練好的檔案
for i in imgFiles:
    img = cv2.imread(i)
    plate = Cascade.detectMultiScale(img)
    for (x,y,w,h) in plate:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        cropImg = thresh[y:y+h, x:x+w]
        contoursl = cv2.findContours(cropImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        contoursArray = contoursl[0]
        let_img = []

        for k in contoursArray:
            (x,y,w,h) = cv2.boundingRect(k)
            let_img.append((x,y,w,h))
        
        let_img = sorted(let_img,key=lambda x:x[0])

        a = 1
        for box in let_img:
            (x,y,w,h) = box
            print((x,y,w,h))
            if w>=5 and h>28 and h<40:
                let_img2 = gray[y:y+h,x:x+w]
                #let_img2 = cv2.resize(let_img2,(18.38))
                filename = i.split('.')[0] +'_'+str(a)+".jpg"
                cv2.imwrite(filename,let_img2)
                a +=1

print("\n")
        #cv2.imshow(i,cropImg)
        #text = pytesseract.image_to_string(cropImg, lang="eng")
        
        
        

cv2.waitKey()
cv2.destroyAllWindows()    
#cropImg = img[y:y+h, x:x+w]
#cv2.imshow(i,cropImg)
#text = pytesseract.image_to_string(cropImg, lang="eng")

#img = cv2.imread("1.png")
#text = pytesseract.image_to_string(img,lang="eng")
#print(text)