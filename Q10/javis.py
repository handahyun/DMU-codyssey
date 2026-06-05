import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import threading
from datetime import datetime
 
 
# --- 설정 ---
# Hz (CD 품질)
SAMPLE_RATE = 44100
# 모노 (스테레오는 2) 
CHANNELS = 1
# 비트 깊이
DTYPE = "int16"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "records")
 

def list_input_devices() -> int:
    
    #사용 가능한 입력 장치를 출력
    print("\n[사용 가능한 마이크 장치]")
    devices = sd.query_devices()
    default_input = sd.default.device[0]
 
    input_devices = []
    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            marker = "★ (기본)" if i == default_input else "  "
            print(f"  [{i}] {marker} {dev['name']}  "
                  f"(입력 채널: {dev['max_input_channels']}, "
                  f"샘플레이트: {int(dev['default_samplerate'])} Hz)")
            input_devices.append(i)
 
    if not input_devices:
        raise RuntimeError("입력 장치를 찾을 수 없습니다. 마이크 연결을 확인하세요.")
 
    print()
    return default_input
 
 
def select_device(default_idx: int) -> int:
    #장치를 선택하거나 기본값 사용
    choice = input(f"사용할 마이크 번호를 입력하세요 (기본값: {default_idx}): ").strip()
    if choice == "":
        return default_idx
    try:
        idx = int(choice)
        # 유효성 검사
        sd.query_devices(idx)
        return idx
    except Exception:
        print(f"  ※ 유효하지 않은 번호입니다. 기본 장치({default_idx})를 사용합니다.")
        return default_idx
 
# 스레드 기반 실시간 녹음 클래스
class Recorder:
    def __init__(self, device: int):
        self.device   = device
        self.frames   = []
        self._stop    = threading.Event()
        self._thread  = None
 
    # 백그라운드 스레드에서 실행되는 녹음 루프
    def _record_loop(self):
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            device=self.device,
        ) as stream:
            print("  녹음 중... (Enter를 누르면 중지됩니다)")
            while not self._stop.is_set():
                data, _ = stream.read(1024)
                self.frames.append(data.copy())
 
    def start(self):
        self._stop.clear()
        self.frames = []
        self._thread = threading.Thread(target=self._record_loop, daemon=True)
        self._thread.start()
 
    def stop(self) -> np.ndarray:
        self._stop.set()
        self._thread.join()
        if not self.frames:
            return np.array([], dtype=DTYPE)
        return np.concatenate(self.frames, axis=0)
 
 
def save_recording(audio: np.ndarray) -> str:
    # 녹음 데이터를 파일로 저장하고 경로 반환
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename  = f"{timestamp}.wav"
    filepath  = os.path.join(OUTPUT_DIR, filename)
    sf.write(filepath, audio, SAMPLE_RATE)
    return filepath
 
 
def format_duration(samples: int) -> str:
    secs  = samples / SAMPLE_RATE
    mins  = int(secs // 60)
    secs  = secs % 60
    return f"{mins}분 {secs:.1f}초" if mins else f"{secs:.1f}초"
 
 
# --- 메인 ---
def main():
    print("=" * 50)
    print("  마이크 녹음기  :  ")
    print("=" * 50)
 
    try:
        default_idx = list_input_devices()
        device_idx  = select_device(default_idx)
        device_info = sd.query_devices(device_idx)
        print(f"\n  선택된 마이크: {device_info['name']}\n")
    except Exception as e:
        print(f"[오류] 장치 초기화 실패: {e}")
        return
 
    recorder = Recorder(device=device_idx)
 
    while True:
        print("-" * 50)
        cmd = input("Enter -> 녹음 시작 / q -> 종료: ").strip().lower()
 
        if cmd == "q":
            print("프로그램을 종료합니다.")
            break
 
        # --- 녹음 시작 ---
        recorder.start()
        # 사용자가 Enter를 누를 때까지 대기
        input()
 
        # --- 녹음 중지 및 저장 ---
        audio = recorder.stop()
 
        if audio.size == 0:
            print("녹음된 데이터가 없습니다.")
            continue
 
        duration = format_duration(len(audio))
        filepath = save_recording(audio)
 
        print(f"\n  저장 완료!")
        print(f"     파일 : {filepath}")
        print(f"     길이 : {duration}")
        print(f"     크기 : {os.path.getsize(filepath) / 1024:.1f} KB\n")
 
 
if __name__ == "__main__":
    main()