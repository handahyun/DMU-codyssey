# 설치 확인
print('Hello Mars')

# 전체 읽기
try:
    with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # 로그 출력
        for line in lines:
            print(line, end='')

        print('---')

        # 역순 출력
        for line in reversed(lines):
            print(line, end='')

    # 마지막 3줄 추출
    problem_lines = lines[-3:]

    # 새로운 파일로 저장(이미 존재 시 덮어쓰기)
    with open('problem_logs.log', 'w', encoding='utf-8') as output:
        for line in problem_lines:
            output.write(line)

# 예외 처리
except Exception as error:
    print(f'오류 발생 : {error}')