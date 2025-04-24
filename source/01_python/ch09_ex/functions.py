#functions.py = fn1~()부터  fn9~() 
from customer import Customer
def fn1_insert_customer_info(): 
    name = input('이름을 작성해주세요: ')
    phone = input('전화번호를 작성해주세요: ')
    email = input('이메일을 작성해주세요: ')
    while True:
        try:
            age = int(input('나이를 작성해주세요: '))
            if (age<0) | (age>130):
                raise Exception('나이 범위 이상')
            break            
        except:
            print('올바른 나이를 입력하세요.')           
    try:
        grade = int(input('등급을 작성해주세요: '))
        if grade < 1: 
            grade = 1
        if grade > 5:
            grade =5
    except :
        print('유효하지 않은 등급 입력시 1등급으로 초기화 합니다.')
        grade = 1
    etc = input('기타를 작성해주세요: ')
    return Customer(name, phone, email, age, grade, etc) 

def fn2_print_customers(customer_list):
    'customer_list를 출력(pdf 40page 스타일)'
    print('='*70)
    print('{:^70}'.format('고객정보'))
    print('-'*70)
    print('{:>5}\t{:3}\t{:13}\t{:10}\t{:3}\t{}'.format('GRADE','이름','전화','메일','나이','기타'))    
    print('-'*70)
    for customer in customer_list:
        print(customer)

def fn3_delete_customer(customer_list):
    delname = input('삭제할 고객 이름을 입력하세요: ')
    delidx = [] 
    for idx,customer in enumerate(customer_list):
        if customer.name == delname:
            delidx.append(idx)  
    if delidx:
        for idx in delidx[::-1]: 
            print(customer_list[idx], '지우겠습니까?', end='')
            answer = input('(Y/N)')
            if (answer == 'Y')|(answer == 'y'): 
                print('요청하신 {}({})님 삭제 완료'.format(delname,
                                                 customer_list[idx].phone))
                del customer_list[idx]
    else:
        print('{}님의 데이터가 존재하지 않습니다.'.format(delname))

def fn4_search_customer(customer_list):
    search_name = input('검색할 이름은?')
    search_list = []
    
    for customer in customer_list:
        if customer.name ==search_name:
            search_list.append(customer)
            
    if search_list:
        fn2_print_customers(search_list)
    else:
        print('\n입력하신 {} 고객님의 정보는 조회할 수 없습니다.'.format(search_name))   

def fn5_save_customer_csv(customer_list):
    import csv
    if customer_list:
        customer_dict_list = [] 
        for customer in customer_list:      
            customer_dict_list.append(customer.as_dic())  
        fieldnames = list(customer_dict_list[0].keys())
        filename = input('저장할 csv 파일명을 작성해주세요 :')
        with open('data/{}.csv'.format(filename), 'w', encoding='utf-8', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)       
            dict_writer.writeheader() 
            dict_writer.writerows(customer_dict_list)
            print(f'data/{filename}.csv 내보내기 완료')
    else:
        print('입력된 회원 데이터가 없어 csv 내보내기가 취소됩니다.')     
    
def fn9_save_customer_txt(customer_list):
    customer_txt_list = []
    for customer in customer_list:
        customer_txt_list.append(customer.to_list_style()+ '\n')    
    with open('data/ch09_customers.txt', 'w', encoding='utf-8') as f:
        f.writelines(customer_txt_list)
        print('데이터가 ch09_customers.txt로 저장되었습니다.')