# [Part 9] 관심사의 분리와 AppConfig의 등장

**Published:** 2026-02-03T04:53:30.677Z
**Link:** https://velog.io/@kik328288/Part-9-관심사의-분리와-AppConfig의-등장

---

### 1. 인터페이스에만 의존하도록 변경 (하지만 실패)

---

지난 시간(Part 8), 우리는 `OrderServiceImpl`이 `FixDiscountPolicy` 같은 구체 클래스에 의존(DIP 위반)하고 있음을 발견했습니다.
이를 해결하기 위해, 과감하게 **구체 클래스 의존을 모두 지우고 인터페이스에만 의존**하도록 코드를 변경해 봅시다.

`OrderServiceImpl.java` (수정)

```java
public class OrderServiceImpl implements OrderService {

    private final MemberRepository memberRepository = new MemoryMemberRepository();
    
    // [수정 전] 구체 클래스(RateDiscountPolicy)에 의존
    // private final DiscountPolicy discountPolicy = new RateDiscountPolicy();

    // [수정 후] 인터페이스에만 의존! (DIP 준수)
    private DiscountPolicy discountPolicy;

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);
        
        // 🚨 실행 시 여기서 NullPointerException 발생!
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}
```

**❌ 문제 발생:**
코드는 깔끔해졌지만, 실제 실행(테스트)을 해보면 **`NullPointerException`**이 발생합니다.
이유는 간단합니다. `discountPolicy` 인터페이스 변수만 선언했을 뿐, **실제 구현 객체를 할당(대입)해 주는 코드가 없기 때문**입니다.

**🔑 해결의 실마리:**
누군가가 클라이언트인 `OrderServiceImpl` 대신에, `DiscountPolicy`의 **구현 객체를 생성하고 주입**해주어야 합니다.

### 2. 관심사의 분리 (공연 기획자의 등장)

---

여기서 아주 중요한 **'공연'의 비유**가 등장합니다. (이 비유는 면접이나 동료 설득 시에도 매우 유용합니다!)

- **기존 코드의 문제점:**
    - 로미오 역할(인터페이스)을 맡은 **디카프리오(구현체)**가 줄리엣 역할의 **여자 주인공(구현체)을 직접 초빙**하는 꼴입니다.
    - 디카프리오는 **'연기'**도 해야 하고, **'배우 섭외'**도 해야 합니다. **책임이 너무 많습니다.**
- **관심사의 분리:**
    - 배우는 **본인의 배역을 수행하는 것**에만 집중해야 합니다.
    - 상대 배우가 누구든 똑같이 공연할 수 있어야 합니다.
    - 공연을 구성하고, 배우를 섭외하고, 배역을 지정하는 책임은 별도의 **'공연 기획자'**가 담당해야 합니다.

**AppConfig**가 바로 이 **공연 기획자**입니다.
애플리케이션의 전체 동작 방식을 **구성(Configuration)**하기 위해, **구현 객체를 생성하고 연결하는 책임**을 담당하는 별도의 클래스를 만듭니다.

### 3. AppConfig 리팩터링 (`AppConfig`)

---

프로젝트의 루트 패키지(`hello.core`)에 `AppConfig` 클래스를 생성합니다.

```java
package hello.core;

import hello.core.discount.FixDiscountPolicy;
import hello.core.member.MemberService;
import hello.core.member.MemberServiceImpl;
import hello.core.member.MemoryMemberRepository;
import hello.core.order.OrderService;
import hello.core.order.OrderServiceImpl;

public class AppConfig {

    // MemberService 역할에 대한 구현체 생성 및 연결
    public MemberService memberService() {
        // 생성자 주입: MemberServiceImpl에 MemoryMemberRepository를 넣어줌
        return new MemberServiceImpl(new MemoryMemberRepository());
    }

    // OrderService 역할에 대한 구현체 생성 및 연결
    public OrderService orderService() {
        // 생성자 주입: OrderServiceImpl에 Repository와 DiscountPolicy를 넣어줌
        return new OrderServiceImpl(
                new MemoryMemberRepository(),
                new FixDiscountPolicy());
    }
}
```

**💡 AppConfig가 하는 일:**

1. 애플리케이션의 실제 동작에 필요한 **구현 객체를 생성**합니다.
    - `MemberServiceImpl`
    - `MemoryMemberRepository`
    - `OrderServiceImpl`
    - `FixDiscountPolicy`
2. 생성한 객체 인스턴스의 참조(레퍼런스)를 **생성자를 통해서 주입(연결)**해줍니다.

