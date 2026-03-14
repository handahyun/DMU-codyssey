# 설치 확인
print('Hello Mars')

# 로그 출력
# 전체 읽기
try:
    with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # 출력
        for line in lines:
            print(line, end='')

        print('---')

        # 역순 출력
        for line in reversed(lines):
            print(line, end='')

# 예외 처리
except Exception as error:
    print(f'오류 발생 : {error}')


    