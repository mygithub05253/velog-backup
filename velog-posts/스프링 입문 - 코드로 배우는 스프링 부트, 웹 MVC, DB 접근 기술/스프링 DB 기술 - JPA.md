# 스프링 DB 기술 - JPA

**Published:** 2026-01-09T08:18:55.035Z
**Link:** https://velog.io/@kik328288/스프링-DB-기술-JPA

---

## 14. JPA (Java Persistence API)

---

SQL 중심적인 개발에서 **객체 중심의 개발**로 패러다임을 전환하는 기술이다.

### 14.1 특징

---

- 기본적인 SQL(CRUD)을 JPA가 직접 만들어서 실행한다.
- 개발 생산성을 크게 높여준다.
- **`EntityManager`:** JPA의 모든 동작은 엔티티 매니저를 통해 이루어진다.

### 14.2 설정 및 사용

---

- `build.gradle`: `spring-boot-starter-data-jpa` 추가.

```java
dependencies {
	implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
	implementation 'org.springframework.boot:spring-boot-starter-webmvc'
	// implementation 'org.springframework.boot:spring-boot-starter-jdbc'
	implementation "org.springframework.boot:spring-boot-starter-data-jpa"
	runtimeOnly 'com.h2database:h2'
	testImplementation 'org.springframework.boot:spring-boot-starter-thymeleaf-test'
	testImplementation 'org.springframework.boot:spring-boot-starter-webmvc-test'
	testImplementation("org.springframework.boot:spring-boot-starter-test") {
		exclude group: "org.junit.vintage", module: "junit-vintage-engine"
	}
	testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
```

- `application.properties`:
    - `spring.jpa.show-sql=true`: 실행되는 SQL을 로그로 확인.
    - `spring.jpa.hibernate.ddl-auto=none`: 테이블 자동 생성 기능 끄기 (기존 테이블 사용 시).

```java
spring.application.name=hello-spring
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa

spring jpa.show-sql = true
spring.jpa.hibernate.ddl-auto=none
```

- **`@Entity` 매핑:** 도메인 객체에 `@Entity`를 붙여서 DB 테이블과 매핑한다.

```java
package hello.hello_spring.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Member {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

- **`@Transactional`:** JPA를 통한 데이터 변경은 반드시 트랜잭션 안에서 실행되어야 하므로 서비스 계층에 추가한다.

```java
// JPA 저장 예제 (SQL을 작성하지 않음)
public Member save(Member member) {
    em.persist(member); // 영구 저장
    return member;
}
```

### 14.3 리포지토리 전체 코드 (`JpaMemberRepository`)

---

```java
package hello.hello_spring.repository;

import hello.hello_spring.domain.Member;
import jakarta.persistence.EntityManager;

import java.util.List;
import java.util.Optional;

public class JpaMemberRepository implements MemberRepository {
    private final EntityManager em;

    public JpaMemberRepository(EntityManager em) {
        this.em = em;
    }

    public Member save(Member member) {
        em.persist(member);
        return member;
    }

    public Optional<Member> findById(Long id) {
        Member member = em.find(Member.class, id);
        return Optional.ofNullable(member);
    }

    public List<Member> findAll() {
        return em.createQuery("select m from Member m", Member.class).getResultList();
    }

    public Optional<Member> findByName(String name) {
        List<Member> result = em.createQuery("select m from Member m where m.name = :name", Member.class)
                .setParameter("name", name)
                .getResultList();
        return result.stream().findAny();
    }
}
```

### 14.4 스프링 설정 변경 (`SpringConfig`)

---

```java
package hello.hello_spring;

import hello.hello_spring.repository.*;
import hello.hello_spring.service.MemberService;
import jakarta.persistence.EntityManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class SpringConfig {

    private final DataSource dataSource;
    private final EntityManager em;

    public SpringConfig(DataSource dataSource, EntityManager em) {
        this.dataSource = dataSource;
        this.em = em;
    }

    @Bean // 스프링 빈 등록
    public MemberService memberService() {
        // 의존관계 엮어주기 (생성자 주입)
        return new MemberService(memberRepository());
    }

    @Bean
    public MemberRepository memberRepository() {
        // 나중에 DB 리포지토리로 변경 시 이 부분만 수정하면 됨
        // return new MemoryMemberRepository();

        // return new JdbcMemberRepository(dataSource);
        // return new JdbcTemplateMemberRepository(dataSource);

        return new JpaMemberRepository(em);
    }
}
```

## 15. 스프링 데이터 JPA

---

JPA를 더 편리하게 사용할 수 있도록 감싼 프레임워크이다. **리포지토리 구현 클래스 없이 인터페이스만으로 개발**을 완료할 수 있다.

### 15.1 특징

---

- 개발자가 인터페이스(`SpringDataJpaMemberRepository`)만 만들고 `JpaRepository`를 상속받으면, 스프링 데이터 JPA가 **구현체를 자동으로 생성해서 스프링 빈으로 등록**해준다.

![](https://velog.velcdn.com/images/kik328288/post/4440c9d9-43d6-4049-afaa-dc98c1a1bf94/image.png)

- **설명:** `JpaRepository`는 `PagingAndSortingRepository`, `CrudRepository`를 상속받고 있어 기본적인 CRUD, 페이징, 정렬 기능을 모두 제공한다 .

### 15.2 주요 기능

---

- **기본 CRUD 제공:** `save()`, `findAll()`, `findById()` 등 공통 메서드 제공 .
- **메서드 이름으로 쿼리 생성:**
    - 예: `findByName(String name)`이라고 메서드 이름만 지어주면, `select m from Member m where m.name = :name` JPQL을 알아서 짠다.

### 15.3 사용 예시 코드

---

- 스프링 데이터 JPA 회원 리포지토리 코드 (`SpringDataJpaMemberRepository`)

```java
package hello.hello_spring.repository;

import hello.hello_spring.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SpringDataJpaMemberRepository extends JpaRepository<Member, Long>, MemberRepository {
    Optional<Member> findByName(String name);
}
```

- 스프링 설정 변경 (`SpringConfig`)

```java
package hello.hello_spring;

import hello.hello_spring.repository.*;
import hello.hello_spring.service.MemberService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SpringConfig {
    private final MemberRepository memberRepository;

    public SpringConfig(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
    
    @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository);
    }
}
```

### 15.4 실무 조합 (권장)

---

실무에서는 **JPA + 스프링 데이터 JPA**를 기본으로 사용하고, 복잡한 동적 쿼리는 **Querydsl**이라는 라이브러리를 사용하여 해결한다.

- 기술 선택 가이드

| **기술** | **특징** | **장점** | **단점** |
| --- | --- | --- | --- |
| **순수 JDBC** | 날것의 JDBC API | 가장 기초, 원리 이해용 | 코드가 너무 길고 복잡함 |
| **JdbcTemplate** | JDBC의 래퍼(Wrapper) | 반복 코드 제거, SQL 직접 제어 | 여전히 SQL을 직접 짜야 함 |
| **JPA** | ORM 기술 표준 | SQL 자동 생성, 객체 중심 설계 | 학습 곡선이 높음 |
| **스프링 데이터 JPA** | JPA의 추상화 계층 | 인터페이스만으로 개발 가능, 생산성 극대화 | JPA를 모르면 문제 해결 어려움 |
