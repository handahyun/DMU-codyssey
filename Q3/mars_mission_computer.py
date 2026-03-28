import random

class DummySensor:

   # 유지보수 편의성
    RANGES = {
        'mars_base_internal_temperature': (18, 30),
        'mars_base_external_temperature': (0, 21),
        'mars_base_internal_humidity': (50, 60),
        'mars_base_external_illuminance': (500, 715),
        'mars_base_internal_co2': (0.02, 0.1),
        'mars_base_internal_oxygen': (4, 7)
    }


    # env_values에 사전 객체({}) 추가
    def __init__(self):
        # private 변수로 캡슐화
        self._env_values = {}


    # env_values에 random값 채우기
    def set_env(self):
        for key, (low, high) in self.RANGES.items():
            self._env_values[key] = round(random.uniform(low, high), 2)


    # env_values return
    def get_env(self):
        # 복사본 반환하여 외부에서 수정 방지
        return self._env_values.copy()


# DummySensor 클래스 인스턴스화
ds = DummySensor()

# set_env 메소드 호출 - 랜덤값 채우기
ds.set_env()

# get_env 메소드 호출 - 채워진 객체들 리턴받기
print(ds.get_env())