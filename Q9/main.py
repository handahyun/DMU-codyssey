def caesar_cipher_decode(target_text):
    
    print("=" * 60)
    print("카이사르 암호 복호화 결과 (shift 1 ~ 26)")
    print("=" * 60)

    for shift in range(1, 27):
        decoded_chars = []

        for char in target_text:
            if char.isalpha():
                # 대문자와 소문자 기준점(base) 분리
                base = ord('A') if char.isupper() else ord('a')
                # 복호화 공식: (현재 문자 위치 - shift) mod 26
                decoded_char = chr((ord(char) - base - shift) % 26 + base)
                decoded_chars.append(decoded_char)
            else:
                # 알파벳이 아닌 문자(숫자, 공백, 특수문자)는 그대로 유지
                decoded_chars.append(char)

        decoded_text = ''.join(decoded_chars)
        print(f"[shift {shift:2d}] {decoded_text}")

    print("=" * 60)


def main():
    # 1. password.txt 읽기
    file_path = "../Q8/password.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            password_text = f.read().strip()
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return

    print(f"[원문 암호] {password_text}\n")

    # 2. 26가지 복호화 결과 전체 출력
    caesar_cipher_decode(target_text=password_text)

    # 3. 사용자로부터 정답 shift 번호 입력받기
    while True:
        user_input = input("\n해독된 shift 번호를 입력하세요 (1~26): ").strip()

        if not user_input.isdigit():
            print("숫자만 입력해주세요.")
            continue

        shift_answer = int(user_input)

        if not (1 <= shift_answer <= 26):
            print("1에서 26 사이의 숫자를 입력해주세요.")
            continue

        break

    # 4. 선택한 shift 값으로 최종 복호화 수행
    final_result_chars = []
    for char in password_text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            decoded_char = chr((ord(char) - base - shift_answer) % 26 + base)
            final_result_chars.append(decoded_char)
        else:
            final_result_chars.append(char)

    final_result = ''.join(final_result_chars)

    # 5. result.txt로 저장
    output_path = "result.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"사용된 shift 값: {shift_answer}\n")
        f.write(f"원문 암호: {password_text}\n")
        f.write(f"복호화 결과: {final_result}\n")

    print(f"\n[결과] shift {shift_answer} → {final_result}")
    print(f"'{output_path}' 파일로 저장 완료.")


if __name__ == "__main__":
    main()