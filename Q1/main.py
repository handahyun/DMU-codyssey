# 설치 확인
print('Hello Mars')

# 로그 출력
try:
    with open('mission_computer_main.log', 'r', encoding='utf-8') as file:
        for line in file:
            print(line, end='')
# 예외 처리
except Exception as error:
    print(f'오류 발생 : {error}')