import random
import logging
import os


class DummySensor:

   # 유지보수 편의성
    _RANGES = {
        'mars_base_internal_temperature' : (18, 30),
        'mars_base_external_temperature' : (0, 21),
        'mars_base_internal_humidity' : (50, 60),
        'mars_base_external_illuminance': (500, 715),
        'mars_base_internal_co2' : (0.02, 0.1),
        'mars_base_internal_oxygen' : (4, 7)
    }

    _LOG_FILE = 'mars_base.log'
    _LOG_HEADER = '날짜와 시간,로그 레벨,화성 기지 내부 온도(°C),화성 기지 외부 온도(°C),화성 기지 내부 습도(%),화성 기지 외부 광량(W/m²),화성 기지 내부 이산화탄소 농도(%),화성 기지 내부 산소 농도(%)'


    #인스턴스 초기화
    def __init__(self):
        # env_values에 사전 객체({}) 추가
        # private 변수로 캡슐화
        self._env_values = {}
        # 로깅 초기 설정
        self._setup_logging() 


    def _setup_logging(self):
        # 로그 파일, 로그 레벨, 출력 형식 설정
        logging.basicConfig(
            filename=self._LOG_FILE,
            level=logging.INFO,
            format='%(asctime)s,%(levelname)s,%(message)s',
            # 밀리초 제거
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 로그 파일이 없거나 비어있을 경우에만 헤더 기록
        if not os.path.exists(self._LOG_FILE) or os.path.getsize(self._LOG_FILE) == 0:
        # 헤더는 logging을 거치지 않고 파일에 직접 기록
            with open(self._LOG_FILE, 'w', encoding='utf-8') as f:
                f.write(self._LOG_HEADER + '\n')


    # env_values에 random값 채우기
    def set_env(self):
        for key, (low, high) in self._RANGES.items():
            self._env_values[key] = round(random.uniform(low, high), 2)


    # 로그 파일 기록
    def _log_env(self):
        logging.info(
            f'{self._env_values['mars_base_internal_temperature']},'
            f'{self._env_values['mars_base_external_temperature']},'
            f'{self._env_values['mars_base_internal_humidity']},'
            f'{self._env_values['mars_base_external_illuminance']},'
            f'{self._env_values['mars_base_internal_co2']},'
            f'{self._env_values['mars_base_internal_oxygen']}'
        )


    def get_env(self):
        # 로그 기록
        self._log_env()
        # _env_values 복사본 반환하여 외부에서 수정 방지
        return self._env_values.copy()


# DummySensor 클래스 인스턴스화
ds = DummySensor()

# set_env 메소드 호출 - 랜덤값 채우기
ds.set_env()

# get_env 메소드 호출 - 채워진 객체들 리턴받기
print(ds.get_env())