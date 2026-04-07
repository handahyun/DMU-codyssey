import json
import time
import sys
 # 상위 폴더를 경로에 추가
sys.path.append('..')
from Q3.mars_mission_computer import DummySensor


# DummySensor 클래스를 ds라는 이름으로 인스턴스화
ds = DummySensor()


class MissionComputer:

    def __init__(self):
        # ds를 MissionComputer의 속성으로 연결
        self.ds = ds

        # Q3.DummySensor의 _RANGES의 키 활용하여 env_values 초기화
        # Dictionary Comprehension 문법
        self.env_values = {key: None for key in self.ds._RANGES}


    def get_sensor_data(self):

        # 수집한 값들을 저장할 리스트
        history = []
        # 반복 횟수 카운트
        count = 0

        try:
            # 강제로 종료(Ctrl+C)하지 않는 한 무한 반복
            while True:

                # Q3.DummySensor의 set_env()를 호출하여 Q3의 _env_values에 랜덤값 채움
                self.ds.set_env()

                # Q3.DummySensor의 get_env()를 호출하여 _env_values에 채워진 값을 받아와 Q4.MissionComputer의 env_values에 저장
                self.env_values = self.ds.get_env()

                # env_values를 JSON 형태로 변환해서 출력
                # 4칸 들여쓰기
                print(json.dumps(self.env_values, indent=4))


                # 매 5초마다 값을 history에 저장
                history.append(self.env_values.copy())
                count += 1
            

                # 60회(5분)마다 평균 출력
                if count == 60:
                    # 평균값이 담길 dict
                    average = {}

                    for key in self.env_values:
                        # []에 담긴 60개 값을 키 별로 더한 후 60으로 나눔, 소숫점 2의 자리까지 표현
                        average[key] = round(sum(d[key] for d in history) / 60, 2)
                    print('--- 5분 평균 ---')
                    print(json.dumps(average, indent=4))

                    # history와 count 초기화
                    history = []
                    count = 0

                # 5초마다 반복
                time.sleep(5)


        # ctrl+c 
        except KeyboardInterrupt:
            print('System stopped....')

# MissionComputer를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# get_sensor_data 메서드 호출
RunComputer.get_sensor_data() 