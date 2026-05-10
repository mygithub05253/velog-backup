# 8장 SQL 응용

**Published:** 2026-03-26T07:05:01.562Z
**Link:** https://velog.io/@kik328288/8장-SQL-응용

---

# Section 102 SQL - DDL
## DDL (Data Define Language, 데이터 정의어)
- DB 구조, 데이터 형식, 접근 방식 등 DB를 구축하거나 수정할 목적으로 사용하는 언어
- 번역한 결과가 데이터 사전(Data Dictionary)이라는 특별한 파일에 여러 개의 테이블로 저장됨
### DDL의 3가지 유형
1. CRATE : SCHEMA, DOMAIN, TABLE, VIEW, INDEX 정의
2. ALTER : TABLE에 대한 정의를 변경하는데 사용
3. DROP : SCHEMA, DOMAIN, TABLE, VIEW, INDEX 제거(삭제)
## CREATE SCHEMA
- 스키마를 정의하는 명령문
	- 데이터베이스의 구조와 제약 조건에 관한 전반적인 명세를 기술한 것
	- 데이터 개체, 속성, 관계 및 데이터 조작 시 데이터 값들이 갖는 제약 조건 등에 관해 전반적으로 정의
### 표기 형식
```sql
CREATE SCHEMA 스키마명 AUTHORIZATION 사용자_id;
```
## CREATE DOMAIN
- 도메인을 정의하는 명령문
	- 하나의 속성이 취할 수 있는 동일한 유형의 원자값들의 집합
	- 특정 속성에서 사용할 데이터의 범위를 사용자가 정의하는 사용자 정의 데이터 타입
### 표기 형식
```sql
CREATE DOMAIN 도메인명 [AS] 데이터_타입
	[DEFAULT 기본값]
	[CONSTRAINT 제약조건명 CHECK (범위값)];
```
- 데이터 타입 : SQL에서 지원하는 데이터 타입
- 기본값 : 데이터를 입력하지 않았을 때 자동으로 입력되는 값
## CREATE TABLE
- 테이블을 정의하는 명령문
	- 데이터베이스의 설계 단계에서는 주로 릴레이션이라 부름
	- 조작이나 검색 시에는 테이블이라 부름
### 표기 형식
```sql
CREATE TABLE 테이블명
	(속성명 데이터_타입 [DEFAULT 기본값] [NOT NULL], ...
	[, PRIMARY KEY(기본키_속성명, ...)]
	[, UNIQUE(대체키_속성명, ...)]
	[, FOREIGN KEY(외래키_속성명, ...)
		REFERERENCES 참조테이블(기본키_속성명, ...)]
		[ON DELETE 옵션]
		[ON UPDATE 옵션]
	[, CONSTRAINT 제약조건명] [CHECK (조건식)]);
```
- 기본 테이블에 포함될 모든 속성에 대하여 속성명과 그 속성의 데이터 타입, 기본값, NOT NULL 여부 지정
- PRIMARY KEY : 기본키로 사용할 속성을 지정
- UNIQUE : 대체키로 사용할 속성을 지정하며 중복된 값을 가질 수 없음
- FOREIGN KEY ~ REFERENCES ~ : 외래키로 사용할 속성을 지정
	- ON DELETE 옵션 : 참조 테이블의 튜플이 삭제되었을 때 기본 테이블에 취해야 할 사항을 지정
	- ON UPDATE 옵션 : 참조 테이블의 참조 속성 값이 변경되었을 때 기본 테이블에 취해야 할 사항을 지정
- CONSTRAINT : 제약 조건의 이름 지정
- CHECK : 속성 값에 대한 제약 조건 정의
## CREATE VIEW
- 뷰를 정의하는 명령문
	- 하나 이상의 기본 테이블로부터 유도되는 이름을 갖는 가상 테이블
	- 테이블은 물리적으로 구현되어 실제로 데이터가 저장되지만, 뷰는 물리적으로 구현되지 않음
	- 즉, 뷰를 생성하면 뷰 정의가 시스템 내에 저장되었다가 SQL 내에서 뷰 이름을 사용하면 실행 시간에 뷰 정의가 대체되어 수행
