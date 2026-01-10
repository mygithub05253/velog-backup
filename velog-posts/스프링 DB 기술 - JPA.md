# 스프링 DB 기술 - JPA

**Published:** Fri, 09 Jan 2026 08:18:55 GMT
**Link:** https://velog.io/@kik328288/%EC%8A%A4%ED%94%84%EB%A7%81-DB-%EA%B8%B0%EC%88%A0-JPA

---

<h2 id="14-jpa-java-persistence-api">14. JPA (Java Persistence API)</h2>
<hr />
<p>SQL 중심적인 개발에서 <strong>객체 중심의 개발</strong>로 패러다임을 전환하는 기술이다.</p>
<h3 id="141-특징">14.1 특징</h3>
<hr />
<ul>
<li>기본적인 SQL(CRUD)을 JPA가 직접 만들어서 실행한다.</li>
<li>개발 생산성을 크게 높여준다.</li>
<li><strong><code>EntityManager</code>:</strong> JPA의 모든 동작은 엔티티 매니저를 통해 이루어진다.</li>
</ul>
<h3 id="142-설정-및-사용">14.2 설정 및 사용</h3>
<hr />
<ul>
<li><code>build.gradle</code>: <code>spring-boot-starter-data-jpa</code> 추가.</li>
</ul>
<pre><code class="language-java">dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
    implementation 'org.springframework.boot:spring-boot-starter-webmvc'
    // implementation 'org.springframework.boot:spring-boot-starter-jdbc'
    implementation &quot;org.springframework.boot:spring-boot-starter-data-jpa&quot;
    runtimeOnly 'com.h2database:h2'
    testImplementation 'org.springframework.boot:spring-boot-starter-thymeleaf-test'
    testImplementation 'org.springframework.boot:spring-boot-starter-webmvc-test'
    testImplementation(&quot;org.springframework.boot:spring-boot-starter-test&quot;) {
        exclude group: &quot;org.junit.vintage&quot;, module: &quot;junit-vintage-engine&quot;
    }
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}</code></pre>
<ul>
<li><code>application.properties</code>:<ul>
<li><code>spring.jpa.show-sql=true</code>: 실행되는 SQL을 로그로 확인.</li>
<li><code>spring.jpa.hibernate.ddl-auto=none</code>: 테이블 자동 생성 기능 끄기 (기존 테이블 사용 시).</li>
</ul>
</li>
</ul>
<pre><code class="language-java">spring.application.name=hello-spring
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa

spring jpa.show-sql = true
spring.jpa.hibernate.ddl-auto=none</code></pre>
<ul>
<li><strong><code>@Entity</code> 매핑:</strong> 도메인 객체에 <code>@Entity</code>를 붙여서 DB 테이블과 매핑한다.</li>
</ul>
<pre><code class="language-java">package hello.hello_spring.domain;

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
}</code></pre>
<ul>
<li><strong><code>@Transactional</code>:</strong> JPA를 통한 데이터 변경은 반드시 트랜잭션 안에서 실행되어야 하므로 서비스 계층에 추가한다.</li>
</ul>
<pre><code class="language-java">// JPA 저장 예제 (SQL을 작성하지 않음)
public Member save(Member member) {
    em.persist(member); // 영구 저장
    return member;
}</code></pre>
<h3 id="143-리포지토리-전체-코드-jpamemberrepository">14.3 리포지토리 전체 코드 (<code>JpaMemberRepository</code>)</h3>
<hr />
<pre><code class="language-java">package hello.hello_spring.repository;

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

    public Optional&lt;Member&gt; findById(Long id) {
        Member member = em.find(Member.class, id);
        return Optional.ofNullable(member);
    }

    public List&lt;Member&gt; findAll() {
        return em.createQuery(&quot;select m from Member m&quot;, Member.class).getResultList();
    }

    public Optional&lt;Member&gt; findByName(String name) {
        List&lt;Member&gt; result = em.createQuery(&quot;select m from Member m where m.name = :name&quot;, Member.class)
                .setParameter(&quot;name&quot;, name)
                .getResultList();
        return result.stream().findAny();
    }
}</code></pre>
<h3 id="144-스프링-설정-변경-springconfig">14.4 스프링 설정 변경 (<code>SpringConfig</code>)</h3>
<hr />
<pre><code class="language-java">package hello.hello_spring;

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
}</code></pre>
<h2 id="15-스프링-데이터-jpa">15. 스프링 데이터 JPA</h2>
<hr />
<p>JPA를 더 편리하게 사용할 수 있도록 감싼 프레임워크이다. <strong>리포지토리 구현 클래스 없이 인터페이스만으로 개발</strong>을 완료할 수 있다.</p>
<h3 id="151-특징">15.1 특징</h3>
<hr />
<ul>
<li>개발자가 인터페이스(<code>SpringDataJpaMemberRepository</code>)만 만들고 <code>JpaRepository</code>를 상속받으면, 스프링 데이터 JPA가 <strong>구현체를 자동으로 생성해서 스프링 빈으로 등록</strong>해준다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/4440c9d9-43d6-4049-afaa-dc98c1a1bf94/image.png" /></p>
<ul>
<li><strong>설명:</strong> <code>JpaRepository</code>는 <code>PagingAndSortingRepository</code>, <code>CrudRepository</code>를 상속받고 있어 기본적인 CRUD, 페이징, 정렬 기능을 모두 제공한다 .</li>
</ul>
<h3 id="152-주요-기능">15.2 주요 기능</h3>
<hr />
<ul>
<li><strong>기본 CRUD 제공:</strong> <code>save()</code>, <code>findAll()</code>, <code>findById()</code> 등 공통 메서드 제공 .</li>
<li><strong>메서드 이름으로 쿼리 생성:</strong><ul>
<li>예: <code>findByName(String name)</code>이라고 메서드 이름만 지어주면, <code>select m from Member m where m.name = :name</code> JPQL을 알아서 짠다.</li>
</ul>
</li>
</ul>
<h3 id="153-사용-예시-코드">15.3 사용 예시 코드</h3>
<hr />
<ul>
<li>스프링 데이터 JPA 회원 리포지토리 코드 (<code>SpringDataJpaMemberRepository</code>)</li>
</ul>
<pre><code class="language-java">package hello.hello_spring.repository;

import hello.hello_spring.domain.Member;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SpringDataJpaMemberRepository extends JpaRepository&lt;Member, Long&gt;, MemberRepository {
    Optional&lt;Member&gt; findByName(String name);
}</code></pre>
<ul>
<li>스프링 설정 변경 (<code>SpringConfig</code>)</li>
</ul>
<pre><code class="language-java">package hello.hello_spring;

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
}</code></pre>
<h3 id="154-실무-조합-권장">15.4 실무 조합 (권장)</h3>
<hr />
<p>실무에서는 <strong>JPA + 스프링 데이터 JPA</strong>를 기본으로 사용하고, 복잡한 동적 쿼리는 <strong>Querydsl</strong>이라는 라이브러리를 사용하여 해결한다.</p>
<ul>
<li>기술 선택 가이드</li>
</ul>
<table>
<thead>
<tr>
<th><strong>기술</strong></th>
<th><strong>특징</strong></th>
<th><strong>장점</strong></th>
<th><strong>단점</strong></th>
</tr>
</thead>
<tbody><tr>
<td><strong>순수 JDBC</strong></td>
<td>날것의 JDBC API</td>
<td>가장 기초, 원리 이해용</td>
<td>코드가 너무 길고 복잡함</td>
</tr>
<tr>
<td><strong>JdbcTemplate</strong></td>
<td>JDBC의 래퍼(Wrapper)</td>
<td>반복 코드 제거, SQL 직접 제어</td>
<td>여전히 SQL을 직접 짜야 함</td>
</tr>
<tr>
<td><strong>JPA</strong></td>
<td>ORM 기술 표준</td>
<td>SQL 자동 생성, 객체 중심 설계</td>
<td>학습 곡선이 높음</td>
</tr>
<tr>
<td><strong>스프링 데이터 JPA</strong></td>
<td>JPA의 추상화 계층</td>
<td>인터페이스만으로 개발 가능, 생산성 극대화</td>
<td>JPA를 모르면 문제 해결 어려움</td>
</tr>
</tbody></table>