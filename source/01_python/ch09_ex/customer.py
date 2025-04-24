# customer.py = Customer 클래스, to_customer(),load_customer()
class Customer:
    def __init__(self, name, phone, email, age, grade, etc):
        self.name = name  
        self.phone = phone
        self.email = email
        self.age = age
        self.grade = grade
        self.etc = etc
    def as_dic(self):
        return {
            'name':self.name,
            'phone':self.phone,
            'email':self.email,
            'age':self.age,
            'grade':self.grade,
            'etc':self.etc}
    def to_list_style(self):
        temp = [self.name,
                self.phone,
                self.email,
                str(self.age),
                str(self.grade),
                self.etc]
        return ', '.join(temp)
    
    def __str__(self):
        return '{:>5}\t{:3}\t{:13}\t{:15}\t{:3}\t{}'.format('*'*self.grade,
                                                            self.name,
                                                            self.phone,
                                                            self.email,
                                                            self.age,
                                                            self.etc)
def to_customer(row):
    '''
    "홍길동, 010-9999-9999, a@a.com, 30, 3, 까칠해" (txt파일 내용)을 
    매개변수로 받아 Customer 객체로 return
    '''   

    data = row.split(',')  #,(컴마) 단위로 텍스트를 분리함
    # print(data)
    name = data[0]
    phone = data[1].strip()  #strip은 앞뒤 white space 제거
    email = data[2].strip()
    age = int(data[3].strip())
    grade = int(data[4].strip())
    etc = data[5].strip()

    return Customer(name, phone, email, age, grade, etc)

def load_customers():
    customer_list = []
    try:
        with open('data/ch09_customers.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                customer = to_customer(line)
                customer_list.append(customer)
    except:
        with open('data/ch09_customers.txt', 'w', encoding='utf-8') as f:
            print('초기화 파일을 생성했습니다.')
    return customer_list