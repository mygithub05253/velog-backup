# [Part 7] 주문과 할인 도메인 설계와 개발

**Published:** Thu, 15 Jan 2026 09:20:24 GMT
**Link:** https://velog.io/@kik328288/Part-7-%EC%A3%BC%EB%AC%B8%EA%B3%BC-%ED%95%A0%EC%9D%B8-%EB%8F%84%EB%A9%94%EC%9D%B8-%EC%84%A4%EA%B3%84%EC%99%80-%EA%B0%9C%EB%B0%9C

---

<h2 id="1-비즈니스-요구사항-분석">1. 비즈니스 요구사항 분석</h2>
<hr />
<ul>
<li><strong>주문:</strong> 회원은 상품을 주문할 수 있습니다.</li>
<li><strong>할인 정책:</strong><ul>
<li>회원 등급(VIP)에 따라 할인 정책을 적용합니다.</li>
<li><strong>현재:</strong> VIP는 무조건 <strong>1000원</strong>을 할인해 주는 <strong>고정 금액 할인(FixDiscountPolicy)</strong>을 적용합니다.</li>
<li><strong>미래:</strong> 할인 정책은 변경 가능성이 높습니다. (회사 측에서 아직 확정을 못 함)</li>
</ul>
</li>
</ul>
<p><strong>🤔 개발자의 전략:</strong>
&quot;할인 정책이 정해질 때까지 기다릴까요?&quot;
아닙니다. <strong>역할(Interface)</strong>과 <strong>구현(Implementation)</strong>을 분리하면 됩니다. <code>DiscountPolicy</code>라는 인터페이스를 만들고, 일단 <code>FixDiscountPolicy</code>를 구현해서 개발합니다. 나중에 정책이 바뀌면 갈아 끼우면 됩니다.</p>
<h2 id="2-주문-도메인-설계">2. 주문 도메인 설계</h2>
<hr />
<h3 id="1-주문-도메인-협력-관계">1) 주문 도메인 협력 관계</h3>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/f93f251a-dec4-4f8e-a767-a717aefdd729/image.png" /></p>
<ol>
<li><strong>주문 생성:</strong> 클라이언트가 주문 서비스에 요청.</li>
<li><strong>회원 조회:</strong> 할인을 위해 회원 등급이 필요하므로 회원 저장소에서 조회.</li>
<li><strong>할인 적용:</strong> 주문 서비스는 할인 여부를 <strong>할인 정책(DiscountPolicy)</strong>에 위임.</li>
<li><strong>반환:</strong> 주문 결과 반환.</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/03fa7910-bc7d-4db8-80a3-76c46ac5e70d/image.png" /></p>
<ul>
<li>역할과 구현을 분리해서 자유롭게 구현 객체를 조립할 수 있게 설계했습니다.</li>
<li>이를 통해 회원 저장소 뿐만 아니라, 할인 정책 역시 유연하게 변경할 수 있습니다.</li>
</ul>
<h3 id="2-클래스-다이어그램">2) 클래스 다이어그램</h3>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/5088e19b-4dfd-4650-8bc8-9a05e52746f4/image.png" /></p>
<ul>
<li><strong>역할:</strong> <code>OrderService</code>, <code>MemberRepository</code>, <strong><code>DiscountPolicy</code></strong>.</li>
<li><strong>구현:</strong> <code>OrderServiceImpl</code>, <code>MemoryMemberRepository</code>, <strong><code>FixDiscountPolicy</code></strong>.</li>
<li><strong>특징:</strong> <code>OrderServiceImpl</code>은 <code>DiscountPolicy</code> 인터페이스에 의존합니다. (이상적으로는)</li>
</ul>
<h3 id="3-객체-다이어그램">3) 객체 다이어그램</h3>
<hr />
<ol>
<li>주문 도메인 객체 다이어그램 1</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/0692722c-8788-440a-a64d-c635658f94d7/image.png" /></p>
<ul>
<li>회원을 메모리에서 조회하고, 정액 할인 정책(고정 금액)을 지원해도 주문 서비스를 변경하지 않아도 됩니다.</li>
<li>역할들의 협력 관계를 그대로 재사용 할 수 있습니다.</li>
</ul>
<ol>
<li>주문 도메인 객체 다이어그램 2</li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/b6ddc88f-5067-414e-81a4-7a4a7a541e77/image.png" /></p>
<ul>
<li>회원을 메모리가 아닌 실제 DB에서 조회하고, 정률 할인 정책(주문 금액에 따라 % 할인)을 지원해도 주문 서비스를 변경하지 않아도 됩니다.</li>
<li>협력 관계를 그대로 재사용 할 수 있습니다.</li>
</ul>
<h2 id="3-주문과-할인-도메인-개발-code">3. 주문과 할인 도메인 개발 (Code)</h2>
<hr />
<h3 id="1-할인-정책-인터페이스-discountpolicy">1) 할인 정책 인터페이스 (<code>DiscountPolicy</code>)</h3>
<hr />
<pre><code class="language-java">package hello.core.discount;

