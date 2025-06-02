-- [II] SELECT 문 /* 여러줄 주석 */
-- 1. SELECT 문 작성법
SHOW USER;
    --현재 계정(실행 방법 : CTRL + ENTER)
SELECT * FROM TAB; -- 현 계정이 가지고 있는 테이블들
SELECT * FROM EMP; -- EMP테이블의 모든열, 모든행 출력 / FROM 다음에는 테이블 이름이 와야 함.SELECT뒤에는 열이름
SELECT * FROM DEPT; -- DEPT테이블의 모든 열, 모든 행
SELECT * FROM SALGRADE;
SELECT * FROM TAB;

-- 2.특정열만 출력하는 방법
DESC EMP; 
    -- EMP테이블 구조를 나타내는 ORACLE 명령어
    -- NUMBER(7,2)는 숫자 7자리 소수점2자리
    -- NOT NULL은 프라이머리키
SELECT EMPNO, ENAME, SAL, JOB FROM EMP; -- EMPNO, ENAME, SAL, JOB 열만 모든행 검색
SELECT EMPNO AS "사 번", ENAME AS "이름", SAL AS "급여", JOB AS "직책" FROM EMP; --AS는 alias의 약자 
SELECT EMPNO  "사 번", ENAME  "이름", SAL  "급여", JOB  "직책" FROM EMP; -- AS 빼도 가능
SELECT EMPNO  "사 번", ENAME  이름, SAL  급여, JOB  직책 FROM EMP; -- ""를 빼도 가능 (텍스트에도 가능하나 스페이시는 허용이 안됨)
SELECT EMPNO NO, ENAME ENAME, SAL SALARY FROM EMP; -- 

-- 3.특정행만 출력하는 방법 (WHERE절 - 조건절) - 비교연산자 : 같다(=), 다르다(!=, ^=,<>),>,>=,<,<=
SELECT EMPNO NO, ENAME, SAL FROM EMP WHERE SAL=3000; -- SAL이 3000인 행만 출력 
SELECT EMPNO NO, ENAME, SAL FROM EMP WHERE SAL^=3000; 
SELECT EMPNO NO, ENAME, SAL FROM EMP WHERE SAL<>3000; 
SELECT EMPNO NO, ENAME, SAL FROM EMP WHERE SAL!=3000; 
    -- 비교연산자는 숫자,문자,날짜형 모두 가능
    -- EX1) 사원 이름(ENAME)이 'A','B','C'로 시작하는 사원의 모든 필드
    -- 'A' < 'AA' < 'AAA' < 'AAAA' < 'B' < 'C' < 'D'
    SELECT * FROM EMP WHERE ENAME < 'D';
    
    -- EX2) 81년도 이전에 입사한 사워의 모든 필드
    SELECT * FROM EMP WHERE HIREDATE < '81/01/01';
    SELECT * FROM EMP WHERE HIREDATE > '81/01/01';
    
    -- EX3) 부서번호(DEPTNO) 가 10번인 모든 사원의 모든 필드 출력
    SELECT * FROM EMP WHERE DEPTNO=10;
    
    -- EX4) 이름(ENAME)이 FORD인 직원의 EMPNO, ENAME, MGR(상사의 사번)을 출력
    SELECT EMPNO, ENAME, MGR 
    FROM EMP
    WHERE ENAME = 'FORD';
    -- SQL문은 대소문자 구별없음 (데이터는 대소문자 구분함)
    
-- 4.특정행만 출력하는 방법 (WHERE절 - 조건절) - 논리연산자 : AND, OR, NOT 
    -- EX1) 급여(SAL)가 2000이상 3000이하인 직원의 모든 필드를 출력
    SELECT * FROM EMP 
    WHERE SAL >= 2000 AND SAL <= 3000;
    
    -- EX2) 입사일(HIREDATE)이 82년도에 입사한 사워의 모든 필드
    SELECT * FROM EMP 
    WHERE HIREDATE >= '82/01/01' AND HIREDATE <= '82/12/31';
    -- "" 과  '' 사용법  : alias(AS)에는 ""을 사용, 문자는 '' 사용 
    
    --날짜 표기법 세팅 (현재 : YY/MM/DD 또는 RR / MM / DD)
    ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD';
    ALTER SESSION SET NLS_DATE_FORMAT = 'YY/MM/DD';
    SELECT * FROM EMP;
    SELECT TO_CHAR(HIREDATE,'YY/MM/DD') FROM EMP;
    
    -- 날짜 세팅을 고려한 82년도 입사한 사원의 모든 필드
    SELECT * FROM EMP 
        WHERE TO_CHAR(HIREDATE, 'YY/MM/DD') >= '82/01/01' AND
            TO_CHAR(HIREDATE, 'YY/MM/DD') <= '82/12/31';
            
            
    -- EX3) 연봉이 2400이상인 직원의 ENAME, SAL, 연봉(SAL*12)을 출력
    SELECT * FROM EMP;
    SELECT ENAME, SAL, SAL*12 ANNUALSAL  -- 수행순서 : 3번째
    FROM EMP                             -- 수행순서 : 1번째
    WHERE SAL*12 >=2400;                 -- 수행순서 : 2번째 WHERE절에는 필드의 별칭 사용이 불가 
    
    -- EX4) 연봉이 3000이상인 직원의 ENAME, SAL, 연봉을 연봉순으로 출력
    SELECT ENAME, SAL, SAL*12 연봉        -- 수행순서 : 3번
    FROM EMP                             -- 수행순서 : 1번
    WHERE SAL*12 >=3000                  -- 수행순서 : 2번 (WHERE절에는 필드의 별칭 사용 불가)
    ORDER BY 연봉;                        -- 수행순서 : 4번 (ORDER BY절에는 필드의 별칭 사용 가능)
    
    -- EX5) JOB이 MANAGER이거나 10번 부서(DEPTNO) 직원의 모든 필드 출력
    SELECT * FROM EMP WHERE JOB='MANAGER' OR DEPTNO != 10;
