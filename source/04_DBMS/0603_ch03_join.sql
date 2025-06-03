-- [ III ] join : 2개 이상의 테이블을 연결하여 데이터를 검색하는 방법
SELECT * FROM EMP WHERE ENAME='SCOTT'; -- 1행
SELECT * FROM DEPT; --4행 (내선번호별 근무지, 부서가 담긴 데이터)

-- CROSS JOIN (붙이기만 함, 원하는 정보를 불러오지 못하고 다 불러옴)
SELECT * 
    FROM EMP,DEPT 
    WHERE ENAME ='SCOTT';  -- 1(EMP 테이블 갯수) * 4(DEPT 테이블 갯수) => 4행이 출력이 됨. 
    
----------------------------------------------------------    
-- ★★1. EQUI JOIN (공통필드 값이 일치되는 조건만 JOIN)
----------------------------------------------------------
SELECT EMPNO NO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPT.DEPTNO, DNAME,LOC
    FROM EMP, DEPT
    WHERE ENAME='SCOTT' AND EMP.DEPTNO=DEPT.DEPTNO; --EMP테이블의 DEPTNO와 DEPT의 DEPTNO가 같은것만 JOIN 

    -- 테이블에도 alias 넣기 적용
    SELECT EMPNO NO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, D.DEPTNO, DNAME,LOC      -- 읽는 순서
        FROM EMP E, DEPT D --테이블 Alias는 "" 쌍따옴표와 as 사용 불가                     (1)
        WHERE ENAME='SCOTT' AND E.DEPTNO=D.DEPTNO; --SCOTT의 정보                       (2)  테이블 별칭만 사용 가능 
        ORDER BY NO;                                  --                               (3)
        
    --EX 1. 모든 사원의 사번, 이름, JOB, 상사사번, 부서번호, 부서명, 근무지 출력
    SELECT EMPNO, ENAME, JOB, MGR, D.DEPTNO,DNAME, LOC 
        FROM EMP E, DEPT D 
        WHERE E.DEPTNO=D.DEPTNO;
        
    --EX2. 급여가 2000이상인 직원의 이름, JOB, 급여, 부서명, 근무지 출력
    SELECT ENAME, JOB, SAL, DNAME, LOC
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND SAL >=2000;
    
    --EX3.근무지가 CHICAGO인 직원의 이름, 업무, 부서명, 근무지 출력
    SELECT ENAME, JOB, D.DNAME 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND LOC='CHICAGO';
    
    --EX4.82년도에 입사한 10번부서, 20번 부서 직원의 이름, 급여, 근무지를 급여순으로 출력
    SELECT ENAME,SAL,LOC 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND TO_CHAR(HIREDATE,'RR')=82
            AND D.DEPTNO IN (10,20)
        ORDER BY SAL;
        
    --EX5. JOB이 'SALESMAN'이거나 'MANAGER'인 사원의 이름, 급여, 상여, 연봉(SAL+COMM)*12, 부서명, 근무지 출력 (연봉이 큰 순서로)
    SELECT ENAME, SAL, COMM, (SAL+NVL(COMM,0))*12 연봉, DNAME, LOC 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND JOB IN ('SALESMAN','MANAGER')
        ORDER BY 연봉 DESC;
        
    --EX6. COMM이 NULL이고 SAL이 2000대인 사원의 이름, 급여, 입사일, 부서번호, 부서명 (부서명순, 급여순으로 정렬)
    SELECT ENAME, SAL, HIREDATE, E.DEPTNO, DNAME 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND COMM IS NULL AND SAL BETWEEN 2000 AND 2999
        ORDER BY DNAME, SAL;
        
        
        
    --탄탄1. 뉴욕에서 근무하는 사원의 이름과 급여를 출력하시오
    SELECT ENAME, SAL 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND LOC='NEW YORK';
        
    --탄탄2. ACCOUNTING 부서 소속 사원의 이름과 입사일을 출력하시오
    SELECT ENAME, HIREDATE 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND DNAME='ACCOUNTING';
        
    --탄탄3. 직급이 MANAGER인 사원의 이름, 부서명을 출력하시오
    SELECT ENAME, DNAME 
        FROM EMP E, DEPT D
        WHERE E.DEPTNO = D.DEPTNO AND JOB='MANAGER';
    
    --탄탄4. Comm이 null이 아닌 사원의 이름, 급여, 부서코드, 근무지를 출력하시오.
    SELECT ENAME,SAL,D.DEPTNO,LOC
        FROM EMP E, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND COMM IS NOT NULL;
        