![](https://velog.velcdn.com/images/kik328288/post/ce4f1aca-bffd-4bc8-9455-b397690fef0b/image.png)

- **설명:** `appConfig` 객체가 `memoryMemberRepository`를 생성하고, `memberServiceImpl` 생성자에 참조값을 찔러 넣어주는(주입하는) 화살표 그림. **DI(의존관계 주입)의 핵심 이미지**입니다.

### 4. 서비스 구현체 변경 (생성자 주입 적용)

---

이제 `AppConfig`가 객체를 넣어줄 수 있도록, 서비스 코드에 **생성자**를 만들어야 합니다.

1) `MemberServiceImpl` 변경

```java
package hello.core.member;

public class MemberServiceImpl implements MemberService {

    // final 키워드 유지 (생성자에서 무조건 값이 할당되어야 함을 보장)
    private final MemberRepository memberRepository;

    // [생성자 주입]
    // MemoryMemberRepository를 지우고, 생성자를 통해 외부에서 받도록 변경
    public MemberServiceImpl(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    @Override
    public void join(Member member) {
        memberRepository.save(member);
    }

    @Override
    public Member findMember(Long memberId) {
        return memberRepository.findById(memberId);
    }
}
```

- **설계 변경:** 이제 `MemberServiceImpl`은 `MemoryMemberRepository`를 전혀 모릅니다. 오직 `MemberRepository` 인터페이스에만 의존합니다.
- **DIP 완성:** 구체 클래스에 대한 의존이 완전히 사라졌습니다.

2) `OrderServiceImpl` 변경

```java
package hello.core.order;

import hello.core.discount.DiscountPolicy;
import hello.core.member.Member;
import hello.core.member.MemberRepository;

public class OrderServiceImpl implements OrderService {

    // 인터페이스에만 의존!
    private final MemberRepository memberRepository;
    private final DiscountPolicy discountPolicy;

    // [생성자 주입]
    // 어떤 구현체가 들어올지는 알 수 없다. 오직 외부(AppConfig)에서 결정한다.
    public OrderServiceImpl(MemberRepository memberRepository, DiscountPolicy discountPolicy) {
        this.memberRepository = memberRepository;
        this.discountPolicy = discountPolicy;
    }

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}
```

- **철저한 분업:** `OrderServiceImpl`은 이제 **'실행'**하는 책임만 집니다. 어떤 할인 정책을 쓸지는 기획자(`AppConfig`)가 정해줍니다.

![](https://velog.velcdn.com/images/kik328288/post/edae3fbc-3a70-46a7-947f-b2e44a418cc9/image.png)


- **설명:** `MemberServiceImpl`이 `MemberRepository` 인터페이스만 바라보고 있고, 아래에서 `AppConfig`가 생성(`create`) 화살표를 보내는 구조도

### 5. AppConfig 실행 및 테스트

---

이제 `AppConfig`를 통해 애플리케이션을 실행해 봅시다.

1) `MemberApp` (사용 클래스)

```java
public class MemberApp {
    public static void main(String[] args) {
        // AppConfig를 통해 객체 생성
        AppConfig appConfig = new AppConfig();
        // appConfig가 다 결정해서 줌
        MemberService memberService = appConfig.memberService(); 
        
        // ... 기존 로직 실행 ...
    }
}
```

2) `OrderApp` (사용 클래스)

```java
public class OrderApp {
    public static void main(String[] args) {
        AppConfig appConfig = new AppConfig();
        MemberService memberService = appConfig.memberService();
        OrderService orderService = appConfig.orderService();

        // ... 기존 로직 실행 ...
    }
}
```

3) 테스트 코드 오류 수정 (`MemberServiceTest`, `OrderServiceTest`)

기존 테스트 코드는 `new MemberServiceImpl()` 처럼 직접 생성했기 때문에 컴파일 오류가 납니다. `@BeforeEach`를 사용하여 테스트 실행 전에 `AppConfig`를 통해 주입받도록 수정합니다.

```java
class OrderServiceTest {

    MemberService memberService;
    OrderService orderService;

    @BeforeEach
    public void beforeEach() {
        AppConfig appConfig = new AppConfig();
        memberService = appConfig.memberService();
        orderService = appConfig.orderService();
    }
    
    // ... @Test 코드들 ...
}
```

### 📝 정리: 무엇이 좋아졌는가?

---

1. **관심사의 분리:** 객체를 **생성하고 연결**하는 역할(`AppConfig`)과 **실행**하는 역할(`ServiceImpl`)이 명확히 분리되었습니다.
2. **DIP 준수:** 클라이언트 코드(`ServiceImpl`)는 이제 구체 클래스를 몰라도 됩니다. 추상 인터페이스에만 의존합니다.
3. **OCP 준비:** 만약 할인 정책을 변경하고 싶다면? 클라이언트 코드는 손댈 필요 없이, **구성 영역인 `AppConfig`만 수정**하면 됩니다. (이 내용은 다음 파트에서 자세히 확인합니다!)