-- 5. 산술연산자 (SELECT절, 조건절, ORDER BY절)
    -- 모든 사원의 월급을 10% 인상된 월급과 사번(EMPNO), 이름(ENAME) 출력
    SELECT EMPNO, ENAME, SAL*1.1 FROM EMP;
    
    -- 모든 사원의 이름(ENAME),월급(SAL),상여(COMM),연봉(SAL*12+COMM)을 출력
    SELECT ENAME, SAL, COMM, SAL*12+COMM 연봉 FROM EMP;
    
    -- 산술연산의 결과는 NULL을 포함하면 결과도 NULL이다.
    -- NVL(NULL 일 수도 있는 필드명, NULL을 대체할 값)을 이용 -  두 매개변수의 타입이 일치해야 대체값이 작성이 됨
    SELECT ENAME, SAL, NVL(COMM, 0), SAL*12+NVL(COMM, 0) 연봉 FROM EMP;
    
    -- 모든 사원의 사번,이름 상사사번(MGR)출력 (상사가 없으면 'CEO'로 출력) 
    SELECT EMPNO, ENAME, NVL(TO_CHAR(MGR), 'CEO') FROM EMP;
    
-- 6. 연결연산자(||) : 필드값이나 문자를 연결 // EMPLOYEE는 별칭(alias)
SELECT ENAME || '는 ' || JOB EMPLOYEE FROM EMP;

-- 7. 중복제거(DISTINCT)
SELECT DISTINCT JOB FROM EMP;
SELECT DISTINCT DEPTNO FROM EMP;

--연습문제 1차
-- Q1. 테이블이의 구조 출력
DESC EMP;

-- Q2. EMP 테이블의 모든 내용 출력
SELECT * FROM EMP; 

--Q3. 현 scott 계정에서 사용가능한 테이블 출력

--Q4. emp 테이블에서 사번, 이름, 급여, 업무, 입사일 출력

--Q5. emp 테이블에서 급여가 2000미만인 사람의 사번, 이름, 급여 출력

--Q6. 입사일이 81/02이후에 입사한 사람의 사번, 이름, 업무, 입사일 출력

--Q7. 업무가 SALESMAN인 사람들 모든 자료 출력

--Q8. 업무가 CLERK이 아닌 사람들 모든 자료 출력

--Q9. 급여가 1500이상이고 3000이하인 사람의 사번, 이름, 급여 출력

--Q10. 부서코드가 10번이거나 30인 사람의 사번, 이름, 업무, 부서코드 출력

--Q11. 업무가 SALESMAN이거나 급여가 3000이상인 사람의 사번, 이름, 업무, 부서코드 출력

--Q12. 급여가 2500이상이고 업무가 MANAGER인 사람의 사번, 이름, 업무, 급여 출력

--Q13.“ename은 XXX 업무이고 연봉은 XX다” 스타일로 모두 출력(연봉은 SAL*12+COMM)

--연습문제 끝

