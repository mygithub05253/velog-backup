# 스프링 DB 접근 기술 - 순수 JDBC (Legacy)

**Published:** Fri, 09 Jan 2026 07:30:21 GMT
**Link:** https://velog.io/@kik328288/%EC%8A%A4%ED%94%84%EB%A7%81-DB-%EC%A0%91%EA%B7%BC-%EA%B8%B0%EC%88%A0-%EC%88%9C%EC%88%98-JDBC-Legacy

---

<h2 id="11-순수-jdbc-legacy">11. 순수 JDBC (Legacy)</h2>
<hr />
<p>가장 오래된 방식이다. 20년 전에는 이렇게 개발했으나, 지금은 <strong>&quot;고생스러웠던 역사&quot;</strong>를 알고, 프레임워크가 무엇을 대신해 주는지 이해하는 차원에서 학습한다 .</p>
<h3 id="111-환경-설정">11.1 환경 설정</h3>
<hr />
<ul>
<li><code>build.gradle</code>: <code>spring-boot-starter-jdbc</code>, <code>h2</code> 라이브러리 추가.</li>
</ul>
<pre><code class="language-java">implementation 'org.springframework.boot:spring-boot-starter-jdbc'
runtimeOnly 'com.h2database:h2'</code></pre>
<ul>
<li><code>application.properties</code>: DB 접속 정보 설정 .<ul>
<li><strong>주의:</strong> 스프링 부트 2.4부터 <code>spring.datasource.username=sa</code>를 반드시 추가해야 한다.</li>
</ul>
</li>
</ul>
<pre><code class="language-java">spring.application.name=hello-spring
spring.datasource.url=jdbc:h2:tcp://localhost/~/test
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa</code></pre>
<h3 id="112-특징-및-단점">11.2 특징 및 단점</h3>
<hr />
<ul>
<li><code>DataSource</code>, <code>Connection</code>, <code>PreparedStatement</code>, <code>ResultSet</code> 등 JDBC 표준 인터페이스를 직접 사용한다 .</li>
<li><strong>반복 코드:</strong> 커넥션 연결/해제, 예외 처리(<code>try-catch-finally</code>) 코드가 비즈니스 로직보다 훨씬 길다.</li>
</ul>
<h3 id="113-구현체-교체와-ocp-open-closed-principle">11.3 구현체 교체와 OCP (Open-Closed Principle)</h3>
<hr />
<p>객체 지향 설계의 장점은 <strong>다형성(Polymorphism)</strong>을 활용해 인터페이스의 구현체를 갈아끼울 수 있다는 점이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/02628b69-7c00-4cec-942a-fdd8e1fc0890/image.png" /></p>
<ul>
<li><strong>설명:</strong> <code>MemberService</code>는 <code>MemberRepository</code> 인터페이스만 의존한다. 기존 <code>MemoryMemberRepository</code>를 <code>JdbcMemberRepository</code>로 교체해도 서비스 코드는 변경되지 않는다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/ce0776bf-e0dd-47d2-a73f-3206a206203c/image.png" /></p>
<ul>
<li><strong>설명:</strong> 스프링 설정(<code>SpringConfig</code>)만 변경하면, 스프링 컨테이너가 기존 메모리 저장소 대신 JDBC 저장소를 빈으로 등록하여 의존성을 주입해준다. 이것이 <strong>OCP(확장에는 열려 있고, 변경에는 닫혀 있다)</strong> 원칙을 지키는 방법이다 .</li>
</ul>
<h3 id="114-jdbc-레포지토리-구현">11.4 JDBC 레포지토리 구현</h3>
<hr />
<p>주의사항! 이렇게 JDBC API로 직접 코딩하는 것은 20년 전 이야기이다. 따라서 고대 개발자들이 이렇게 고생하고 살았구나 생각하고, 정신 건강을 위해 참고만 하고 넘어가자.</p>
<ul>
<li>JDBC 회원 레포지토리</li>
</ul>
<pre><code class="language-java">package hello.hello_spring.repository;

