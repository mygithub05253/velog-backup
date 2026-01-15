# [Part 3] 좋은 객체 지향 설계의 5가지 원칙 (SOLID)

**Published:** Wed, 14 Jan 2026 07:35:40 GMT
**Link:** https://velog.io/@kik328288/Part-3-%EC%A2%8B%EC%9D%80-%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%EC%84%A4%EA%B3%84%EC%9D%98-5%EA%B0%80%EC%A7%80-%EC%9B%90%EC%B9%99-SOLID

---

<h2 id="1-solid란-무엇인가">1. SOLID란 무엇인가?</h2>
<hr />
<p>SOLID는 클린코드로 유명한 로버트 마틴이 설계한 원칙으로 다음 5가지 원칙의 앞 글자를 따서 만든 단어입니다.</p>
<ol>
<li><strong>SRP:</strong> 단일 책임 원칙 (Single Responsibility Principle)</li>
<li><strong>OCP:</strong> 개방-폐쇄 원칙 (Open/Closed Principle)</li>
<li><strong>LSP:</strong> 리스코프 치환 원칙 (Liskov Substitution Principle)</li>
<li><strong>ISP:</strong> 인터페이스 분리 원칙 (Interface Segregation Principle)</li>
<li><strong>DIP:</strong> 의존관계 역전 원칙 (Dependency Inversion Principle)</li>
</ol>
<h2 id="2-각-원칙-상세-정리">2. 각 원칙 상세 정리</h2>
<hr />
<h3 id="1-srp-단일-책임-원칙-single-responsibility-principle">1) SRP: 단일 책임 원칙 (Single Responsibility Principle)</h3>
<hr />
<ul>
<li><strong>정의:</strong> 한 클래스는 하나의 책임만 가져야 합니다 .</li>
<li><strong>핵심 기준:</strong> '책임'이라는 단어는 모호할 수 있습니다. 중요한 판단 기준은 <strong>'변경'</strong>입니다 .<ul>
<li>변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 따른 것입니다.</li>
<li>예) UI를 변경하는데 비즈니스 로직(SQL 등)까지 고쳐야 한다면 SRP 위반입니다.</li>
</ul>
</li>
</ul>
<h3 id="2-ocp-개방-폐쇄-원칙-openclosed-principle-⭐-가장-중요">2) OCP: 개방-폐쇄 원칙 (Open/Closed Principle) ⭐ <strong>(가장 중요)</strong></h3>
<hr />
<ul>
<li><strong>정의:</strong> 소프트웨어 요소는 <strong>확장에는 열려</strong> 있으나 <strong>변경에는 닫혀</strong> 있어야 합니다 .</li>
<li><strong>의문:</strong> &quot;기능을 확장하려면 당연히 코드를 변경해야 하는 것 아닌가?&quot;</li>
<li><strong>해결책:</strong> <strong>다형성(Polymorphism)</strong>을 활용합니다 . 인터페이스를 구현한 새로운 클래스를 하나 만들어서 새로운 기능을 구현하면, 기존 코드를 변경하지 않고 확장할 수 있습니다 .</li>
</ul>
<p><strong>⚠️ OCP의 문제점 (순수 자바의 한계)</strong>
아래 코드를 보면, 다형성을 사용했음에도 불구하고 OCP가 깨지는 것을 볼 수 있습니다.</p>
<pre><code class="language-java">public class MemberService {
    // 기존 코드
    // private MemberRepository memberRepository = new MemoryMemberRepository();

    // 변경 코드 (구현체를 변경하려면 클라이언트 코드를 직접 수정해야 함!)
    private MemberRepository memberRepository = new JdbcMemberRepository();
}</code></pre>
<ul>
<li>구현 객체를 변경하려면 <strong>클라이언트(<code>MemberService</code>) 코드를 변경</strong>해야 합니다 .</li>
<li>분명 다형성을 사용했지만 <strong>OCP 원칙을 지킬 수 없습니다</strong> .</li>
<li>이 문제를 해결하려면 객체를 생성하고 연관관계를 맺어주는 별도의 <strong>조립, 설정자(Spring Container)</strong>가 필요합니다 .</li>
</ul>
<h3 id="3-lsp-리스코프-치환-원칙-liskov-substitution-principle">3) LSP: 리스코프 치환 원칙 (Liskov Substitution Principle)</h3>
<hr />
<ul>
<li><strong>정의:</strong> 프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 합니다 .</li>
<li><strong>핵심:</strong> 단순히 컴파일에 성공하는 것을 넘어서는 이야기입니다. <strong>'인터페이스의 규약'</strong>을 지켜야 한다는 뜻입니다 .</li>
<li><strong>예시:</strong> 자동차 인터페이스의 '엑셀' 기능은 앞으로 가라는 기능입니다. 만약 뒤로 가게 구현한다면 컴파일은 되더라도 LSP 위반입니다 .</li>
</ul>
<h3 id="4-isp-인터페이스-분리-원칙-interface-segregation-principle">4) ISP: 인터페이스 분리 원칙 (Interface Segregation Principle)</h3>
<hr />
<ul>
<li><strong>정의:</strong> 특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫습니다 .</li>
<li><strong>예시:</strong><ul>
<li>자동차 인터페이스 $\rightarrow$ 운전 인터페이스, 정비 인터페이스로 분리 .</li>
<li>사용자 클라이언트 $\rightarrow$ 운전자 클라이언트, 정비사 클라이언트로 분리 .</li>
</ul>
</li>
<li><strong>장점:</strong> 인터페이스가 명확해지고, 대체 가능성이 높아집니다 .</li>
</ul>
<h3 id="5-dip-의존관계-역전-원칙-dependency-inversion-principle-⭐-가장-중요">5) DIP: 의존관계 역전 원칙 (Dependency Inversion Principle) ⭐ <strong>(가장 중요)</strong></h3>
<hr />
<ul>
<li><strong>정의:</strong> 프로그래머는 <strong>&quot;추상화에 의존해야지, 구체화에 의존하면 안 된다&quot;</strong> .</li>
<li><strong>쉬운 설명:</strong> 구현 클래스(구현)에 의존하지 말고, <strong>인터페이스(역할)에 의존</strong>하라는 뜻입니다 .</li>
</ul>
<p><strong>⚠️ DIP 위반 (순수 자바의 한계)</strong>
앞서 본 OCP 문제 코드를 다시 보면 DIP도 위반하고 있습니다.</p>
<pre><code class="language-java">// MemberService는 인터페이스(MemberRepository)에도 의존하지만,
// 구현 클래스(MemoryMemberRepository)에도 동시에 의존한다.
MemberRepository m = new MemoryMemberRepository();</code></pre>
<ul>
<li><code>MemberService</code>가 구현 클래스를 직접 선택하고 있습니다 (<code>new ...</code>) .</li>
<li>이는 <strong>DIP 위반</strong>입니다 .</li>
</ul>
<h2 id="3-정리-객체-지향의-핵심과-한계">3. 정리: 객체 지향의 핵심과 한계</h2>
<hr />
<ul>
<li>객체 지향의 핵심은 <strong>다형성(Polymorphism)</strong>입니다 .</li>
<li>하지만 다형성만으로는 구현 객체를 변경할 때 클라이언트 코드도 함께 변경됩니다 .</li>
<li>즉, <strong>다형성만으로는 OCP, DIP를 지킬 수 없습니다</strong> .</li>
<li><strong>뭔가 더 필요합니다.</strong> (그것이 바로 <strong>Spring</strong>입니다!) .</li>
</ul>