-- 8. SQL연산자(BETWEEN, IN, LIKE, IS NULL) IS NULL = NULL인지 확인하는것 -NULL이냐 
    --(1) BETWEEN A AND B : A부터 B까지(A,B 포함) A가 작은 값이여야 함. A가 B보다 더 크면 실행이 안 됨. 
        --EX1. SAL이 1500이상 3000이하인 직원의 사번, 이름, 급여
        SELECT EMPNO, ENAME, SAL FROM EMP WHERE SAL >= 1500 AND SAL <=3000; 
        SELECT EMPNO, ENAME, SAL FROM EMP
        WHERE SAL BETWEEN 1500 AND 3000
        ORDER BY SAL;
        
        --EX2. SAL이 1500미만, 3000 초과 (NOT BETWEEN 사용)
        SELECT EMPNO, ENAME, SAL FROM EMP
        WHERE SAL NOT BETWEEN 1500 AND 3000
        ORDER BY SAL;
        
        --EX3. 이름이 'A','B','C' 로 시작하는 직원의 모든 필드
        SELECT *FROM EMP
        WHERE ENAME BETWEEN 'A' AND 'D' AND ENAME!='D'; -- A부터 D까지중에 D는 빼고 찾기
        
        --EX4. 82년도 입사한 직원의 모든 필드 출력
        SELECT * FROM EMP
        WHERE TO_CHAR(HIREDATE) BETWEEN '1982-01-01' AND '1982-12-31';
        
    -- (2) 필드명 IN 연산자  (값1, 값2, 값3,...값n)
        --EX1. 부서번호(DEPTNO)가 10,20,40번인 직원의 모든 필드
        SELECT * FROM EMP
        WHERE DEPTNO IN(10,20,40);
        
        --EX2. 직책(JOB)이 MANAGER거나 ANALYST인 사원의 모든 필드 
        SELECT * FROM EMP
        WHERE JOB IN ('MANAGER','ANALYST');
        
    --(3) 필드명 LIKE 패턴 ( 해당필드가 다음패턴과 같으면 출력) : %(0글자 이상), _(1글자)를 포함한 패턴
        --EX1. 이름이 M으로 시작하는 사원의 모든 필드 
        SELECT * FROM EMP WHERE ENAME LIKE 'M%';
        
        --EX2. 이름에 N이 들어가거나 JOB에 N이 들어가는 직원의 모든 필드
        SELECT * FROM EMP 
        WHERE ENAME LIKE '%N%' OR JOB LIKE '%N%';
        
        --EX3. 급여(SAL)가 5로 끝나는 사원의 모든 필드
        SELECT * FROM EMP
        WHERE SAL LIKE '%5';
        
        --EX4. 82년도의 입사한 사원의 모든 필드
        SELECT * FROM EMP
        WHERE TO_CHAR(HIREDATE) LIKE '1982-%';
        
        --EX5. 1월에 입사한 사원의 모든 필드 <?>
        SELECT * FROM EMP
        WHERE HIREDATE LIKE '__/01/__';
        
    --(4) 필드 IS NULL (해당 필드가 널인지 여부)
        --EX1. 상여금(COMM)을 받지 않느느 사원의 모든 필드
        SELECT * FROM EMP
        WHERE COMM=0 OR COMM IS NULL;; --COMM=NULL이라고 쓰면 0인 사람만 출력이 되어서 이렇게 하면 안됨
        
        --EX2. 상여금(COMM)을 받는 사원의 모든 필드
        SELECT * FROM EMP
        WHERE COMM!=0 AND COMM IS NOT NULL; -- WHERE COMM!=0 AND NOT COMM IS NULL로 써도 됨.

-- 9. 정렬(오름차순, 내림차순) : ORDER BY절
SELECT * FROM EMP
ORDER BY SAL;  -- SAL기준 오름차순 정렬 
SELECT * FROM EMP
ORDER BY SAL, ENAME; -- SAL 기준으로 오름차순 정렬(SAL이 같으면 ENAME순 오름차순 정렬)
SELECT * FROM EMP
ORDER BY SAL DESC; -- SAL기준 내림차순 정렬 
SELECT * FROM EMP
ORDER BY SAL DESC, HIREDATE DESC; -- SAL기준 내림차순 정렬(SAL이 같으면 HIREDATE 기준으로 내림차순) 

-- 연습문제 전 형변환 함수 : TO_CHAR, TO_DATE
-- 날짜형(HIREDATE)를 문자형으로 변환 : TO_CHAR(날짜형 데이터, 패턴)
        -- YYYY,YY,RR:년도/ MM 월 / DD 일 / DY 월 / DAY 월요일 
        -- HH24(24시간), HH12, HH : 시 / AM이나 PM / MI 분 / SS 초
    SELECT ENAME, TO_CHAR(HIREDATE, 'YY/MM/DD AM H12:MI:SS') FROM EMP;
    --82년전에 입사한 사원의 데이터
    SELECT * FROM EMP WHERE TO_CHAR(HIREDATE, 'RR/MM/DD') < '82/01/01';
    SELECT * FROM EMP WHERE HIREDATE < TO_DATE('82/01/01', 'RR/MM/DD'); -- TO_DATE 문자를 날짜로 바꾸는것 



