# [Part 6] 회원 도메인 설계와 개발 (순수 자바)

**Published:** Thu, 15 Jan 2026 09:18:05 GMT
**Link:** https://velog.io/@kik328288/Part-6-%ED%9A%8C%EC%9B%90-%EB%8F%84%EB%A9%94%EC%9D%B8-%EC%84%A4%EA%B3%84%EC%99%80-%EA%B0%9C%EB%B0%9C-%EC%88%9C%EC%88%98-%EC%9E%90%EB%B0%94

---

<h2 id="1-비즈니스-요구사항-분석">1. 비즈니스 요구사항 분석</h2>
<hr />
<p>기획자로부터 다음과 같은 요구사항을 전달받았다고 가정해 봅시다.</p>
<ul>
<li><strong>회원:</strong><ul>
<li>가입하고 조회할 수 있어야 합니다.</li>
<li>등급은 <strong>일반(Basic)</strong>과 <strong>VIP</strong> 두 가지가 있습니다.</li>
</ul>
</li>
<li><strong>데이터 저장소:</strong><ul>
<li>회원 데이터는 자체 DB를 구축할 수도 있고, 외부 시스템과 연동할 수도 있습니다.</li>
<li><strong>중요:</strong> 아직 <strong>데이터 저장소가 확정되지 않았습니다</strong>.</li>
</ul>
</li>
</ul>
<p><strong>🤔 개발자의 고민:</strong>
&quot;DB가 확정될 때까지 개발을 미뤄야 할까요?&quot;
아닙니다. 우리는 <strong>객체 지향 설계(역할과 구현의 분리)</strong>를 배웠습니다. 인터페이스를 만들고 구현체를 언제든지 갈아 끼울 수 있도록 설계하면 됩니다.</p>
<hr />
<h2 id="2-회원-도메인-설계">2. 회원 도메인 설계</h2>
<hr />
<h3 id="1-도메인-협력-관계-기획자개발자-공용">1) 도메인 협력 관계 (기획자/개발자 공용)</h3>
<hr />
<ul>
<li><strong>클라이언트</strong> $\rightarrow$ <strong>회원 서비스</strong> (회원가입, 회원조회) $\rightarrow$ <strong>회원 저장소</strong> (메모리, DB, 외부시스템)</li>
<li>저장소의 역할만 정의해두고, 실제 저장은 메모리에 할지 DB에 할지 나중에 결정합니다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/80191645-7da1-4bab-9611-21ae735fd0f6/image.png" /></p>
<h3 id="2-클래스-다이어그램-개발자용---정적">2) 클래스 다이어그램 (개발자용 - 정적)</h3>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/065837dc-39df-416d-b81e-32c3a5163dfb/image.png" /></p>
<ul>
<li><strong>Interface:</strong> <code>MemberService</code>, <code>MemberRepository</code>.</li>
<li><strong>Implementation:</strong> <code>MemberServiceImpl</code>, <code>MemoryMemberRepository</code>, <code>DbMemberRepository</code>.</li>
<li><code>MemberService</code>는 <code>MemberRepository</code> 인터페이스를 의존합니다.</li>
</ul>
<h3 id="3-객체-다이어그램">3) 객체 다이어그램</h3>
<hr />
<ul>
<li>앱 실행 시점에 실제 생성되는 객체들의 참조 관계 (New로 생성된 인스턴스 간의 연결).</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/4df854e6-3921-45ea-bd01-38ad8e8d1eb6/image.png" /></p>
<h2 id="3-회원-도메인-개발-코드-작성">3. 회원 도메인 개발 (코드 작성)</h2>
<hr />
<h3 id="1-회원-엔티티-member">1) 회원 엔티티 (<code>Member</code>)</h3>
<hr />
<p>단순한 데이터 전송 객체로, <code>id</code>, <code>name</code>, <code>grade</code>를 가집니다.</p>
<ul>
<li>alt + insert 버튼을 통해 생성자, getter, setter 등을 한 번에 코드에 삽입할 수 있습니다.</li>
</ul>
<pre><code class="language-java">package hello.core.member;

public class Member {
    private Long id;
    private String name;
    private Grade grade;

    public Member(Long id, String name, Grade grade) {
        this.id = id;
        this.name = name;
        this.grade = grade;
    }

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

    public Grade getGrade() {
        return grade;
    }

