-- DCL (계정생성, 권한부여, 권한박탈, 계정삭제, 트랜젝션 명령어)
-- DDL (테이블생성, 테이블삭제, 제약조건, ★oracle과 다르게 시퀀스 없음★, 타입이 다름 )
-- DML (INSERT,UPDATE,DELETE, SELECT)
	-- SELECT의 다른점 OUTER JOIN, AND=&& 연산자, OR=|| 연산자(오라클에서는 연결이였음),CONCAT함수를 이용하여 연결연산자 대치
-- DDL과 DML은 데이터베이스에 접근해야 사용이 가능 (테이블을 만들기 때문에) / DCL은 테이블을 만들게 아니라서 밖에서 해도 됨

-- 
show databases; -- database들 리스트
use world;
use sakila; -- database들에 왔다갔다 할 수 있음
show tables; -- database 내 테이블들
select * from city;
desc city;  -- 테이블의 구조 


-- -------------- --
--    ★ DCL ★
-- -------------- --
-- 계정생성 
create user user01 identified by 'password'; -- 계정생성 (id = user01, password = password)

-- 권한부여
grant all privileges on *.* to user01;  -- *.* 모든데이터베이스와 모든 테이블 데이터베이스명.테이블명  / oracle에서 dba권한부여랑 동일함

-- 권한박탈
revoke all privileges on *.* from user01;  -- 모든데이터베이스와 모든 테이블의 권한을 박탈

-- 계정삭제
drop user user01;  -- user01 계정 삭제 

-- -------------- --
--    ★ DDL ★
-- -------------- --
/*My SQL 타입 : numeric(n,d) 숫자, varchar(n) 문자, date, 
 정수 타입 : tinyint(1byte), smallint(2byte), mediumint(3byte),
			int/integer(4byte) , bigint(8byte)
실수 타입 : float (n,d;4byte) , double(n,d;8byte)
문자 타입 : char(n), text, mediumtext(16MB), longtext(4GB)
날짜 타입 : date, datetime, time, year, timestamp
*/
-- DDL 이나 DML 명령어는 데이터베이스 내에서 실행해야 함
-- 데이터베이스 조회 및 생성
show databases;        -- 데이터베이스 list (dbdb가 생성됨)
create database dbdb;  -- 데이터베이스 생성하는 명령어
use dbdb;              -- 위에서 생성한 dbdb로 진입 / 특정데이터베이스로 들어감
select database();     -- 현재 들어와 있는 데이터베이스

-- 테이블 만들기 
drop table emp;            -- 에러 발생
drop table if exists emp;  -- emp 테이블이 존재할 경우 삭제  
create table emp(
	empno    numeric(4) primary key,
    ename    varchar(6) not null,
    nickname varchar(6) unique,
    sal    numeric(7,2) check(sal>0),
    comm   numeric(7,2) default 0
)default charset=utf8;

-- 데이터 추가
insert into emp (empno,ename,nickname,sal) 
	values (1,'홍길동동동동','길다길다길어',-1);
insert into emp (empno, ename, nickname, sal) 
	values (1,'홍','길다길다길어',1000);
select * from emp;

-- MySQL에서는 시퀀스가 없음 
-- MySQL에서 10, 20, 30, ...를 만들기 위한 인위적인 primary key
/* 
set @@auto_increment_increment=10;
set @@auto_increment_offset=10;

-- 테이블 만들기 
drop table if exists major; 
create table major(
	mcode int primary key auto_increment, -- auto_increment에선 반드시 int로 해야 함(numeric이 아닌 int)
    mname varchar(30),
    moffice varchar(30)
)default charset=utf8;
insert into major (mname, moffice) values('컴공','m101호');
insert into major (mname, moffice) values('화학','m201호');
select * from major; */

