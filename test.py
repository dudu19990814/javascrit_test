import speech_recognition as sr
import os
import time
import keyboard
from hanspell import spell_checker #github 통해서 다운로드 받아야함
import kss #네이버에서 제공하는 모듈

#녹음 시작 함수 
#녹음이 끝났다고 감지하면, 바로 프로그램이 종료되게 설정

text_file = "myInterview.txt"

#startRecord 함수는 runningTime을 반환하는 동시에 녹음의 기능까지 하는 함수
def startRecord():
    #텍스트 파일 생성   
    
    with open(text_file, 'w', encoding='UTF-8'):
        pass

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("녹음을 시작합니다.")
        start_time = time.time()    
        audio = r.listen(source)
        text = r.recognize_google(audio, language='ko-KR')
        print("인식 결과 : " + text)

        #텍스트 파일에 결과 추가
        with open(text_file, 'a', encoding='UTF-8') as f:
            f.write(text + "\n")
        
        end_time = time.time()
        runningTime = end_time - start_time
        print("녹음이 끝났습니다.")
        print("총 녹음시간 : {:.2f}초".format(runningTime))

        return runningTime

final_runningTime = startRecord() #최종 실행 시간 반환 

#txt 파일 내에 있는 오류들을 고쳐주는 함수
def textCorrect():
    with open(text_file, 'r', encoding='UTF-8') as f:
        lines = f.readlines()

        # 수정된 문장 저장할 리스트 초기화
    new_lines = []

    # 오타 수정과 띄어쓰기 교정
    for line in lines:
        # 한글 문장 오타 수정
        spelled_sent = spell_checker.check(line.strip())
        corrected_sent = spelled_sent.checked
        # 한글 문장 띄어쓰기 교정
        spacing_sent = kss.split_sentences(corrected_sent)
        # 수정된 문장 저장
        new_lines.extend(spacing_sent)

    # 수정된 문장을 파일에 쓰기
    with open(text_file, 'w', encoding='UTF-8') as f:
        for line in new_lines:
            f.write(line.strip() + '\n')

textCorrect()   

#여기에 들어가면 좋은 함수 
#자연어 처리를 활용하여 비슷한 오타를 찾는 함수를 제작해주면 좋을 것으로 예상된다.
#pickKeyword.py 함수를 더 보완해야할지, DB를 다양하게 구성해야할지
#Tensorflow 사용하는 법을 터득해서 구현해야할지 고민해야한다.
#후자가 제일 좋다고 생각된다. 


#여기 부터는 txt 파일을 수정하지 않고 진행한다.
#글자수를 자동으로 세주는 프로그램
#글자수를 통해서 유도하는 것 : 말의 빠르기 

def fileopen(data):
    with open(data,'r',encoding='UTF-8') as f:
        text = f.read()
        split_data = text.split()
 
    return split_data, len(split_data)
 
def count_character(data):
    count = 0  
    for i in data :  
        count += len(i)
 
    return  count
 
data, count = fileopen(text_file)
wordCountResult = count_character(data) + count-1

print("글자 수 : ", wordCountResult)

#말하기 빠르기 측정 함수
#아직 측정이 완벽하게 되지가 않는다. 아쉽다.
def compareSpeakingVel():
    calResult_min = 0.2 * wordCountResult 
    calResult_max = 0.3 * wordCountResult 

    #비교 시작
    #startRecord 함수를 보면, runningTime을 반환하게 만들어둠
    if calResult_min > final_runningTime:
        print("말하는 속도가 너무 빠릅니다.")
    elif calResult_max < final_runningTime:
        print("말하는 속도가 너무 느립니다.")
    else:
        print("적당한 속도로 말했습니댜.")

compareSpeakingVel()