import hello.hello_spring.domain.Member;
import org.springframework.jdbc.datasource.DataSourceUtils;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * 순수 JDBC 리포지토리 구현체
 * - 특징: JDBC API를 직접 사용하여 SQL을 작성하고 DB와 통신합니다.
 * - 단점: try-catch-finally 반복 코드가 많고, 연결 관리가 까다롭습니다.
 */
public class JdbcMemberRepository implements MemberRepository {

        // DB 연결 정보를 가지고 있는 DataSource
        // Spring Boot가 설정 정보를 보고 생성해줌
    private final DataSource dataSource;

    public JdbcMemberRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @Override
    public Member save(Member member) {

            // ? : 파라미터바인딩을 위한 자리표시자
            // SQL Injection 방지
        String sql = &quot;insert into member(name) values(?)&quot;;
        Connection conn = null;
        PreparedStatement pstmt = null;

        // 결과(생성한 ID)를 받기 위한 객체
        ResultSet rs = null;

        try {
            conn = getConnection();

            // 두 번째 인자 : DB가 자동으로 생성해준 ID(Key)를 받아오는 옵션
            pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            pstmt.setString(1, member.getName());

            // 실제 쿼리 실행 (executeUpdate : 데이터 변경)
            pstmt.executeUpdate();

            // 생성된 키(ID) 꺼내는 작업
            rs = pstmt.getGeneratedKeys();

            if (rs.next()) {
                member.setId(rs.getLong(1));
            } else {
                throw new SQLException(&quot;id 조회 실패&quot;);
            }
            return member;
        } catch (Exception e) {
            throw new IllegalStateException(e);
        } finally {
                // 사용한 자원 해제 
                // (역순으로 닫아야 함: ResultSet -&gt; Statement -&gt; Connection)
            close(conn, pstmt, rs);
        }
    }