    public void setGrade(Grade grade) {
        this.grade = grade;
    }
}</code></pre>
<h3 id="2-회원-저장소-memberrepository">2) 회원 저장소 (<code>MemberRepository</code>)</h3>
<hr />
<ul>
<li><strong>인터페이스:</strong> <code>save()</code>, <code>findById()</code> 기능을 정의합니다.</li>
</ul>
<pre><code class="language-java">package hello.core.member;

public interface MemberRepository {
    void save(Member member);

    Member findById(Long memberId);
}</code></pre>
<ul>
<li><strong>구현체 (<code>MemoryMemberRepository</code>):</strong><ul>
<li>DB 확정 전까지 개발을 진행하기 위해 가장 단순한 <strong>메모리 저장소</strong>를 구현합니다.</li>
<li><code>Map&lt;Long, Member&gt;</code>를 사용하여 데이터를 저장합니다.</li>
</ul>
</li>
</ul>
<pre><code class="language-java">package hello.core.member;

import java.util.HashMap;
import java.util.Map;

public class MemoryMemberRepository implements MemberRepository {

        // 실무에서는 동시성 이슈로 ConcurrentHashMap 사용 권장
    private static Map&lt;Long, Member&gt; store = new HashMap&lt;&gt;();

    @Override
    public void save(Member member) {
        store.put(member.getId(), member);
    }

    @Override
    public Member findById(Long memberId) {
        return store.get(memberId);
    }

}</code></pre>
<h3 id="3-회원-서비스-memberservice">3) 회원 서비스 (<code>MemberService</code>)</h3>
<hr />
<ul>
<li><strong>인터페이스</strong></li>
</ul>
<pre><code class="language-java">package hello.core.member;

public interface MemberService {
    void join(Member member);

    Member findMember(Long memberId);
}</code></pre>
<ul>
<li><strong>구현체 (<code>MemberServiceImpl</code>):</strong><ul>
<li>비즈니스 로직(가입, 조회)을 처리합니다.</li>
<li><strong>⚠️ 주의할 점:</strong> 의존관계를 설정하는 부분입니다.</li>
</ul>
</li>
</ul>
<pre><code class="language-java">package hello.core.member;

public class MemberServiceImpl implements MemberService {

    // DIP 위반: 구현체(MemoryMemberRepository)를 직접 new로 생성하여 의존 중
    private final MemberRepository memberRepository = new MemoryMemberRepository();

    @Override
    public void join(Member member) {
        memberRepository.save(member);
    }

    @Override
    public Member findMember(Long memberId) {
        return memberRepository.findById(memberId);
    }

}</code></pre>
<p><strong>구현체 의존의 문제점 (DIP 위반):</strong></p>
<ul>
<li>현재 <code>MemberServiceImpl</code> 코드는 순수 자바로 작성하다 보니, 인터페이스를 쓰면서도 구현 클래스를 직접 <code>new</code>하고 있습니다.</li>
<li>이것은 <strong>&quot;배우(Service)가 직접 상대 배우(Repository)를 캐스팅하는 상황&quot;</strong>과 같습니다.</li>
<li>이 문제를 해결하기 위해 다음 파트들에서 <strong>'주문 도메인'</strong>을 만들며 문제점을 키워보고, 결국 <strong>스프링</strong>이 등장하게 됩니다.</li>
</ul>
<h3 id="4-회원-등급-grade">4) 회원 등급 (<code>Grade</code>)</h3>
<hr />
<pre><code class="language-java">package hello.core.member;

public enum Grade {
    BASIC,
    VIP
}</code></pre>
<h2 id="4-회원-도메인-실행과-테스트">4. 회원 도메인 실행과 테스트</h2>
<hr />
<p>애플리케이션 로직이 잘 동작하는지 확인해야 합니다. <code>main</code> 메서드에서 직접 실행해볼 수도 있지만, 실무에서는 <strong>JUnit</strong> 테스트 프레임워크를 사용합니다.</p>
<h3 id="회원가입-main-memberapp">회원가입 Main (<code>MemberApp</code>)</h3>
<hr />
<pre><code class="language-java">package hello.core;

import hello.core.member.Grade;
import hello.core.member.Member;
import hello.core.member.MemberService;
import hello.core.member.MemberServiceImpl;

public class MemberApp {

