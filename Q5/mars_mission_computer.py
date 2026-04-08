import platform
import psutil
import json
import sys

sys.path.append('..')
# Q4의 MissionComputer 클래스를 BaseMissionComputer 이름으로 상속
from Q4.mars_mission_computer import MissionComputer as BaseMissionComputer

# class 자식 클래스(부모 클래스):
class MissionComputer(BaseMissionComputer):

    def get_mission_computer_info(self):
        info = {
            "운영체계": platform.system(),
            "운영체계 버전": platform.version(),
            "CPU 타입": platform.processor(),
            "CPU 코어 수": psutil.cpu_count(),
            # byte 단위로 반환하므로 GB 단위로 변환
            "메모리 크기": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
        }
        # ensure_ascii=False -> 한국어 출력 / indent=4 -> 4칸 들여쓰기
        print(json.dumps(info, ensure_ascii=False, indent=4))


    def get_mission_computer_load(self):
        load = {
            # 1초 동안 측정한 CPU 사용률 반환
            "CPU 실시간 사용량": f"{psutil.cpu_percent(interval=1)} %",
            "메모리 실시간 사용량": f"{psutil.virtual_memory().percent} %"
        }
        print(json.dumps(load, ensure_ascii=False, indent=4))


# 클래스를 runComputer로 인스턴스화
runComputer = MissionComputer()

runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()