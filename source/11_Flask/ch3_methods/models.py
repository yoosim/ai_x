# get 방식으로 회원가입 페이지 만들기
# class Member:
# 	def __init__(self, name, id, pw, addr):
# 		self.name = name
# 		self.id = id
# 		self.pw = pw
# 		self.addr = addr

from pydantic import BaseModel,Field

class Member(BaseModel):
	name: str  = Field(min_length=2, max_length=10, description="이름") # Field 추가
	id: int = Field(gt=0, lt=100, description="아이디")
	# gt=0 : id>0, ge=0: id>=0, lt=100: id<100, le=100: id<=100
	pw: str  #= Field(..., title="비번")
	addr: str = Field(default="서울", description="주소")

if __name__=="__main__":
	member = Member(name="hong", id=1, pw="1234")
	print(member)