import csv
# 데이터를 오래 보관할 수 있는 이진 형태로 절이기(pickling)
import pickle


try:
    # list 객체로 변환
    with open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        data = list(reader)
        #print('리스트 객체로 변환', data)


# 람다식과 동일
# def get_flammability(x):
#     return float(x['Flammability'])
# key=get_flammability

    # Flammability 높은 순서대로 정렬
    sorted_data = sorted(data, key=lambda x: float(x['Flammability']), reverse=True)


    # Flammability 0.7 이상 출력
    danger_data = [item for item in sorted_data if float(item['Flammability']) >= 0.7]
    print('---0.7 이상 출력---')
    for item in danger_data:
        print(item)


    # Flammability 0.7 이상 목록 CSV로 저장
    with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(danger_data)


    # Flammability 높은 순서대로 정렬된 목록을 이진 파일로 저장
    # wb : 이진 파일 쓰기 모드
    with open('Mars_Base_Inventory_List.bin', 'wb') as file:
        pickle.dump(sorted_data, file)


    # Mars_Base_Inventory_List.bin 파일 출력
    # rb : 이진 파일 읽기 모드
    with open('Mars_Base_Inventory_List.bin', 'rb') as file:
        loaded_data = pickle.load(file)
    print('---이진 파일 출력---')
    for item in loaded_data:
        print(item)


# 예외 처리
except Exception as error:
    print(f'오류 발생 : {error}')