-------------------------------------     
-- ★★2. NON-EQUI JOIN 
/*(두 테이블을 동등 조건이 아닌 범위 조건
(>, <, BETWEEN 등) 으로 연결)*/
-------------------------------------
SELECT * 
    FROM EMP
    WHERE ENAME='SCOTT'; -- 지원정보
SELECT *
    FROM SALGRADE; --급여등급 정보
    
SELECT *
    FROM EMP, SALGRADE
    WHERE ENAME='SCOTT' AND SAL BETWEEN LOSAL AND HISAL;
    
    --EX1. 모든 사원의 사번, 이름, JOB, 상사사번, 급여, 급여등급(1등급,2등급,...)
    SELECT EMPNO, ENAME, JOB, MGR, SAL, GRADE||'등급' 급여등급
        FROM EMP E, SALGRADE S
        WHERE SAL BETWEEN LOSAL AND HISAL;
        
     --EX1. 모든 사원의 사번, 이름, JOB, 상사사번, 급여, 급여등급(1등급,2등급,...),부서명  
    SELECT EMPNO, ENAME, JOB, MGR, SAL, GRADE||'등급' 급여등급,DNAME
        FROM EMP E, SALGRADE, DEPT D
        WHERE SAL BETWEEN LOSAL AND HISAL AND E.DEPTNO=D.DEPTNO;     
    
     --탄탄1. Comm이 null이 아닌 사원의 이름, 급여, 등급, 부서번호, 부서이름, 근무지를 출력하시오
     SELECT ENAME, SAL, GRADE, D.DEPTNO, LOC 
        FROM EMP E, SALGRADE, DEPT D
        WHERE D.DEPTNO=E.DEPTNO AND SAL BETWEEN LOSAL AND HISAL AND NOT COMM IS NULL;
        
     --탄탄2. 이름, 급여, 입사일, 급여등급
     SELECT ENAME, SAL, HIREDATE,GRADE 
        FROM EMP E, SALGRADE, DEPT D
        WHERE D.DEPTNO=E.DEPTNO AND SAL BETWEEN LOSAL AND HISAL;
     --탄탄3. 이름, 급여, 급여등급, 연봉, 부서명을 부서명순으로 정렬하여 출력. 부서가 같으면 연봉순. 연봉=(sal+comm)*12 comm이 null이면 0
     SELECT ENAME,SAL,GRADE,(SAL+NVL(COMM,0))*12 연봉,DNAME
        FROM EMP E, SALGRADE, DEPT D
        WHERE D.DEPTNO=E.DEPTNO AND SAL BETWEEN LOSAL AND HISAL 
        ORDER BY DNAME, 연봉;
     --탄탄4. 이름, 업무, 급여, 등급, 부서코드, 부서명 출력. 급여가 1000~3000사이. 정렬조건 : 부서별, 부서같으면 업무별, 업무같으면 급여 큰순
     SELECT ENAME, JOB, SAL, GRADE, D.DEPTNO, DNAME
        FROM EMP E, SALGRADE, DEPT D
        WHERE D.DEPTNO=E.DEPTNO AND SAL BETWEEN LOSAL AND HISAL AND SAL BETWEEN 1000 AND 3000 
        ORDER BY DNAME,JOB,SAL DESC;
     --탄탄5. 이름, 급여, 등급, 입사일, 근무지. 81년에 입사한 사람. 등급 큰순
     SELECT ENAME,SAL,GRADE,HIREDATE,LOC
        FROM EMP E, SALGRADE, DEPT D
        WHERE E.DEPTNO=D.DEPTNO AND SAL BETWEEN LOSAL AND HISAL AND TO_CHAR(HIREDATE, 'RR')=81
        ORDER BY GRADE DESC;
        
