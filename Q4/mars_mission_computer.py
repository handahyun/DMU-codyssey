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

        # 강제로 종료(Ctrl+C)하지 않는 한 무한 반복
        while True:

            # Q3.DummySensor의 set_env()를 호출하여 Q3의 _env_values에 랜덤값 채움
            self.ds.set_env()

            # Q3.DummySensor의 get_env()를 호출하여 _env_values에 채워진 값을 받아와 Q4.MissionComputer의 env_values에 저장
            self.env_values = self.ds.get_env()

            # env_values를 JSON 형태로 변환해서 출력
            # 4칸 들여쓰기
            print(json.dumps(self.env_values, indent=4))

            # 5초마다 반복
            time.sleep(5)


# MissionComputer를 RunComputer라는 이름으로 인스턴스화
RunComputer = MissionComputer()

# get_sensor_data 메서드 호출
RunComputer.get_sensor_data() 