### 표기 형식
```sql
CREATE VIEW 뷰명[(속성명[, 속성명, ...])]
	AS SELECT문;
```
## CREATE INDEX
- 인덱스를 정의하는 명령문
	- 검색 시간을 단축시키기 위해 만든 보조적인 데이터 구조
### 표기 형식
```sql
CREATE [UNIQUE] INDEX 인덱스명
	ON 테이블명(속성명 [ASC | DESC] [, 속성명 [ASC | DESC]])
	[CLUSTER];
```
- UNIQUE
	- 사용된 경우 : 중복 값이 없는 속성으로 인덱스를 생성
	- 생략된 경우 : 중복 값을 허용하는 속성으로 인덱스를 생성
- 정렬 여부 지정
	- ASC : 오름차순 정렬
	- DESC : 내림차순 정렬
	- 생략된 경우 : 오름차순으로 정렬
- CLUSTER : 사용하면 인덱스가 클러스터드 인덱스로 설정
	- 인덱스 키의 순서에 따라 데이터가 정렬되어 저장되는 방식
	- 데이터 삽입, 삭제 발생 시 순서를 유지하기 위해 데이터를 재정렬해야 함
## ALTER TABLE
- 테이블에 대한 정의를 변경하는 명령문
### 표기 형식
```sql
ALTER TABLE 테이블명 ADD 속성명 데이터_타입 [DEFAULT '기본값'];
ALTER TABLE 테이블명 ALTER 속성명 [SET DEFAULT '기본값'];
ALTER TABLE 테이블명 DROP COLUMN 속성명 [CASCADE];
```
- ADD : 새로운 속성(열)을 추가할 때 사용
- ALTER : 특정 속성의 DEFAULT 값을 변경할 때 사용
- DROP COLUMN : 특정 속성을 삭제할 때 사용
## DROP
- 스키마, 도메인, 기본 테이블, 뷰 테이블, 인덱스, 제약 조건 등을 제거하는 명령문
### 표기 형식
```sql
DROP SCHEMA 스키마명 [CASCADE | RESTRICT];
DROP DOMAIN 도메인명 [CASCADE | RESTRICT];
DROP TABLE 테이블명 [CASCADE | RESTRICT];
DROP VIEW 뷰명 [CASCADE | RESTRICT];
DROP INDEX 인덱스명 [CASCADE | RESTRICT];
DROP CONSTRAINT 제약조건명;
```
- CASCADE : 제거할 요소를 참조하는 다른 모든 개체를 함께 제거
- RESTRICT : 다른 개체가 제거할 요소를 참조 중일 때는 제거를 취소
# Section 103 SQL - DCL
## DCL (Data Control Language, 데이터 제어어)
- 데이터의 보안, 무결성, 회복, 병행 제어 등을 정의하는 데 사용하는 언어
- 데이터베이스 관리자(DBA)가 데이터 관리를 목적으로 사용
### DCL의 종류
1. COMMIT : 명령에 의해 수행된 결과를 실제 물리적 디스크로 저장하고, 데이터베이스 조작 작업이 정상적으로 완료되었음을 관리자에게 알려줌
2. ROLLBACK : 데이터베이스 조작 작업이 비정상적으로 종료되었을 때 원래의 상태로 복구
3. GRANT : 데이터베이스 사용자에게 사용 권한을 부여
4. REVOKE : 데이터베이스 사용자의 사용 권한을 취소
## GRANT / REVOKE
- 데이터베이스 관리자가 데이터베이스 사용자에게 권한을 부여하거나 취소하기 위한 명령어
- GRANT : 권한 부여를 위한 명령어
- REVOKE : 권한 취소를 위한 명령어
### 사용자 등급 지정 및 해제
- DBA : 데이터베이스 관리자
- RESOURCE : 데이터베이스 및 테이블 생성 가능자
- CONNECT : 단순 사용자
```sql
GRANT 사용자등급 TO 사용자_ID_리스트 [IDENTIFIED BY 암호];
REVOKE 사용자등급 FROM 사용자_ID_리스트;
```
### 테이블 및 속성에 대한 권한 부여 및 취소
```sql
GRANT 권한_리스트 ON 개체 TO 사용자 [WITH GRANT OPTION];
REVOKE [GRANT OPTION FOR] 권한_리스트 ON 개체 FROM 사용자 [CASCADE];
```
- 권한 종류 : ALL, SELECT, INSERT, DELETE, UPDATE 등
- WITH GRANT OPTION : 부여 받은 권한을 다른 사용자에게 다시 부여할 수 있는 권한을 부여
- GRANT OPTION FOR : 다른 사용자에게 권한을 부여할 수 있는 권한을 취소
- CASCADE : 권한 취소 시 권한을 부여받았던 사용자가 다른 사용자에게 부여한 권한도 연쇄적으로 취소
## COMMIT
- 트랜잭션 처리가 정상적으로 완료된 후 트랜잭션이 수행한 내용을 데이터베이스에 반영하는 명령어
- COMMIT 명령을 실행하지 않아도 DML문이 성공적으로 완료되면 자동으로 COMMIT 되고 DML이 실패하면 자동으로 ROLLBACK이 되도록 Auto Commit 기능 설정 가능
## ROLLBACK
- 변경되었으나 아직 COMMIT되지 않은 모든 내용들을 취소하고 데이터베이스를 이전 상태로 되돌리는 명령어
- 트랜잭션 전체가 성공적으로 끝나지 못하면 일부 변경된 내용만 데이터베이스에 반영되는 비일관성(Inconsistency) 상태가 될 수 있기 때문에 일부분만 완료된 트랜잭션은 롤백(Rollback) 되어야 함
## SAVEPOINT
- 트랜잭션 내에 ROLLBACK 할 위치인 저장점을 지정하는 명령어
- 저장점을 지정할 때는 이름을 부여
- ROLLBACK 할 때 지정된 저장점까지의 트랜잭션 처리 내용이 모두 취소됨
# Section 104 SQL - DML
## DML (Data Manipulation Language, 데이터 조작어)
- 데이터베이스 사용자가 저장된 데이터를 실질적으로 관리하는데 사용되는 언어
- 데이터베이스 사용자와 데이터베이스 관리 시스템 간의 인터페이스 제공
### DML 유형
1. SELECT : 테이블에서 튜플을 검색
2. INSERT : 테이블에 새로운 튜플 삽입
3. DELETE : 테이블에서 튜플 삭제
4. UPDATE : 테이블에서 튜플 내용 갱신
## 삽입문 (INSERT INTO ~)
- 기본 테이블에 새로운 튜플을 삽입할 때 사용
### 일반 형식
```sql
INSERT INTO 테이블명([속성명1, 속성명2, ...])
	VALUES (데이터1, 데이터2, ...);
```
- 대응하는 속성과 데이터는 개수와 데이터 유형이 일치해야 함
- 기본 테이블의 모든 속성을 사용할 때는 속성명 생략 가능
- SELECT문을 사용해 다른 테이블의 검색 결과 삽입 가능
## 삭제문 (DELETE FROM ~)
- 기본 테이블에 있는 튜플들 중에서 특정 튜플(행)을 삭제할 때 사용
### 일반 형식
```sql
DELETE
	FROM 테이블명
	[WHERE 조건];
```
- 모든 레코드를 삭제할 때는 WHERE절 생략
- 모든 레코드를 삭제하더라도 테이블 구조는 남아 있기 때문에 디스크에서 테이블을 완전히 제거하는 DROP과는 다름
## 갱신문 (UPDATE ~ SET ~)
- 기본 테이블에 있는 튜플들 중에서 특정 튜플의 내용을 변경할 때 사용
### 일반 형식
```sql
UPDATE 테이블명
	SET 속성명 = 데이터[, 속성명=데이터, ...]
	[WHERE 조건];
```
# Section 105 DML - SELECT - 1
## 일반 형식
```sql
SELECT [PREDICATE] [테이블명.]속성명 [AS 별칭][, [테이블명.]속성명, ...] [, 그룹함수(속성명) [AS 별칭]] [, Windows함수 OVER (PARTITION BY 속성명1, 속성명2, ... ORDER BY 속성명3, 속성명4, ...)]
	FROM 테이블명[, 테이블명, ...]
	[WHERE 조건]
	[GROUP BY 속성명, 속성명, ...]
	[HAVING 조건]
	[ORDER BY 속성명 [ASC | DESC]];
```
- SELECT절
	- PREDICATE : 검색할 튜플 수를 제한하는 명령어를 기술
		- DISTINCT : 중복된 튜플이 있으면 그 중 첫 번째 한 개만 표시
	- 속성명 : 검색하여 불러올 속성(열) 또는 속성을 이용한 수식을 지정
	- AS : 속성이나 연산의 이름을 다른 이름으로 표시하기 위해 사용
