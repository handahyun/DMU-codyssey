# OpenAI Whisper 사용 (로컬, 무료)
import os
import csv
import whisper

# --- 설정 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS_DIR = os.path.join(BASE_DIR, "..", "Q10", "records")
RECORDS_DIR = os.path.normpath(RECORDS_DIR)

# tiny / base / small / medium / large
WHISPER_MODEL = "base"
# 한국어 고정 (영어면 en, 자동감지는 None)
LANGUAGE = "ko"


def load_audio_files(directory: str) -> list[str]:
    # 디렉토리에서 .wav 파일 목록 반환
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"records 폴더를 찾을 수 없습니다: {directory}")

    files = sorted([
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(".wav")
    ])
    return files

# 초를 HH:MM:SS.xx 형식으로 변환
def seconds_to_timestamp(seconds: float) -> str:
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"

# Whisper로 음성 파일을 변환하고 세그먼트 목록을 반환
def transcribe(model, audio_path: str) -> list[dict]:
    options = {"language": LANGUAGE} if LANGUAGE else {}
    result  = model.transcribe(audio_path, **options)

    rows = []
    for seg in result["segments"]:
        rows.append({
            "start_time": seconds_to_timestamp(seg["start"]),
            "end_time":   seconds_to_timestamp(seg["end"]),
            "text":       seg["text"].strip(),
        })
    return rows

#변환 결과를 CSV로 저장하고 저장 경로를 반환
def save_csv(rows: list[dict], audio_path: str) -> str:
    
    base     = os.path.splitext(audio_path)[0]
    csv_path = base + ".csv"

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["start_time", "end_time", "text"])
        writer.writeheader()
        writer.writerows(rows)

    return csv_path


# --- 메인 ---
def main():
    print("=" * 55)
    print("STT 변환기 (OpenAI Whisper)")
    print("=" * 55)
    print(f"records 경로 : {RECORDS_DIR}")
    print(f"Whisper 모델 : {WHISPER_MODEL}")
    print(f"언어 설정 : {LANGUAGE or '자동 감지'}\n")

    # --- 음성 파일 목록 로드 ---
    try:
        audio_files = load_audio_files(RECORDS_DIR)
    except FileNotFoundError as e:
        print(f"[오류] {e}")
        return

    if not audio_files:
        print("변환할 .wav 파일이 없습니다.")
        return

    print(f"총 {len(audio_files)}개 파일 발견:")
    for i, f in enumerate(audio_files, 1):
        print(f"{i}] {os.path.basename(f)}")
    print()

    # --- Whisper 모델 로드 ---
    print(f"Whisper '{WHISPER_MODEL}' 모델 로딩 중...", end=" ", flush=True)
    model = whisper.load_model(WHISPER_MODEL)
    print("완료!\n")

    # --- 파일별 변환 ---
    for i, audio_path in enumerate(audio_files, 1):
        filename = os.path.basename(audio_path)
        print(f"[{i}/{len(audio_files)}] {filename} 변환 중...")

        try:
            rows = transcribe(model, audio_path)

            if not rows:
                print(f"인식된 텍스트가 없습니다.\n")
                continue

            csv_path = save_csv(rows, audio_path)

            print(f"저장 완료 -> {os.path.basename(csv_path)}")
            print(f"인식된 세그먼트 수: {len(rows)}개")

            # 미리보기 (최대 3줄)
            print(f"--- 미리보기 ---")
            for row in rows[:3]:
                print(f"{row['start_time']} ~ {row['end_time']}  {row['text']}")
            if len(rows) > 3:
                print(f"... 외 {len(rows) - 3}개 세그먼트")
            print()

        except Exception as e:
            print(f"[오류] 변환 실패: {e}\n")

    print("=" * 55)
    print("모든 변환 완료!")
    print("=" * 55)


if __name__ == "__main__":
    main()