    @Override
    public Optional&lt;Member&gt; findById(Long id) {
        String sql = &quot;select * from member where id = ?&quot;;
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setLong(1, id);

            // 조회는 executeQuery() 사용
            // 결과를 ResultSet으로 반환
            rs = pstmt.executeQuery();
            if (rs.next()) {
                Member member = new Member();
                member.setId(rs.getLong(&quot;id&quot;));
                member.setName(rs.getString(&quot;name&quot;));
                return Optional.of(member);
            } else {
                return Optional.empty();
            }
        } catch (Exception e) {
            throw new IllegalStateException(e);
        } finally {
            close(conn, pstmt, rs);
        }
    }

    @Override
    public List&lt;Member&gt; findAll() {
        String sql = &quot;select * from member&quot;;
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(sql);
            rs = pstmt.executeQuery();
            List&lt;Member&gt; members = new ArrayList&lt;&gt;();

            while (rs.next()) {
                Member member = new Member();
                member.setId(rs.getLong(&quot;id&quot;));
                member.setName(rs.getString(&quot;name&quot;));
                members.add(member);
            }

            return members;
        } catch (Exception e) {
            throw new IllegalStateException(e);
        } finally {
            close(conn, pstmt, rs);
        }
    }

    @Override
    public Optional&lt;Member&gt; findByName(String name) {
        String sql = &quot;select * from member where name = ?&quot;;
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        try {
            conn = getConnection();
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, name);
            rs = pstmt.executeQuery();

            if (rs.next()) {
                Member member = new Member();
                member.setId(rs.getLong(&quot;id&quot;));
                member.setName(rs.getString(&quot;name&quot;));
                return Optional.of(member);
            }
            return Optional.empty();
        } catch (Exception e) {
            throw new IllegalStateException(e);
        } finally {
            close(conn, pstmt, rs);
        }
    }

        // [중요] 스프링 프레임워크를 쓸 때는 DataSourceUtils를 통해 커넥션을 얻어야 합니다.
    // 이를 통해 트랜잭션이 걸려있을 때 같은 커넥션을 유지 가능
    private Connection getConnection() {
        return DataSourceUtils.getConnection(dataSource);
    }

        // 자원 해제 메서드
    private void close(Connection conn, PreparedStatement pstmt, ResultSet rs) {
        try {
            if (rs != null) {
                rs.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        try {
            if (pstmt != null) {
                pstmt.close();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        try {
            if (conn != null) {
                close(conn);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

        // [중요] 커낵션을 닫을 때도 DataSourceUtils를 통해야 합니다.
        // 이를 통해 트랜잭션 중이면 닫지 않고 유지하고, 아닐 경우 닫아주는 로직을 스프링이 처리하기 때문입니다.
    private void close(Connection conn) throws SQLException {
        DataSourceUtils.releaseConnection(conn, dataSource);
    }
}</code></pre>
<ul>
<li>스프링 설정 변경</li>
</ul>
<pre><code class="language-java">package hello.hellospring;

import hello.hellospring.repository.JdbcMemberRepository;
import hello.hellospring.repository.JdbcTemplateMemberRepository;
import hello.hellospring.repository.MemberRepository;
import hello.hellospring.repository.MemoryMemberRepository;
import hello.hellospring.service.MemberService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import javax.sql.DataSource;

@Configuration
public class SpringConfig {
    private final DataSource dataSource;

    public SpringConfig(DataSource dataSource) {
        this.dataSource = dataSource;
  }

  @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository());
  }

  @Bean
    public MemberRepository memberRepository() {
        // return new MemoryMemberRepository();
        return new JdbcMemberRepository(dataSource); 
    }
}</code></pre>
<p>⇒ DataSource는 데이터베이스 커넥션을 획득할 때 사용하는 객체이다.</p>
<p>⇒ 스프링 부트는 데이터베이스 커넥션 정보를 바탕으로 DataSource를 생성하고 스프링 빈으로 만들어주기 때문에 DI를 받을 수 있다.</p>
<h2 id="12-스프링-통합-테스트">12. 스프링 통합 테스트</h2>
<hr />
<p>기존의 단위 테스트와 달리, <strong>스프링 컨테이너와 DB까지 실제로 연결</strong>해서 진행하는 테스트이다.</p>
<h3 id="121-주요-애노테이션">12.1 주요 애노테이션</h3>
<hr />
<ul>
<li><strong><code>@SpringBootTest</code>:</strong> 스프링 컨테이너를 구동하여 테스트를 함께 실행한다.</li>
<li><strong><code>@Transactional</code> (핵심!):</strong><ul>
<li>테스트 시작 전에 트랜잭션을 시작하고, <strong>테스트가 끝나면 항상 롤백(Rollback)</strong>한다 .</li>
<li>덕분에 DB에 데이터가 남지 않아 다음 테스트에 영향을 주지 않고 반복 테스트가 가능하다.</li>
</ul>
</li>
</ul>
<h3 id="122-테스트-코드">12.2 테스트 코드</h3>
<hr />
<pre><code class="language-java">package hello.hello_spring.service;

import hello.hello_spring.domain.Member;
import hello.hello_spring.repository.MemberRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest
@Transactional
class MemberServiceIntegrationTest {

    @Autowired
    MemberService memberService;

    @Autowired
    MemberRepository memberRepository;

    @Test
    public void 회원가입() throws Exception {
        //Given
        Member member = new Member();
        member.setName(&quot;hello&quot;);

        //When
        Long saveId = memberService.join(member);

        //Then
        Member findMember = memberRepository.findById(saveId).get();
        assertEquals(member.getName(), findMember.getName());
    }

    @Test
    public void 중복_회원_예외() throws Exception {
        //Given
        Member member1 = new Member();
        member1.setName(&quot;spring&quot;);
        Member member2 = new Member();
        member2.setName(&quot;spring&quot;);

        //When
        memberService.join(member1);
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -&gt; memberService.join(member2));//예외가 발생해야 한다.
        assertThat(e.getMessage()).isEqualTo(&quot;이미 존재하는 회원입니다.&quot;);
    }

}</code></pre>