import hello.core.member.Member;

public interface DiscountPolicy {

    // @return 할인 대상 금액
    int discount(Member member. int price);

}</code></pre>
<h3 id="2-정액-할인-정책-구현체-fixdiscountpolicy">2) 정액 할인 정책 구현체 (<code>FixDiscountPolicy</code>)</h3>
<hr />
<p><strong>VIP</strong>면 1000원, 아니면 0원을 반환하는 단순한 로직입니다.</p>
<pre><code class="language-java">package hello.core.discount;

import hello.core.member.Grade;
import hello.core.member.Member;

public class FixDiscountPolicy implements DiscountPolicy {

    private int discountFixAmount = 1000; // 1000원 할인

    @Override
    public int discount(Member member, int price) {
        // Enum 비교는 == 사용
        if (member.getGrade() == Grade.VIP) {
            return discountFixAmount;
        } else {
            return 0;
        }
    }
}</code></pre>
<h3 id="3-주문-엔티티-order">3) 주문 엔티티 (<code>Order</code>)</h3>
<hr />
<p>주문 결과 데이터를 담고 있는 객체입니다. 계산 로직(<code>calculatePrice</code>)을 포함하고 있습니다.</p>
<pre><code class="language-java">package hello.core.order;

public class Order {

    private Long memberId;
    private String itemName;
    private int itemPrice;
    private int discountPrice;

    public Order(Long memberId, String itemName, int itemPrice, int discountPrice) {
        this.memberId = memberId;
        this.itemName = itemName;
        this.itemPrice = itemPrice;
        this.discountPrice = discountPrice;
    }

    // 계산된 결과 가격 (원가 - 할인 가격)
    public int calculatePrice() {
        return itemPrice - discountPrice;
    }

    public Long getMemberId() {
        return memberId;
    }

    public void setMemberId(Long memberId) {
        this.memberId = memberId;
    }

    public String getItemName() {
        return itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public int getItemPrice() {
        return itemPrice;
    }

    public void setItemPrice(int itemPrice) {
        this.itemPrice = itemPrice;
    }

    public int getDiscountPrice() {
        return discountPrice;
    }

    public void setDiscountPrice(int discountPrice) {
        this.discountPrice = discountPrice;
    }

    @Override
    public String toString() {
        return &quot;Order{&quot; +
                &quot;memberId=&quot; + memberId +
                &quot;, itemName='&quot; + itemName + '\'' +
                &quot;, itemPrice=&quot; + itemPrice +
                &quot;, discountPrice=&quot; + discountPrice +
                '}';
    }
}</code></pre>
<h3 id="4-주문-서비스-인터페이스-orderservice">4) 주문 서비스 인터페이스 (<code>OrderService</code>)</h3>
<hr />
<pre><code class="language-java">package hello.core.order;

public interface OrderService {
    Order createOrder(Long memberId, String itemName, int itemPrice);
}</code></pre>
<h3 id="5-주문-서비스-구현체-orderserviceimpl-🚨-중요">5) 주문 서비스 구현체 (<code>OrderServiceImpl</code>) 🚨 <strong>중요!</strong></h3>
<hr />
<p>여기가 가장 중요합니다. 설계를 잘한 것 같지만 <strong>치명적인 문제</strong>가 숨어 있습니다.</p>
<pre><code class="language-java">package hello.core.order;

import hello.core.discount.DiscountPolicy;
import hello.core.discount.FixDiscountPolicy;
import hello.core.member.Member;
import hello.core.member.MemberRepository;
import hello.core.member.MemoryMemberRepository;

public class OrderServiceImpl implements OrderService {

    // 1. 회원 저장소 의존 (DIP 위반)
    private final MemberRepository memberRepository = new MemoryMemberRepository();

    // 2. 할인 정책 의존 (DIP 위반)
    // 인터페이스(DiscountPolicy)뿐만 아니라 구현체(FixDiscountPolicy)에도 의존하고 있음!
    private final DiscountPolicy discountPolicy = new FixDiscountPolicy();

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);

        // 설계가 잘된 점: 할인은 discountPolicy에게 전적으로 위임 (단일 책임 원칙 준수)
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}</code></pre>
<h2 id="4-테스트-코드-작성-junit-5--assertj">4. 테스트 코드 작성 (JUnit 5 + AssertJ)</h2>
<hr />
<ul>
<li><code>OrderApp</code></li>
</ul>
<pre><code class="language-java">package hello.core;