- FROM절 : 검색할 데이터가 들어있는 테이블 이름을 기술
- WHERE절 : 검색할 조건을 기술
- ORDER BY절 : 데이터를 정렬하여 검색할 때 사용
	- 속성명 : 정렬의 기준이 되는 속성명을 기술
	- [ASC | DESC] : 정렬 방식으로, ASC는 오름차순, DESC는 내림차순으로 생략할 경우 오름차순으로 지정
## 조건 연산자
1. 비교 연산자
	- = : 같다
	- <> : 같지 않다
	- > : 크다
	- < : 작다
	- ≥ : 크거나 작다
	- ≤ : 작거나 같다
2. 논리 연산자
	- NOT, AND, OR
3. LIKE 연산자
	- 대표 문자를 이용해 지정된 속성의 값이 문자 패턴과 일치하는 튜플을 검색하기 위해 사용
	- % : 모든 문자를 대표
	- _ : 문자 하나를 대표
	-  # : 숫자 하나를 대표
## 기본 검색
- SELECT 절에 원하는 속성을 지정하여 검색
### 예시
- <사원> 테이블에서 “주소”만 검색하되 같은 “주소”는 한 번만 출력하시오
```sql
SELECT DISTINCT 주소
	FROM 사원;
```
## 조건 지정 검색
- WHERE 절에서 조건을 지정하여 조건에 만족하는 튜플만 검색
### 예시
- <사원> 테이블에서 “기획”부의 모든 튜플을 검색하시오.
```sql
SELECT *
	FROM 사원
	WHERE 부서 = '기획';
```
## 정렬 검색
- ORDER BY 절에 특정 속성을 지정하여 지정된 속서응로 자료를 정렬하여 검색
### 예시
- <사원> 테이블에서 “주소”를 기준으로 내림차순 정렬시켜 상위 2개 튜플만 검색하시오
```sql
SELECT TOP 2 *
	FROM 사원
	ORDER BY 주소 DESC;
```
## 하위 질의
- 조건절에 주어진 질의를 먼저 수행하여 그 검색 결과를 조건절의 피연산자로 사용
### 예시
- 취미 활동을 하지 않는 사원들을 검색하시오
```sql
SELECT *
	FROM 사원
	WHERE 이름 NOT IN (SELECT 이름 FROM 여가활동);
```
## 복수 테이블 검색
- 여러 테이블을 대상으로 검색을 수행
### 예시
- “경력”이 10년 이상인 사원의 “이름”, “부서”, “취미”, “경력”을 검색하시오.
```sql
SELECT 사원.이름, 사원.부서, 여가활동.취미, 여가활동.경력
	FROM 사원, 여가활동
	WHERE 여가활동.경력 >= 10 AND 사원.이름 = 여가활동.이름;
```
# Section 106 DML - SELECT - 2
## 일반 형식
```sql
SELECT [PREDICATE] [테이블명.]속성명 [AS 별칭][, [테이블명.]속성명, ...][, 그룹함수(속성명) [AS 별칭]][, WINDOW함수 OVER (PARTITION BY 속성명1, 속성명2, ... ORDER BY 속성명3, 속성명4, ...) [AS 별칭]]
	FROM 테이블명[, 테이블명, ...]
	[WHERE 조건]
	[GROUP BY 속성명, 속성명, ...]
	[HAVING 조건]
	[ORDER BY 속성명 [ASC | DESC]];
```
- 그룹함수 : GROUP BY절에 지정된 그룹별로 속성의 값을 집계할 함수 기술
- WINDOW 함수 : GROUP BY절을 이용하지 않고 속성의 값을 집계할 함수 기술
	- PARTITION BY : WINDOW 함수의 적용 범위가 될 속성 지정
	- ORDER BY : PARTITION 안에서 정렬 기준으로 사용할 속성 지정