-------------------------------------       
-- ★★3. SELF JOIN ()
-------------------------------------
SELECT * 
    FROM EMP
    WHERE ENAME='SMITH'; 

SELECT EMPNO, ENAME 
    FROM EMP 
    WHERE EMPNO=7902;
    
SELECT WORKER.EMPNO, WORKER.ENAME, WORKER.MGR, MANAGER.EMPNO, MANAGER.ENAME
    FROM EMP WORKER, EMP MANAGER
    WHERE WORKER.MGR = MANAGER.EMPNO AND WORKER.ENAME='SMITH';
    
SELECT WORKER.EMPNO, WORKER.ENAME, WORKER.MGR, MANAGER.EMPNO, MANAGER.ENAME
    FROM EMP WORKER, EMP MANAGER
    WHERE WORKER.MGR = MANAGER.EMPNO ;
    --EX 1. 모든 사원의 사번, 이름, 상사의 사번, 상사이름
    SELECT W.EMPNO, W.ENAME, W.MGR, M.ENAME 상사이름
        FROM EMP W, EMP M
        WHERE W.MGR=M.EMPNO;
        
    --EX 2. 'SMITH'의 상사는 JONES이다' 포맷으로 출력
    SELECT W.ENAME ||'의 상사는' || M.ENAME  || '이다' MESSAGE
        FROM EMP W , EMP M
        WHERE W.MGR=M.EMPNO; --MGR에 NULL이 있어서 13명으로 출력
 
     --탄탄1. 매니저가 KING인 사원들의 이름과 직급을 출력
     SELECT W.ENAME, W.JOB--, W.MGR, M.ENAME
        FROM EMP W, EMP M
        WHERE W.MGR=M.EMPNO AND M.ENAME='KING';
        
    SELECT EMPNO FROM EMP WHERE ENAME='KING'; --KING의 사번 찾기
    
    SELECT ENAME, JOB  FROM EMP
        WHERE MGR = (SELECT EMPNO FROM EMP WHERE ENAME='KING');--서브쿼리

     --탄탄2. SCOTT과 동일한 부서에서 근무하는 사원의 이름을 출력
     SELECT E2.ENAME
        FROM EMP E1, EMP E2
        WHERE E1.ENAME='SCOTT' AND E1.DEPTNO=E2.DEPTNO 
            AND E2.ENAME <> 'SCOTT'; -- SELF JOIN 이용
     
     SELECT  ENAME 
        FROM EMP
        WHERE DEPTNO = (SELECT DEPTNO FROM EMP WHERE  ENAME='SCOTT') 
            AND ENAME != 'SCOTT'; --서브쿼리 이용 , 스칼라데이터로 나와야 함
        
        SELECT DEPTNO FROM EMP WHERE  ENAME='SCOTT'; --SCOTT의 근무부서 번호 찾기
        
     --탄탄3. SCOTT과 동일한 근무지에서 근무하는 사원의 이름을 출력 (subquery 사용 추천)
     SELECT ENAME
        FROM EMP
        WHERE LOC = 
        SELECT ;
        
 -------------------------------------       
-- ★★4. OUTER JOIN 
/*  SELF JOIN, EQUI JOIN시 조건이
 만족하지 않는 행까지 나타나게 하는 
  OUTER JOIN */