-- 연습문제 2차  
-- Q1. EMP 테이블에서 sal이 3000이상인 사원의 empno, ename, job, sal을 출력
SELECT EMPNO, ENAME, JOB, SAL FROM EMP
WHERE SAL >= 3000;
-- Q2. EMP 테이블에서 empno가 7788인 사원의 ename과 deptno를 출력
SELECT ENAME, DEPTNO FROM EMP
WHERE EMPNO =7788;
-- Q3.	연봉(SAL*12+COMM)이 24000이상인 사번, 이름, 급여 출력 (급여순정렬)
SELECT EMPNO, ENAME, SAL 급여, SAL*12+NVL(COMM,0) 연봉
FROM EMP
WHERE SAL*12+NVL(COMM,0) >= 24000
ORDER BY 급여; 

-- Q4.	입사일이 1981년 2월 20과 1981년 5월 1일 사이에 입사한 사원의 사원명, 직책, 입사일을 출력 (단 hiredate 순으로 출력)
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD';
SELECT ENAME, JOB, HIREDATE 
FROM EMP
WHERE TO_CHAR(HIREDATE, 'YYYY-MM-DD') BETWEEN '1981-02-20' AND '1981-05-01'
ORDER BY HIREDATE;

-- Q5.	deptno가 10,20인 사원의 모든 정보를 출력 (단 ename순으로 정렬)
SELECT * FROM EMP WHERE DEPTNO IN(10,20)
ORDER BY ENAME;
-- Q6.	sal이 1500이상이고 deptno가 10,30인 사원의 ename과 sal를 출력
-- (단 출력되는 결과의 타이틀을 employee과 Monthly Salary로 출력)
SELECT ENAME || '의 급여는' || SAL || '입니다.' FROM EMP
WHERE SAL >= 1500 AND DEPTNO in (10,30);

-- Q7.	hiredate가 1982년인 사원의 모든 정보를 출력
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD';
SELECT * FROM EMP
WHERE TO_CHAR(HIREDATE, 'YYYY-MM-DD')BETWEEN '1982-01-01' AND '1982-12-31';

-- Q8.	이름의 첫자가 C부터  P로 시작하는 사람의 이름, 급여 이름순 정렬 
SELECT ENAME, SAL FROM EMP
WHERE ENAME BETWEEN'C' AND 'P'
ORDER BY ENAME;

-- Q9.	comm이 sal보다 10%가 많은 모든 사원에 대하여 이름, 급여, 상여금을 
--출력하는 SELECT 문을 작성 
SELECT ENAME,SAL,NVL(COMM,0) FROM EMP
WHERE COMM/SAL >=1.1;


-- Q10.	job이 CLERK이거나 ANALYST이고 sal이 1000,3000,5000이 아닌 모든 사원의 정보를 출력
SELECT * FROM EMP
WHERE JOB IN('CLERK','ANALYST') AND  SAL NOT IN (1000,3000,5000);

-- Q11.	ename에 L이 두 자가 있고 deptno가 30이거나 또는 mgr이 7782인 사원의 
--모든 정보를 출력하는 SELECT 문을 작성하여라.
SELECT * FROM EMP
WHERE ENAME LIKE '%LL%' AND DEPTNO = 30 OR MGR = 7782;

-- Q12.	입사일이 81년도인 직원의 사번, 사원명, 입사일, 업무, 급여를 출력
ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD';
SELECT EMPNO,ENAME,HIREDATE,JOB,SAL FROM EMP
WHERE TO_CHAR(HIREDATE, 'YYYY-MM-DD') BETWEEN '1981-01-01' AND '1981-12-31';

-- Q13.	입사일이81년이고 업무가 'SALESMAN'이 아닌 직원의 사번, 사원명, 입사일, 
-- 업무, 급여를 검색하시오.
SELECT EMPNO, ENAME, HIREDATE,JOB,SAL FROM EMP
WHERE TO_CHAR(HIREDATE, 'YYYY-MM-DD') BETWEEN '1981-01-01' AND '1981-12-31' 
    AND JOB!='SALESMAN';

-- Q14.	사번, 사원명, 입사일, 업무, 급여를 급여가 높은 순으로 정렬하고, 
-- 급여가 같으면 입사일이 빠른 사원으로 정렬하시오. 
SELECT EMPNO, ENAME, HIREDATE,JOB,SAL FROM EMP
ORDER BY SAL DESC, HIREDATE;

-- Q15.	사원명의 세 번째 알파벳이 'N'인 사원의 사번, 사원명을 검색하시오 <문의>
SELECT EMPNO, ENAME FROM EMP
WHERE ENAME LIKE '__N%';
-- Q16.	사원명에 'A'가 들어간 사원의 사번, 사원명을 출력
SELECT EMPNO, ENAME FROM EMP
WHERE ENAME LIKE '%A%';
-- Q17.	연봉(SAL*12)이 35000 이상인 사번, 사원명, 연봉을 검색 하시오.
SELECT EMPNO, ENAME, SAL*12 연봉 FROM EMP
WHERE SAL*12 >=35000;

--연습문제 끝