- GROUP BY절
	- 특정 속성을 기준으로 그룹화하여 검색할 때 사용
	- 일반적으로 GROUP BY절은 그룹 함수와 함께 사용
- HAVING절 : GROUP BY와 함께 사용되며, 그룹에 대한 조건 지정
## 그룹 함수
- GROUP BY절에 지정된 그룹별로 속성의 값을 집계할 때 사용
### 그룹 함수 종류
1. COUNT(속성명) : 그룹별 튜플 수를 구하는 함수
2. SUM(속성명) : 그룹별 합계를 구하는 함수
3. AVG(속성명) : 그룹별 평균을 구하는 함수
4. MAX(속성명) : 그룹별 최대값을 구하는 함수
5. MIN(속성명) : 그룹별 최소값을 구하는 함수
6. STDDEV(속성명) : 그룹별 표준편차를 구하는 함수
7. VARIANCE(속성명) : 그룹별 분산을 구하는 함수
8. ROLLUP(속성명, 속성명, …)
	- 인수로 주어진 속성을 대상으로 그룹별 소계를 구하는 함수
	- 속성의 개수가 n개이면, n+1 레벨까지, 하위 레벨에서 상위 레벨 순으로 데이터가 집계됨
9. CUBE(속성명, 속성명, …)
	- ROLLUP과 유사한 형태지만 CUBE는 인수로 주어진 속성을 대상으로 모든 조합의 그룹별 소계 구함
	- 속성의 개수가 n개이면, $2^n$ 레벨까지, 상위 레벨에서 하위 레벨 순으로 데이터가 집계됨
