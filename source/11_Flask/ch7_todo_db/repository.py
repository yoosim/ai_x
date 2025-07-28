import cx_Oracle
conn = cx_Oracle.connect('scott', 
                        'tiger', 
                        '210.121.189.12:1521/xe') # 객체 생성

from models import TodoRequest
from typing import List # 타입체크

def get_todos(order) -> List[dict]: # 리턴타입 체크
	cursor = conn.cursor()
	if order == 'asc':
		sql = "SELECT * FROM TODO ORDER BY ID"
	else:
		sql = "SELECT * FROM TODO ORDER BY ID DESC"
	cursor.execute(sql)
	result = cursor.fetchall() # 튜플 리스트 
	# keys = [desc[0] for desc in cursor.description] # 컬럼 이름 리스트 (id, content, is_done)
	# todos = [TodoRequest(**row).model_dump() for row in cursor.fetchall()]
	# return [TodoRequest(**row).model_dump() for row in keys]
	todos = []
	for row in result:
		todos.append({'id': row[0], 'content': row[1], 'is_done' : row[2]})
	return todos

def get_next_id() -> int:
	cursor = conn.cursor()
	sql = "SELECT NVL(MAX(ID), 0)+1 FROM TODO"
	cursor.execute(sql)
	result = cursor.fetchone() # 튜플로 받음 (4,)
	cursor.close()
	return result[0]

def get_todo(id:int) -> dict:	
	cursor = conn.cursor()
	sql = "SELECT * FROM TODO WHERE ID = :id"
	cursor.execute(sql, {'id': id})
	result = cursor.fetchone() # 튜플 (1, '바꿀내용' , 0)
	cursor.close()
	return {'id': result[0], 'content': result[1], 'is_done' : result[2]}

def create_todo(todo:TodoRequest) -> int:
	cursor = conn.cursor()
	sql = "INSERT INTO TODO (ID, CONTENTS, IS_DONE) VALUES (:id, :content, :is_done)"
	cursor.execute(sql, 
								todo.model_dump()) # todo 객체를 dict 형태로 변환하여 저장('id':1,..)
	conn.commit()
	cursor.close()
	return cousor.rowcount # 추가 성공시 1, 실패시 0

def update_todo(todo:TodoRequest) -> int:
  cursor = conn.cursor()
  sql = "UPDATE TODO SET CONTENTS=:content, IS_DONE=:is_done WHERE ID=:id"
  cursor.execute(sql, todo.model_dump())
  conn.commit()
  cursor.close()
	if cursor.rowcount:
		return f"{todo.id}번 {todo.content}수정에 성공했습니다."
  return "수정 실패 " # 수정 성공시 성공 메세지, 실패시 실패 메세지 return

def delete_todo(id:int) -> int:
  cursor = conn.cursor()
  sql = "DELETE FROM TODO WHERE ID=:id"
  cursor.execute(sql, {'id': id})
  conn.commit()
  cursor.close()
	if cursor.rowcount:
		return f"{id}번 삭제에 성공했습니다."
  return "삭제 실패 " # 삭제 성공시 성공 메세지, 실패시 실패 메세지 return


if __name__ == '__main__':
	print('/todos :',get_todos('asc'))
	print(' next_id :',get_next_id())
	print('/todo/1 :',get_todo(1))
	todo = TodoRequest(id="90", content='바꿀내용', is_done=True)