use dbdb;
select database();
-- 테이블 만들기 (major)
drop table if exists major; 
create table major(
	mcode int primary key auto_increment, -- auto_increment에선 반드시 int로 해야 함(numeric이 아닌 int)
    mname varchar(30),
    moffice varchar(30)
)default charset=utf8;

insert into major (mname,moffice) values ('컴공','a102호');
insert into major (mname,moffice) values ('ai','a104호');
insert into major (mname,moffice) values ('정보통신','a101호');
select * from major;

-- 테이블 만들기 (student)
drop table if exists student; 
create table student(
	sno   numeric(4) primary key,
    sname varchar(30) not null,
    mcode int references major(mcode) 
)default charset=utf8;

insert into student values (101, '홍길동', 1);
insert into student values (102, '신길동', 2);
insert into student values (103, '임길동', 3);
insert into student values (104, '차길동', 4);
select * from student; -- references 적용이 안됨 

-- join
select *
	from student s, major m 
    where s.mcode = m.mcode;  -- equi,non-equi, self join은 사용법 동일 
    
-- outer join
select *
	from student s left outer join major m 
    on s.mcode = m.mcode; 
    
-- 테이블 다시 만들기    
drop table if exists student; 
create table student(
	sno   numeric(4),
    sname varchar(30) not null,
    mcode int,
    primary key (sno),
    foreign key(mcode) references major(mcode)
)default charset=utf8;

select * from major;
insert into student values (101, '홍길동', 1);
insert into student values (102, '신길동', 2);
insert into student values (103, '유길동', 9); -- 에러 : fk
select * from student;
select sno, sname, m.mcode, mname, moffice 
	from major m, student s
    where m.mcode=s.mcode;  -- 3번 학과는 출력되지 않음 (student에 없어서)
    
select sno, sname, m.mcode, mname, moffice 
	from student s right outer join major m      -- student 는 1,2 / major은 1,2,3이 있음 
    on m.mcode=s.mcode;  -- 3번 학과까지 출력(outer join) 
    
-- -------------- --
--    ★ DML ★
-- -------------- --

-- division 테이블 생성
drop table if exists division;
create table division(
	DNO int not null primary key,
    dname varchar(20),
    phone varchar(20),
    position varchar(20))default charset=utf8;
show tables;  -- 현 데이터베이스 내의 테이블 list 

-- personal 테이블 생성
drop table if exists personal;
create table personal (
	pno int primary key,
	pname varchar(10) not null,
    job varchar(15) not null,
    manager int,
    startdate date,
    pay int, 
    bonus int,
    dno int ,
    foreign key(dno) references division(dno))default charset=utf8;
show tables;
desc division;
insert into division values (10, 'finance','02-777-7777','종로');
insert into division values (20, 'research','041-888-7777','대전');
insert into division values (30, 'sales','02-999-7777','인천');
insert into division values (40, 'marketing','02-555-7777','강남');
select * from division

insert into personal values (1111,'smith','manager', 1001, '1990-12-17', 1000, null, 10);
insert into personal values (1112,'ally','salesman',1116,'1991-02-20',1600,500,30);
insert into personal values (1113,'word','salesman',1116,'1992-02-24',1450,300,30);
insert into personal values (1114,'james','manager',1001,'1990-04-12',3975,null,20);
insert into personal values (1001,'bill','president',null,'1989-01-10',7000,null,10);
insert into personal values (1116,'johnson','manager',1001,'1991-05-01',3550,null,30);
insert into personal values (1118,'martin','analyst',1111,'1991-09-09',3450,null,10);
insert into personal values (1121,'kim','clerk',1114,'1990-12-08',4000,null,20);
insert into personal values (1123,'lee','salesman',1116,'1991-09-23',1200,0,30);
insert into personal values (1226,'park','analyst',1111,'1990-01-03',2500,null,10);

select * from division;
select * from personal;


-- 1. 사번, 이름, 급여를 출력
select pno, pname,pay 
	from personal;

-- 2. 급여가 2000~5000 사이 모든 직원의 모든 필드
select * 
	from personal
    where pay between 2000 and 5000;