## WINDOW 함수
- GROUP BY절을 이용하지 않고 함수의 인수로 지정한 속성의 값을 집계
- 윈도우(WINDOW) : 함수의 인수로 지정한 속성이 집계할 범위
- WINDOW 함수
	- ROW_NUMBER() : 윈도우별로 각 레코드에 대한 일련번호 반환
	- RANK() : 윈도우별로 순위를 반환하며, 공동 순위를 반영
	- DENSE_RANK() : 윈도우별로 순위를 반환하며, 공동 순위를 무시하고 순위를 부여
## WINDOW 함수 이용 검색
- GROUP BY절을 이용하지 않고 함수의 인수로 지정한 속성을 범위로 하여 속성의 값을 집계
### 예시
- <상여금> 테이블에서 “상여내역”별로 “상여금”에 대한 일련 번호를 구하시오. (단 순서는 내림차순이며 속성명은 “NO”로 할 것)
```SQL
SELECT 상여내역, 상여금
	ROW_NUMBER() OVER (PARTITION BY 상여내역 ORDER BY 상여금 DESC) AS NO
	FROM 상여금;
```
## 그룹 지정 검색
- GROUP BY절에 지정한 속성을 기준으로 자료를 그룹화하여 검색
### 예시
- <상여금> 테이블에서 “부서”별 “상여금”의 평균을 구하시오
```SQL
SELECT 부서, AVG(상여금) AS 평균
	FROM 상여금
	GROUP BY 부서;
```
## 집합 연산자를 이용한 통합 질의
- 집합 연산자를 사용하여 2개 이상의 테이블의 데이터를 하나로 통합
### 표기 형식
```SQL
SELECT 속성명1, 속성명2, ...
	FROM 테이블명
UNION | UNION ALL | INTERSECT | EXCEPT
SELECT 속성명1, 속성명2, ...
	FROM 테이블명
[ORDER BY 속성명 [ASC | DESC]];
```
- 두 개의 SELECT문에 기술한 속성들은 개수와 데이터 유형이 서로 동일해야 함
### 집합 연산자의 종류 (통합 질의의 종류)
1. UNION (합집합)
	- 두 SELECT문의 조회 결과를 통합하여 모두 출력
	- 중복된 행은 한 번만 출력
2. UNION ALL (합집합)
	- 두 SELECT문의 조회 결과를 통합하여 모두 출력
	- 중복된 행도 그대로 출력
3. INTERSECT (교집합)
	- 두 SELECT문의 조회 결과 중 공통된 행만 출력
4. EXCEPT (차집합)
	- 첫 번째 SELECT문의 조회 결과에서 두 번째 SELECT문의 조회 결과를 제외한 행을 출력
