import pyzipper
import itertools
import string
import time
import os


# 숫자(0-9)와 소문자 알파벳(a-z)으로 구성된 지정 길이의 암호
def unlock_zip(zip_path: str = "emergency_storage_key.zip", password_length: int = 6) -> str | None:
    if not os.path.exists(zip_path):
        print(f"파일을 찾을 수 없습니다: {zip_path}")
        return None

    charset = string.digits + string.ascii_lowercase
    total_combinations = len(charset) ** password_length

    start_time = time.time()
    print(f"시작 시각 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

    # 50만 회마다 진행 상황 출력
    log_interval = 500_000

    with pyzipper.AESZipFile(zip_path) as zf:

        # 모든 문자 조합을 순서대로 시도
        for attempt, combo in enumerate(itertools.product(charset, repeat=password_length), start=1):
            password = "".join(combo)

            # 진행 상황 출력
            if attempt % log_interval == 0:
                elapsed = time.time() - start_time
                progress = attempt / total_combinations * 100
                print(
                    f"[{time.strftime('%H:%M:%S')}] "
                    f"시도: {attempt:>12,}회 | "
                    f"진행: {progress:5.2f}% | "
                    f"경과: {elapsed:8.1f}s | "
                    
                )

            try:
                zf.extractall(pwd=password.encode())

                # 성공 시 결과 출력 및 password.txt에 저장
                elapsed = time.time() - start_time
                print()
                print(f"암호 해제 성공!")
                print(f"발견된 암호 : {password}")
                print(f"총 시도 횟수 : {attempt:,}회")
                print(f"소요 시간    : {elapsed:.2f}초")

                with open("password.txt", "w", encoding="utf-8") as f:
                    f.write(password)
                print(f"암호가 'password.txt'에 저장되었습니다.")
                return password

            except Exception:
                continue

    # 모든 조합 소진 후 실패 시 결과 출력
    elapsed = time.time() - start_time
    print("암호 해제 실패")
    print(f"총 시도 횟수 : {total_combinations:,}회")
    print(f"소요 시간 : {elapsed:.2f}초")
    return None


if __name__ == "__main__":
    unlock_zip("emergency_storage_key.zip")