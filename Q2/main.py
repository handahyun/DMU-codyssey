import csv

try:
    #list 객체로 변환
    with open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        data = list(reader)
        #print('리스트 객체로 변환', data)


#람다식과 동일
# def get_flammability(x):
#    return float(x['Flammability'])
# key=get_flammability

    # Flammability 높은 순서대로 정렬
    sorted_data = sorted(data, key=lambda x: float(x['Flammability']), reverse=True)

    # Flammability 0.7 이상 출력
    danger_data = [item for item in sorted_data if float(item['Flammability']) >= 0.7]
    for item in danger_data:
        print(item)

# CSV로 저장
    with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(danger_data)

# 예외 처리
except Exception as error:
    print(f'오류 발생 : {error}')