-------------------------------------    
    --(1) SELF JOIN에서 OUTER JOIN
    -- 배제된 행을 결과에 포함시킬 경우 (+) 기호를 정보가 부족한 컬럼이름 뒤에 덧붙임
    SELECT W.EMPNO, W.ENAME, W.MGR, M.EMPNO, M.ENAME
        FROM EMP W, EMP M
        WHERE W.MGR = M.EMPNO(+);
        --EX. 모든 사원에 대해 'SMITH의 상사는 FORD이다' ... 'KING의 상사는  없다'
            SELECT W.ENAME || '의 상사는 ' || NVL(M.ENAME, '없') || '다'   MASSAGE 
                FROM EMP W, EMP M
                WHERE W.MGR = M.EMPNO(+);
        --EX. 말단 직원 <★★★★★★★★★다시 하기
        SELECT M.ENAME
            FROM EMP W, EMP M
            WHERE W.MGR(+) = M.ENAME AND W.ENAME IS NULL;
            
    --(2)  EQUI JOIN에서의 OUTER JOIN
    SELECT * FROM DEPT; -- 10,20,30,40
    SELECT * FROM EMP; 10,20,30
    SELECT ENAME, E.DEPTNO, DNAME
        FROM EMP E, DEPT D
        WHERE E.DEPTNO (+)=D.DEPTNO;
        
        
        
   ------------------------------------------
   -- ★ <총 연습문제>
  -- < part1>
-- 1.모든 사원에 대한 이름, 부서번호, 부서명을 출력하는 SELECT 문장을 작성
  SELECT ENAME,E.DEPTNO,DNAME 
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO;
    
-- 2.NEW YORK에서 근무하고 있는 사원에 대하여 이름, 업무, 급여, 부서명을 출력
SELECT ENAME, JOB, SAL, ENAME
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO AND LOC='NEW YORK';
    
-- 3.보너스를 받는 사원에 대하여 이름,부서명,위치를 출력
SELECT ENAME,DNAME,LOC 
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO AND COMM IS NOT NULL AND COMM!=0;
    
 -- 4.이름중 L자가 있는 사원에 대하여 이름,업무,부서명,위치를 출력
 SELECT ENAME,JOB,DNAME,LOC
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO AND ENAME LIKE '%L%';
    
-- 5.사번, 사원명,부서코드,부서명을 검색 (사원명기준 오름차순)
SELECT EMPNO,ENAME,D.DEPTNO,DNAME
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO
    ORDER BY ENAME ;
    
-- 6.사번, 사원명,급여,부서명을 검색 (급여가 2000이상인 사원에 대하여 급여기준 내림차순)  
 SELECT EMPNO,ENAME,SAL,DNAME
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO AND SAL >=2000
    ORDER BY SAL DESC;
       
 -- 7.사번, 사원명,업무,급여,부서명을 검색 (업무는 MANAGER이고 급여는 2500이상  사번기준 오름차순)    
 SELECT EMPNO, ENAME,JOB,SAL,DNAME 
    FROM EMP E, DEPT D
    WHERE E.DEPTNO=D.DEPTNO AND JOB='MANAGER' AND SAL>=2500
    ORDER BY EMPNO;
    
 -- 8.사번, 사원명,업무,급여,등급을 검색 (급여기준 내림차순)
 SELECT EMPNO,ENAME,JOB,SAL,GRADE
    FROM EMP E, DEPT D, SALGRADE
    WHERE  SAL BETWEEN LOSAL AND HISAL AND E.DEPTNO=D.DEPTNO 
    ORDER BY SAL;

  -- < part2>
-- 1. 이름, 직속상사명
SELECT W.ENAME 이름, M.ENAME 직속상사명
    FROM EMP W ,  EMP M
    WHERE W.MGR=M.EMPNO;
    
-- 2. 이름,급여,업무,직속상사명
SELECT W.ENAME 이름, W.SAL 급여, W.JOB 업무, M.ENAME 직속상사명
    FROM EMP W , EMP M
    WHERE W.MGR=M.EMPNO;
    
--3. 이름,급여,업무,직속상사명.(상사가 없는 직원까지 전체 직원 다 출력 / 상사 없을시 '없음'으로 출력)
SELECT W.ENAME 이름, W.SAL 급여,  W.JOB 업무,NVL( M.ENAME , '없음') 직속상사명
    FROM EMP W , EMP M
    WHERE W.MGR=M.EMPNO(+) ; 
    
-- 4. 이름, 급여, 부서명, 직속상사명   
SELECT W.ENAME 이름, W.SAL 급여, DNAME 부서명, M.ENAME 직속상사명
    FROM EMP W, EMP M, DEPT D
    WHERE W.MGR=M.EMPNO AND W.DEPTNO=D.DEPTNO;
    