### 예시
- <사원> 테이블과 <직원> 테이블을 통합하는 질의문을 작성하시오. (단, 같은 레코드가 중복되어 나오지 않게 하시오.)
```SQL
SELECT *
	FROM 사원
UNION
SELECT *
	FROM 직원;
```
# Section 107 DML - JOIN
## JOIN
- 2개의 릴레이션에서 연관된 튜플들을 결합하여, 하나의 새로운 릴레이션을 반환
- 일반적으로 FROM절에 기술하지만, 릴레이션이 사용되는 곳 어디에나 사용 가능
### JOIN 구분
1. INNER JOIN : THETA JOIN, EQUI JOIN, NATURAL JOIN, NON-EQUI JOIN
2. OUTER JOIN : LEFT OUTER JOIN, RIGHT OUTER JOIN, FULL OUTER JOIN
## INNER JOIN
- 일반적으로 EQUI JOIN과 NON-EQUI JOIN으로 구분
- 조건이 없는 INNER JOIN을 수행할 경우 CROSS JOIN과 동일한 결과 획득 가능
### EQUI JOIN
- THETA JOIN(세타 조인) : JOIN에 참여하는 두 릴레이션의 속성 값을 비교하여 조건을 만족하는 튜플만 반환하는 조언
	- 조인에 사용되는 조건 : =, !=, <, ≤, >, ≥
- EQUI JOIN(동등 조인) : 조인에 사용되는 조건 중 =(EQUAL) 비교에 의해 같은 값을 가지는 행을 연결하여 결과를 생성하는 방법
- NATURAL JOIN : JOIN 조건이 “=”일 때 동일한 속성이 두 번 나타나게 되는데, 이 중 중복된 속성을 제거하여 같은 속성을 한 번만 표기하는 방법
- JOIN 속성 : EQUI JOIN에서 연결 고리가 되는 공통 속성
#### WHERE절을 이용한 EQUI JOIN의 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1, 테이블명2, ...
	WHERE 테이블명1.속성명 = 테이블명2.속성명
```
#### NATURAL JOIN절을 이용한 EQUI JOIN의 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1 NATURAL JOIN 테이블명2;
```
#### JOIN ~ USING절을 이용한 EQUI JOIN의 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1 JOIN 테이블명2 USING(속성명);
```
### NON-EQUI JOIN
- JOIN 조건에 “=” 조건이 아닌 나머지 비교 연산자, 즉 >, <, <>, ≤, ≥ 연산자를 사용하는 JOIN 방법
#### 표기 형식
```SQL
SELECT [테이블명1.]속섬명, [테이블명2.]속성명, ...
	FROM 테이블명1, 테이블명2, ...
	WHERE (NON-EQUI JOIN 조건);
```
## OUTER JOIN
- 릴레이션에서 JOIN 조건에 만족하지 않는 튜플도 결과로 출력하기 위한 JOIN 방법
### LEFT OUTER JOIN
- INNER JOIN의 결과를 구한 후, 우측 항 릴레이션의 어떤 튜플과도 맞지 않는 좌측 항의 릴레이션에 있는 튜플들에 NULL 값을 붙여서 INNER JOIN의 결과에 추가
#### 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1 LEFT OUTER JOIN 테이블명2
	ON 테이블명1.속성명 = 테이블명2.속성명;

SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1, 테이블명2
	WHERE 테이블명1.속성명 = 테이블명2.속성명(+);
```
### RIGHT OUTER JOIN
- INNER JOIN의 결과를 구한 후, 좌측 항 릴레이션의 어떤 튜플과도 맞지 않는 우측 항의 릴레이션에 있는 튜플들에 NULL 값을 붙여서 INNER JOIN의 결과에 추가
#### 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1 RIGHT OUTER JOIN 테이블명2
	ON 테이블명1.속성명 = 테이블명2.속성명;

SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1, 테이블명2
	WHERE 테이블명1.속성명(+) = 테이블명2.속성명;
