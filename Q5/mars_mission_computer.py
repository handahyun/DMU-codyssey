import platform
import psutil
import json
import sys
import os

sys.path.append('..')
# Q4의 MissionComputer 클래스를 BaseMissionComputer 이름으로 상속
from Q4.mars_mission_computer import MissionComputer as BaseMissionComputer


# class 자식 클래스(부모 클래스):
class MissionComputer(BaseMissionComputer):

    # 파일이 없으면 기본값으로 생성
    if not os.path.exists('setting.txt'):
        with open('setting.txt', 'w', encoding='utf-8') as f:
            f.write('운영체계=on\n')
            f.write('운영체계 버전=on\n')
            f.write('CPU 타입=on\n')
            f.write('CPU 코어 수=on\n')
            f.write('메모리 크기=on\n')
            f.write('CPU 실시간 사용량=on\n')
            f.write('메모리 실시간 사용량=on\n')


    # 출력할 항목을 설정한 파일 읽기
    def _load_settings(self):
        settings = {}
        with open('setting.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                # strip() -> \n 제거
                key, value = line.strip().split('=')
                # setting.txt의 내용을 딕셔너리로 변환
                settings[key] = value
        return settings


    def get_mission_computer_info(self):
        settings = self._load_settings()

        all_info = {
            "운영체계": platform.system(),
            "운영체계 버전": platform.version(),
            "CPU 타입": platform.processor(),
            "CPU 코어 수": psutil.cpu_count(),
            # byte 단위로 반환하므로 GB 단위로 변환
            "메모리 크기": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB"
        }
        
        # on인 항목만 필터링
        # ensure_ascii=False -> 한국어 출력 / indent=4 -> 4칸 들여쓰기
        info = {key: value for key, value in all_info.items() if settings.get(key) == 'on'}
        print(json.dumps(info, ensure_ascii=False, indent=4))


    def get_mission_computer_load(self):
        settings = self._load_settings()

        all_load = {
            # 1초 동안 측정한 CPU 사용률 반환
            "CPU 실시간 사용량": f"{psutil.cpu_percent(interval=1)} %",
            "메모리 실시간 사용량": f"{psutil.virtual_memory().percent} %"
        }

        # on인 항목만 필터링
        # ensure_ascii=False -> 한국어 출력 / indent=4 -> 4칸 들여쓰기
        load = {key: value for key, value in all_load.items() if settings.get(key) == 'on'}
        print(json.dumps(load, ensure_ascii=False, indent=4))


# 클래스를 runComputer로 인스턴스화
runComputer = MissionComputer()

runComputer.get_mission_computer_info()
runComputer.get_mission_computer_load()