-- 5. 이름,급여,부서코드,부서명,근무지, 직속상사명을 출력 (직속상사가 없을 경우 '없음'으로 출력)
SELECT W.ENAME 이름, W.SAL 급여, D.DEPTNO 부서코드, D.LOC 근무지 , NVL(M.ENAME,'없음') 직속상사명
    FROM EMP W, EMP M, DEPT D
    WHERE D.DEPTNO=W.DEPTNO AND W.MGR=M.EMPNO(+);
    
 -- 6. 이름,급여,등급,부서명,직속상사명(급여가 2000이상인 사람만 출력)
 SELECT W.ENAME 이름, W.SAL 급여, GRADE 등급, D.DNAME 부서명, M.ENAME 직속상사명
    FROM  EMP W, EMP M, SALGRADE S, DEPT D
    WHERE W.MGR=M.EMPNO 
        AND W. SAL BETWEEN S.LOSAL AND S.HISAL 
        AND D.DEPTNO=W.DEPTNO 
        AND W.SAL >=2000;
    
 -- 7. 이름,급여,등급,부서명,직속상사명(직속상사가 없는 직원까지 전체직원 부서명 정렬)  
SELECT W.ENAME 이름, W.SAL 급여, GRADE 등급, D.DNAME 부서명, NVL(M.ENAME,'없음') 직속상사명
    FROM  EMP W, EMP M, SALGRADE S, DEPT D
    WHERE W.MGR=M.EMPNO(+)
        AND W. SAL BETWEEN S.LOSAL AND S.HISAL 
        AND D.DEPTNO=W.DEPTNO;   

 -- 8. 이름,급여,등급,부서명,연봉,직속상사명(연봉 = (급여+COMM)*12)
 SELECT W.ENAME 이름, W.SAL 급여, GRADE 등급, D.DNAME 부서명, (W.SAL+NVL(W.COMM, 0))*12 연봉 , M.ENAME 직속상사명
    FROM EMP W, EMP M, SALGRADE S, DEPT D
    WHERE D.DEPTNO=W.DEPTNO 
        AND W.SAL BETWEEN S.LOSAL AND S.HISAL
        AND W.MGR=M.EMPNO;
 
  -- 9. 이름,급여,등급,부서명,연봉,직속상사명(연봉 = (급여+COMM)*12)/ (부서명, 급여 큰 순으로 정렬)
 SELECT W.ENAME 이름, W.SAL 급여, GRADE 등급, D.DNAME 부서명, (W.SAL+NVL(W.COMM, 0))*12 연봉 , M.ENAME 직속상사명
    FROM EMP W, EMP M, SALGRADE S, DEPT D
    WHERE D.DEPTNO=W.DEPTNO 
        AND W.SAL BETWEEN S.LOSAL AND S.HISAL
        AND W.MGR=M.EMPNO
    ORDER BY D.DNAME, W.SAL DESC;    
        
-- 10.사원테이블에서 사원명, 사원의 상사를 검색하시오 (상사가 없는 직원까지)
SELECT W.ENAME 사원명, NVL(M.ENAME, '없음')
    FROM EMP W, EMP M
    WHERE W.MGR = M.EMPNO (+); 

--11. 사원명, 상사명, 상사의 상사명을 검색하시오(self join)
SELECT W.ENAME 사원명,M.ENAME 상사명, K.ENAME 상사의상사명
    FROM EMP W, EMP M, EMP K
    WHERE W.MGR=M.EMPNO 
        AND M.MGR=K.EMPNO;
        
--12. 위의 결과에서 상위 상사가 없는 모든 직원의 이름도 출력되도록 수정하시오(outer join)
SELECT W.ENAME 사원명,NVL(M.ENAME,'없음') 상사명, NVL(K.ENAME,'없음') 상사의상사명
    FROM EMP W, EMP M, EMP K
    WHERE W.MGR=M.EMPNO(+) 
        AND M.MGR=K.EMPNO(+);