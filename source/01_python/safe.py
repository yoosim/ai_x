def safe_index(lst, item) :
    """
    list안에 item 요소가 있으면 
    item 요소의 index를 반환,
    없으면 -1을 반환 
    lst : 나열가능한 데이터
    item : 찾을 데이터 
    """
    if item in lst:        #in연산자 list 가 item에 포함하고 있다면 
        return lst.index(item) 
    else:                   #포함하지 않는다면 -1
        return -1

    # 위의 4줄을 1줄로 바꾼다면 이렇게 쓸 수 있음
    #return lst.index(item) if item in lst else -1 