-- 3. 부서번호가 10또는 20인 사원의 사번, 이름, 부서번호
select pno, pname,dno
	from personal
    where dno in (10,20);

-- 4. 보너스가 null인 사원의 사번, 이름, 급여 급여 큰 순정렬
select pno,pname,pay
	from personal
    where bonus is null
    order by pay desc;
    
-- 5. 사번, 이름, 부서번호, 급여. 부서코드 순 정렬 같으면 PAY 큰순
select pno, pname, dno, pay
	from personal
    order by dno, pay desc;
-- 6. 사번, 이름, 부서명
select p.pno, p.pname, d.dname
	from personal p, division d
    where p.dno=d.dno;
    
select * from division;
select * from personal; 

-- 7. 사번, 이름, 상사이름
select a.pno 사번 , a.pname 이름, b.pname 상사이름
	from personal a, personal b
	where a.manager=b.pno;

-- 8. 사번, 이름, 상사이름(상사가 없는 사람도 출력하되 상사가 없는 경우 ★CEO★로 출력) 
select w.pno 사번 , 
	   w.pname 이름, 
       if(m.pname is null,'ceo',m.pname) 상사이름
	from personal w left outer join personal m
	on w.manager=m.pno;
    
-- 8-1 사번, 이름, 상사사번(상사가 없으면 ceo로 출력. ifnull함수의 매개변수의 타입이 상이해도 상관없음)
select w.pno 사번 , 
	   w.pname 이름, 
       ifnull(w.manager, 'ceo') 상사사번
	from personal w;
    

-- 8-2. 사번, 이름, 상사이름, 부서명(상사가 없는 사람도 출력) – 같이 합시다
select w.pno 사번, 
		w.pname 이름, 
        ifnull(m.pname, '없음') 상사이름,
        d.dname 부서명
	from personal w 
		left outer join personal m 
			on w.manager=m.pno
		left outer join division d
			on w.dno=d.dno;

-- 9. 이름이 s로 시작하는 사원 이름 (like 이용, substr함수이용, instr함수 이용등 다양하게 사용 가능) like 이용 
select pname
	from personal
    where pname like's%';

-- 10. 사번, 이름, 급여, 부서명, 상사이름
select w.pno 사번, w.pname 이름, w.pay 급여, d.dname 부서명, if(m.pname is null,'ceo',m.pname) 상사이름
	from personal w 
		left outer join personal m
			on w.manager=m.pno
        left outer join division d
			on w.dno=d.dno;


-- ---------------------- --
-- ★★★★ oracle과 다른 함수들
-- ---------------------- --
-- (1)concat
select pname || '는' || job from personal; -- || : or연산자 
select concat(pname,'는',job) message from personal;

-- (2)sysdate();
select sysdate(); -- 현재 시점 

-- (3)date_format
-- to_char(hiredate, 'yy/mm/dd') -- to_char는 사용이 불가
-- date_format(날짜/시간, 포맷) => 날짜형을 문자로 변경
-- date_format(문자,     포맷) => 문자형을 날짜형으로 변경
	-- %Y(4자리 년도) , %y(2자리 년도), %m(월01,02,...), %c(1,2,...)
    -- %d(일01,02,...), %e(1,2,...), %H(24시간), %h(12시간), %p(오전,오후), %i(분), %s(초)
    
select date_format(sysdate(),'%y-%m-%d %p %h:%i:%s') now;

-- (4) 오라클의 nvl() => if() 나 ifnull()함수 사용
select * from personal;
select pname, pay, ifnull(bonus,0) bonus from personal;
select pname, pay, if(bonus is null, 0, bonus) bonus from personal; -- if(조건(보너스가 null이 있는지),조건이 충족하면 0, 조건에 불충족하면 bonus그대로) 
select pname, pay, if (pay>=3000, '부자','평범') pay2 from personal;