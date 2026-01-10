# 스프링 DB 기술 - 스프링 JdbcTemplate

**Published:** Fri, 09 Jan 2026 07:32:36 GMT
**Link:** https://velog.io/@kik328288/%EC%8A%A4%ED%94%84%EB%A7%81-DB-%EA%B8%B0%EC%88%A0-%EC%8A%A4%ED%94%84%EB%A7%81-JdbcTemplate

---

<h2 id="13-스프링-jdbctemplate">13. 스프링 JdbcTemplate</h2>
<hr />
<p>순수 JDBC의 반복 코드를 대부분 제거해 주지만, SQL은 여전히 개발자가 직접 작성해야 한다.</p>
<h3 id="131-특징">13.1 특징</h3>
<hr />
<ul>
<li>JDBC API에서 본 <code>try-catch-finally</code>, 커넥션 동기화 등의 코드를 제거한다.</li>
<li><strong>실무 활용:</strong> 복잡한 동적 쿼리가 필요할 때 JPA와 함께 유용하게 사용된다.</li>
</ul>
<h3 id="132-코드-비교">13.2 코드 비교</h3>
<hr />
<p>순수 JDBC에 비해 코드가 획기적으로 줄어든다.</p>
<pre><code class="language-java">// JdbcTemplate 사용 예제
@Override
public Optional&lt;Member&gt; findById(Long id) {
    List&lt;Member&gt; result = jdbcTemplate.query(&quot;select * from member where id = ?&quot;, memberRowMapper(), id);
    return result.stream().findAny();
}

private RowMapper&lt;Member&gt; memberRowMapper() {
    return (rs, rowNum) -&gt; {
        Member member = new Member();
        member.setId(rs.getLong(&quot;id&quot;));
        member.setName(rs.getString(&quot;name&quot;));
        return member;
    };
}</code></pre>
<h3 id="133-코드-jdbctemplatememberrepository">13.3 코드 (<code>JdbcTemplateMemberRepository</code>)</h3>
<hr />
<pre><code class="language-java">package hello.hello_spring.repository;

import hello.hello_spring.domain.Member;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.simple.SimpleJdbcInsert;

import javax.sql.DataSource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public class JdbcTemplateMemberRepository implements MemberRepository {
    private final JdbcTemplate jdbcTemplate;

    public JdbcTemplateMemberRepository(DataSource dataSource) {
        jdbcTemplate = new JdbcTemplate(dataSource);
    }

    @Override
    public Member save(Member member) {
        SimpleJdbcInsert jdbcInsert = new SimpleJdbcInsert(jdbcTemplate);
        jdbcInsert.withTableName(&quot;member&quot;).usingGeneratedKeyColumns(&quot;id&quot;);

        Map&lt;String, Object&gt; parameters = new HashMap&lt;&gt;();
        parameters.put(&quot;name&quot;, member.getName());

        Number key = jdbcInsert.executeAndReturnKey(new MapSqlParameterSource(parameters));
        member.setId(key.longValue());
        return member;
    }

    @Override
    public Optional&lt;Member&gt; findById(Long id) {
        List&lt;Member&gt; result = jdbcTemplate.query(&quot;select * from member where id = ?&quot;, memberRowMapper(), id);
        return result.stream().findAny();
    }

    @Override
    public List&lt;Member&gt; findAll() {
        return jdbcTemplate.query(&quot;select * from member&quot;, memberRowMapper());
    }

    @Override
    public Optional&lt;Member&gt; findByName(String name) {
        List&lt;Member&gt; result = jdbcTemplate.query(&quot;select * from member where name = ?&quot;, memberRowMapper(), name);
        return result.stream().findAny();
    }

    private RowMapper&lt;Member&gt; memberRowMapper() {
        return (rs, rowNum) -&gt; {
            Member member = new Member();
            member.setId(rs.getLong(&quot;id&quot;));
            member.setName(rs.getString(&quot;name&quot;));
            return member;
        };
    }
}</code></pre>
<h3 id="134-스프링-설정-변경-springconfig">13.4 스프링 설정 변경 (<code>SpringConfig</code>)</h3>
<hr />
<pre><code class="language-java">package hello.hello_spring;

import hello.hello_spring.repository.JdbcMemberRepository;
import hello.hello_spring.repository.JdbcTemplateMemberRepository;
import hello.hello_spring.repository.MemberRepository;
import hello.hello_spring.repository.MemoryMemberRepository;
import hello.hello_spring.service.MemberService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;

@Configuration
public class SpringConfig {

    private final DataSource dataSource;

    public SpringConfig(DataSource dataSource) {
        this.dataSource = dataSource;
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
        return new JdbcTemplateMemberRepository(dataSource);
    }
}</code></pre>