```
### FULL OUTER JOIN
- LEFT OUTER JOIN과 RIGHT OUTER JOIN을 합쳐 놓은 것
- INNER JOIN의 결과를 구한 후, 좌측 항의 릴레이션의 튜플들에 대해 우측 항의 릴레이션의 어떤 튜플과도 맞지 않는 튜플들에 NULL 값을 붙여서 INNER JOIN의 결과에 추가
- 그리고 유사하게 우측 항의 릴레이션 튜플들에 대해 좌측 항의 릴레이션의 어떤 튜플과도 맞지 않는 튜플들에 NULL 값을 붙여서 INNER JOIN의 결과에 추가
#### 표기 형식
```SQL
SELECT [테이블명1.]속성명, [테이블명2.]속성명, ...
	FROM 테이블명1 FULL OUTER JOIN 테이블명2
	ON 테이블명1.속성명 = 테이블명2.속성명;
```
# Section 108 트리거(Trigger)
## 트리거 (Trigger)
- 데이터베이스 시스템에서 데이터의 삽입(Insert), 갱신(Update), 삭제(Delete) 등의 이벤트(Event)가 발생할 때 관련 작업이 자동으로 수행되게 하는 절차형 SQL
- 데이터베이스에 저장되며, 데이터 변경 및 무결성 유지, 로그 메시지 출력 등의 목적으로 사용
- 트리거의 구문에는 DCL(데이터 제어어)을 사용할 수 없으며, DCL이 포함된 프로시저나 함수를 호출하는 경우에 오류 발생
## 트리거의 구성도
![](https://velog.velcdn.com/images/kik328288/post/eebb91eb-114c-4c93-a608-8cf118aa1a5b/image.png)

- DECLARE : 트리거의 명칭, 변수 및 상수, 데이터 타입을 정의하는 선언부
- EVENT : 트리거가 실행되는 조건을 명시
- BEGIN / END : 트리거의 시작과 종료를 의미
- CONTROL : 조건문 또는 반복문이 삽입되어 순차적으로 처리
- SQL : DML 문이 삽입되어 데이터 관리를 위한 조회, 추가, 수정, 삭제 작업을 수행
- EXCEPTION : BEGIN ~ END 안의 구문 실행 시 예외가 발생하면 이를 처리하는 방법을 정의
## 트리거의 생성
- 트리거를 생성하기 위해서는 CREATE TRIGGER 명령어 사용
### 표기 형식
```sql
CREATE [OR REPLACE] TRIGGER 트리거명 [동작시기 옵션][동작 옵션] ON 테이블명
	REFERENCING [NEW | OLD] AS 테이블명
	FOR EACH ROW
	[WHEN 조건식]
BEGIN
	트리거 BODY;
END;
```
- ON REPLACE
	- 선택적인(Optional) 예약어
	- 해당 예약어를 사용하면 동일한 트리거 이름이 이미 존재하는 경우, 기존의 트리거 대체 가능
- 동작시기 옵션 : 트리거가 실행될 때를 지정
	- AFTER : 테이블이 변경된 후에 트리거가 실행됨
	- BEFORE : 테이블이 변경되기 전에 트리거가 실행됨
- 동작 옵션 : 트리거가 실행되게 할 작업의 종류 지정
	- INSERT : 테이블에 새로운 튜플을 삽입할 때 트리거가 실행
	- DELETE : 테이블의 튜플을 삭제할 때 트리거가 실행
	- UPDATE : 테이블의 튜플을 수정할 때 트리거가 실행
- NEW | OLD : 트리거가 적용될 테이블의 별칭을 지정
	- NEW : 추가되거나 수정에 참여할 튜플들의 집합(테이블)
	- OLD : 수정되거나 삭제 전 대상이 되는 튜플들의 집합(테이블)
- FOR EACH ROW : 각 튜플마다 트리거를 적용한다는 의미
- WHEN 조건식
	- 선택적인(Optional) 예약어
	- 트리거를 적용할 튜플의 조건을 지정
- 트리거 BODY
	- 트리거의 본문 코드를 입력하는 부분
	- BEGIN으로 시작해서 END로 끝나는데, 적어도 하나 이상의 SQL문이 있어야함
	- 그렇지 않을 경우 오류가 발생
## 트리거의 제거
- 트리거를 제거하기 위해서는 DROP TRIGGER 명령어 사용
### 표기 형식
```SQL
DROP TRIGGER 트리거명;
```