import hello.core.member.Grade;
import hello.core.member.Member;
import hello.core.member.MemberService;
import hello.core.member.MemberServiceImpl;
import hello.core.order.Order;
import hello.core.order.OrderService;
import hello.core.order.OrderServiceImpl;

public class OrderApp {

    public static void main(String[] args) {
        MemberService memberService = new MemberServiceImpl();
        OrderService orderService = new OrderServiceImpl();

        Long memberId = 1L;
        Member member = new Member(memberId, &quot;memberA&quot;, Grade.VIP);
        memberService.join(member);

        Order order = orderService.createOrder(memberId, &quot;itemA&quot;, 10000);

        System.out.println(&quot;order = &quot; + order);
        System.out.println(&quot;order.calculatePrice = &quot; + order.calculatePrice());
    }
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/fa2d4386-6d19-4a65-9d85-ec23f7b70c1d/image.png" /></p>
<ul>
<li><code>OrderServiceTest</code></li>
</ul>
<p>단위 테스트를 통해 로직이 정상 동작하는지 검증합니다.</p>
<pre><code class="language-java">package hello.core.order;

import hello.core.member.Grade;
import hello.core.member.Member;
import hello.core.member.MemberService;
import hello.core.member.MemberServiceImpl;
import org.junit.jupiter.api.Test;

// 최신 트렌드: static import 사용
import static org.assertj.core.api.Assertions.*;

public class OrderServiceTest {

    MemberService memberService = new MemberServiceImpl();
    OrderService orderService = new OrderServiceImpl();

    @Test
    void createOrder() {
        // given
        Long memberId = 1L;
        Member member = new Member(memberId, &quot;memberA&quot;, Grade.VIP);
        memberService.join(member);

        // when
        Order order = orderService.createOrder(memberId, &quot;itemA&quot;, 10000);

        // then
        // VIP는 1000원 할인이 적용되어야 한다.
        assertThat(order.getDiscountPrice()).isEqualTo(1000);
    }
}</code></pre>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/813c1fea-a0b3-4c1e-95f9-393a01ccd074/image.png" /></p>
<h2 id="5-참고-자료">5. 참고 자료</h2>
<hr />
<h3 id="1-돈을-다룰-때-int를-써도-될까요">1. 돈을 다룰 때 <code>int</code>를 써도 될까요?</h3>
<hr />
<p>강의 예제에서는 편의상 <code>int</code>를 사용했지만, 실무에서 돈(화폐)을 다룰 때는 <strong>절대 <code>int</code>나 <code>double</code>을 사용하면 안 됩니다.</strong></p>
<ul>
<li><strong>이유:</strong> 부동 소수점 문제로 인한 계산 오차가 발생할 수 있고, 표현 범위를 넘어서는 경우가 생깁니다.</li>
<li><strong>해결:</strong> 자바에서는 <strong><code>BigDecimal</code></strong> 클래스를 사용해야 정확한 금융 계산이 가능합니다.</li>
<li><strong>참고 자료:</strong> <a href="https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html">Java 공식 문서 - BigDecimal</a></li>
</ul>
<h3 id="2-enum-비교--vs-equals">2. Enum 비교, <code>==</code> vs <code>equals</code>?</h3>
<hr />
<p><code>FixDiscountPolicy</code>에서 <code>member.getGrade() == Grade.VIP</code>로 비교했습니다.</p>
<ul>
<li><strong>Enum:</strong> 자바의 Enum은 싱글톤처럼 유일한 객체임이 보장되므로 <code>==</code> (참조 비교)를 사용하는 것이 <code>NullPointerException</code> 안전성 면에서나 성능 면에서 더 권장됩니다.</li>
</ul>
<h3 id="3-테스트-메서드-이름-displayname">3. 테스트 메서드 이름 (<code>@DisplayName</code>)</h3>
<hr />
<p>실무에서는 테스트 메서드 이름만 보고도 내용을 알 수 있게 <strong>한글</strong>로 적거나, JUnit 5의 <code>@DisplayName</code>을 사용합니다.</p>
<pre><code class="language-java">@Test
@DisplayName(&quot;VIP 회원은 1000원 고정 할인이 적용되어야 한다&quot;)
void createOrder_VIP() { ... }</code></pre>