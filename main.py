#%%
# 라이브러리 호출
import numpy as np
import cv2

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이

xml = 'haarcascade/haarcascade_frontalface_default.xml' # github 오픈소스 haarcascades 사용
face_cascade = cv2.CascadeClassifier(xml) # 학습된 데이터 셋을 가져옴

# 얼굴을 인식하여 나이와 성별을 학습 시켜놓은 모델을 불러옴
age_net = cv2.dnn.readNet(
	'deploy_age.prototxt',
	'age_net.caffemodel')

gender_net = cv2.dnn.readNet(
	'deploy_gender.prototxt',
	'gender_net.caffemodel')

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746) # 각 채널에서 빼야하는 RGB값 지정 (정규화를 위한 평균값)

# 나이와 성별 리스트 생성
age_list = ['(0 ~ 10)','(10 ~ 19)', '(20 ~ 32)','(33 ~ 41)','(42 ~ 49)','(50 ~ 69)','(70 ~ 80)','(81 ~ 100)']
gender_list = ['Male', 'Female']

def facefind(cap, face_cascade, age_net, gender_net, MODEL_MEAN_VALUES, age_list, gender_list):
    while(True):
        ret, frame = cap.read() # 설정된 캠으로 영상을 송출하고 비디오 frame을 array 형태로 받아옴, ret은 실행되는지 아닌지 bool형태
        frame = cv2.flip(frame, 1) # 좌우대칭
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 회색으로 스케일링(이미지의 윤곽을 더 명확하게 확인하기 위함)

        faces = face_cascade.detectMultiScale(gray,scaleFactor = 1.05 , minNeighbors = 3, minSize=(30,30)) # 이미지에서 얼굴을 검출(스케일링한 회색이미지, 
                                                                                                        # 이미지를 스케일 사이즈에 맞추기 위한 파라미터,
                                                                                                        # 얼굴을 검출하기 위해 생성된 rectangular 이웃의 개수 지정 :: 너무 높으면 검출한 얼굴을 지워버릴 수 있음
                                                                                                        # 검출하려는 이미지의 최소 사이즈)

        for(x,y,w,h) in faces: # 얼굴

            face = frame[int(y):int(y+h),int(x):int(x+h)].copy() # x,y = rectangular가 시작하는 지점 x,y의 좌표
                                                                # w,h = rectangular의 너비와 길이
                                                                # retangular의 y축 시작지점부터 길이를 더한 값과 x축 시작지점부터 너비를 구한 부분을 얼굴로 지정 
            # 4차원 텐서 형태로 변환(영상에서 검출한 얼굴을 4차원 텐서 형태로 변환하여 추론하기 위한 함수)
            blob = cv2.dnn.blobFromImage(face, scalefactor = 1.1, size = (227, 227), mean=MODEL_MEAN_VALUES, swapRB=False)
                                    # 이미지, 이미지를 스케일 사이즈에 맞추기 위한 파라미터, 신경망이 예상하는 이미지의 크기, 정규화를 하기위해 뺄 평균값 ,R과 B 채널을 서로 바꿀지
            # gender detection
            gender_net.setInput(blob) # net에 blob 데이터를 넣어줌
            gender_preds = gender_net.forward() # 순방향으로 학습
            gender = gender_preds.argmax() # 학습한 것 중에 제일 높은 값 반환
            # Predict age
            age_net.setInput(blob) # net에 blob 데이터를 넣어줌
            age_preds = age_net.forward() # 순방향으로 학습
            age = age_preds.argmax() # 학습한 것 중에 제일 높은 값 반환
            info = gender_list[gender] +' '+ age_list[age]

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2) # 이미지, 사각형의 시작 지점 좌표, 사각형의 크기, (B,G,R), 선 두께
            cv2.putText(frame,info,(x,y-15),0, 0.5, (0, 255, 0), 1) # 이미지, net에서 추출한 정보값, 폰트 입력 좌표값, 폰트 크기, 글씨 두께,(B,G,R)...

        cv2.imshow('result', frame) # 현재 프레임을 윈도우에 출력

        k = cv2.waitKey(30) & 0xff
        if k == 27: # ESC 키를 누르면 종료
            break
            
    cap.release() # 비디오 재생 종료
    cv2.destroyAllWindows() # 모든 윈도우 창 종료
    
    return age
#%%
age = facefind(cap, face_cascade, age_net, gender_net, MODEL_MEAN_VALUES, age_list, gender_list) # 함수에서 반환 받은 age값을 변수로 지정

if age < 5: # age_list의 5번째 인덱스보다 작은(50대 미만)
    import os
    os.system('"C:/Users/82104/Desktop/카메라로 얼굴인식/order_dist/order.exe"') # 기존의 키오스크 창을 이용
else: # 50대 이상
    import os
    os.system('"dist\older.exe"') # 기존의 키오스크보다 노인이 이용하기 편한 키오스크 창 이용

# %%