    public static void main(String[] args) {
        MemberService memberService = new MemberServiceImpl();
        Member member = new Member(1L, &quot;memberA&quot;, Grade.VIP);
        memberService.join(member);

        Member findMember = memberService.findMember(1L);
        System.out.println(&quot;new Member = &quot; + member.getName());
        System.out.println(&quot;find Member = &quot; + findMember.getName());
    }

}</code></pre>
<h3 id="junit-테스트-memberservicetest">JUnit 테스트 (<code>MemberServiceTest</code>)</h3>
<hr />
<ul>
<li><strong>Given:</strong> 환경 기반 (VIP 회원 생성).</li>
<li><strong>When:</strong> 동작 (회원 가입 실행).</li>
<li><strong>Then:</strong> 검증 (가입한 회원이 조회된 회원과 같은가?).</li>
</ul>
<pre><code class="language-java">package hello.core.member;

import org.junit.jupiter.api.Test;

// [중요] 최신 트렌드: AssertJ의 static import 사용
import static org.assertj.core.api.Assertions.*;

public class MemberServiceTest {

    MemberService memberService = new MemberServiceImpl();

    @Test
    void join() {
        // given
        Member member = new Member(1L, &quot;memberA&quot;, Grade.VIP);

        // when
        memberService.join(member);
        Member findMember = memberService.findMember(1L);

        // then
        // AssertJ 사용 (읽기 쉬운 검증 라이브러리)
        assertThat(member).isEqualTo(findMember);
    }

}</code></pre>
<p><strong>테스트 라이브러리의 표준화 (AssertJ):</strong></p>
<ul>
<li>과거: <code>Assertions.assertEquals(expected, actual)</code> (순서 헷갈림)</li>
<li><strong>현재:</strong> <code>assertThat(actual).isEqualTo(expected)</code> (직관적, 체이닝 가능)</li>
<li>강의 교안도 AssertJ를 쓰지만, import 실수를 방지하기 위해 <code>static import</code> 사용을 생활화하세요.</li>
</ul>
<h2 id="5-참고-자료">5. 참고 자료</h2>
<hr />
<p>단순한 예제 코드 뒤에 숨겨진 실무 지식을 보충해 드립니다.</p>
<h3 id="1-hashmap-vs-concurrenthashmap">1. <code>HashMap</code> vs <code>ConcurrentHashMap</code></h3>
<hr />
<p>교안 코드에 <code>store</code> 변수를 선언할 때 <code>HashMap</code>을 사용했습니다. 하지만 실무에서는 <strong>동시성 이슈(Concurrency Issue)</strong>가 발생할 수 있습니다.</p>
<ul>
<li><strong>문제:</strong> 여러 스레드가 동시에 <code>HashMap</code>에 접근하여 <code>put</code>을 시도하면 데이터가 꼬이거나 에러가 발생할 수 있습니다.</li>
<li><strong>해결:</strong> 실무에서 동시 접근이 발생하는 환경이라면 <code>ConcurrentHashMap</code>을 사용해야 합니다.</li>
<li><strong>참고 자료:</strong> <a href="https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ConcurrentHashMap.html">Java 공식 문서 - ConcurrentHashMap</a></li>
</ul>
<h3 id="2-왜-구현체-이름-뒤에-impl을-붙이나요">2. 왜 구현체 이름 뒤에 <code>Impl</code>을 붙이나요?</h3>
<hr />
<p>자바 개발자들 사이의 관례(Convention)입니다.</p>
<ul>
<li>인터페이스 하나에 구현 클래스가 <strong>오직 하나</strong>만 있을 때는 관례적으로 <code>InterfaceName</code> + <code>Impl</code>이라고 짓습니다.</li>
<li>만약 구현체가 2개 이상(예: <code>MemoryMemberRepository</code>, <code>DbMemberRepository</code>)이라면 <code>Impl</code>을 붙이지 않고 각각의 특징을 드러내는 이름을 사용합니다.</li>
</ul>
<h3 id="3-assertj-vs-junit-assertions">3. AssertJ vs JUnit Assertions</h3>
<hr />
<p>테스트 코드에서 <code>org.assertj.core.api.Assertions</code>를 사용하는 것을 보셨을 겁니다.</p>
<ul>
<li><strong>JUnit 기본:</strong> <code>assertEquals(expected, actual)</code> - 순서가 헷갈리고 가독성이 조금 떨어짐.</li>
<li><strong>AssertJ:</strong> <code>assertThat(actual).isEqualTo(expected)</code> - 문장처럼 읽혀서 가독성이 훨씬 좋습니다. 최근 스프링 부트 프로젝트에서는 AssertJ를 기본으로 많이 사용합니다.</li>
<li><strong>참고 자료:</strong> <a href="https://assertj.github.io/doc/">AssertJ 공식 문서</a></li>
</ul>