# [Part 8] 새로운 할인 정책과 OCP, DIP의 붕괴

**Published:** 2026-02-02T09:06:15.505Z
**Link:** https://velog.io/@kik328288/Part-8-새로운-할인-정책과-OCP-DIP의-붕괴

---

### 1. 비즈니스 요구사항 변경 (악덕 기획자의 등장)

---

서비스 오픈 직전, 기획자가 찾아와 요구사항을 변경합니다.

- **기존:** VIP는 무조건 **1000원** 고정 할인 (FixDiscountPolicy).
- **변경:** VIP는 주문 금액의 **10%**를 할인하는 **정률 할인(RateDiscountPolicy)**으로 변경.

**👨‍💻 순진한 개발자:** "처음부터 고정 할인은 아니라고 했잖아요!"
**😈 악덕 기획자:** "애자일(Agile) 몰라요? 계획을 따르기보다 변화에 대응해야죠!"
우리는 다형성을 사용해 인터페이스(`DiscountPolicy`)를 만들어 두었으니, 괜찮을 것이라 생각하고 새로운 정책을 개발합니다.

### 2. 새로운 할인 정책 개발 (`RateDiscountPolicy`)

---

새로운 요구사항인 10% 할인을 적용하는 구현체를 만듭니다.

![](https://velog.velcdn.com/images/kik328288/post/09fd7981-85ab-4f42-801d-e16af09077e4/image.png)

```java
package hello.core.discount;

import hello.core.member.Grade;
import hello.core.member.Member;

public class RateDicountPolicy implements DiscountPolicy {
    private int discountPercent = 10; // 10% 할인

    @Override
    public int discount(Member member, int price) {
        if (member.getGrade() == Grade.VIP) {
            return price * discountPercent / 100; // 주문 금액의 10%
        } else {
            return 0;
        }
    }
}
```

### 3. 새로운 할인 정책 테스트 (JUnit 5 + AssertJ) (`RateDiscountPolicyTest`)

---

로직이 맞는지 검증하기 위해 테스트를 작성합니다. VIP는 10% 할인이 적용되어야 하고, 일반 회원은 할인이 없어야 합니다.

```java
package hello.core.discount;

import hello.core.member.Grade;
import hello.core.member.Member;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.*;

class RateDicountPolicyTest {

    RateDicountPolicy discountPolicy = new RateDicountPolicy();

    @Test
    @DisplayName("VIP는 10% 할인이 적용되어야 한다")
    void vip_o() {
        // given
        Member member = new Member(1L, "memberVIP", Grade.VIP);
        // when
        int discount = discountPolicy.discount(member, 10000);
        // then
        assertThat(discount).isEqualTo(1000); // 10000원의 10% = 1000원
    }

    // 성공 테스트 뿐만 아니라 실패하는 경우도 테스트 해볼 필요가 있습니다.
    @Test
    @DisplayName("VIP가 아니면 할인이 적용되지 않아야 한다")
    void vip_x() {
        // given
        Member member = new Member(2L, "memberBASIC", Grade.BASIC);
        // when
        int discount = discountPolicy.discount(member, 10000);
        // then
        assertThat(discount).isEqualTo(1000);
    }

}
```

- 실패 케이스 결과

![](https://velog.velcdn.com/images/kik328288/post/83dc2fd1-84f0-4f79-a641-a910a8f3d942/image.png)

### 4. 문제점 발견: 클라이언트 코드를 변경해야 한다!

---

새로 만든 `RateDiscountPolicy`를 적용하려고 `OrderServiceImpl` 코드를 열었습니다. 그런데 **코드를 수정해야만 적용이 가능**합니다.

`OrderServiceImpl.java` (수정 전후)

```java
package hello.core.order;

import hello.core.discount.DiscountPolicy;
import hello.core.discount.FixDiscountPolicy;
import hello.core.discount.RateDicountPolicy;
import hello.core.member.Member;
import hello.core.member.MemberRepository;
import hello.core.member.MemoryMemberRepository;

public class OrderServiceImpl implements OrderService {

    // 1. 회원 저장소 의존 (DIP 위반)
    private final MemberRepository memberRepository = new MemoryMemberRepository();

    // 2. 할인 정책 의존 (DIP 위반)
    // 인터페이스(DiscountPolicy)뿐만 아니라 구현체(FixDiscountPolicy)에도 의존하고 있음!
    // private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
    private final DiscountPolicy discountPolicy = new RateDicountPolicy();

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);

        // 설계가 잘된 점: 할인은 discountPolicy에게 전적으로 위임 (단일 책임 원칙 준수)
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}
```

**⁉️ 문제 분석:**

---

우리는 분명 역할과 구현을 분리했고, 다형성도 활용했습니다. 하지만 **객체 지향 설계 원칙을 위반**했습니다.
**1) DIP 위반 (의존관계 역전 원칙)**

---

클라이언트(`OrderServiceImpl`)는 인터페이스(`DiscountPolicy`)에만 의존하는 줄 알았는데, **실제로는 구현 클래스(`FixDiscountPolicy`, `RateDiscountPolicy`)에도 의존**하고 있습니다.

- **증거:** `new RateDiscountPolicy()`라고 직접 적었기 때문입니다.
- 기대했던 의존 관계

![](https://velog.velcdn.com/images/kik328288/post/26d4ff1b-b2c9-42e7-870e-eb4c577e9b97/image.png)

- **실제 의존 관계**

![](https://velog.velcdn.com/images/kik328288/post/6b323470-aaf3-4dc8-92b1-7d83447ba403/image.png)

**2) OCP 위반 (개방-폐쇄 원칙)**

---

기능을 확장(변경)해서 새로운 할인 정책을 적용하려고 하니, **클라이언트 코드(`OrderServiceImpl`)를 변경**해야 합니다.

- **이상적:** `Fix` $\rightarrow$ `Rate`로 변경해도 클라이언트 코드는 손대지 않아야 합니다.
- **현실:** 클라이언트 코드를 뜯어고쳐야 합니다.

![](https://velog.velcdn.com/images/kik328288/post/29922aa0-0847-41ac-a038-5cf07b227992/image.png)

### 5. 해결 방안 모색

---

이 문제를 해결하려면 어떻게 해야 할까요?

**DIP를 위반하지 않도록 인터페이스에만 의존하도록 의존관계를 변경**해야 합니다.

![](https://velog.velcdn.com/images/kik328288/post/d5845d58-8ce2-4ca4-b235-4f451648d869/image.png)


### 인터페이스에만 의존하도록 코드 변경 (가설)

---

```java
package hello.core.order;

import hello.core.discount.DiscountPolicy;
import hello.core.discount.FixDiscountPolicy;
import hello.core.discount.RateDicountPolicy;
import hello.core.member.Member;
import hello.core.member.MemberRepository;
import hello.core.member.MemoryMemberRepository;

public class OrderServiceImpl implements OrderService {

    // 1. 회원 저장소 의존 (DIP 위반)
    private final MemberRepository memberRepository = new MemoryMemberRepository();

    // 2. 할인 정책 의존 (DIP 위반)
    // 인터페이스(DiscountPolicy)뿐만 아니라 구현체(FixDiscountPolicy)에도 의존하고 있음!
    // private final DiscountPolicy discountPolicy = new FixDiscountPolicy();
    // private final DiscountPolicy discountPolicy = new RateDicountPolicy();
    private DiscountPolicy discountPolicy;

    @Override
    public Order createOrder(Long memberId, String itemName, int itemPrice) {
        Member member = memberRepository.findById(memberId);

        // 설계가 잘된 점: 할인은 discountPolicy에게 전적으로 위임 (단일 책임 원칙 준수)
        int discountPrice = discountPolicy.discount(member, itemPrice);

        return new Order(memberId, itemName, itemPrice, discountPrice);
    }
}
```

**🚨 결과:** 구현체가 없으므로 코드를 실행하면 `NullPointerException`이 발생합니다.

**🔑 결론:** 누군가가 클라이언트인 `OrderServiceImpl`에 `DiscountPolicy`의 **구현 객체를 대신 생성하고 주입(Injection)** 해주어야 합니다.
이 역할을 해줄 **"제3의 존재(공연 기획자)"**가 필요합니다.

### 추가 지식

---

### 1. 애자일 소프트웨어 개발 선언 (Agile Manifesto)

---

기획자가 언급한 "계획을 따르기보다 변화에 대응하기를"은 애자일 선언문의 핵심 가치 중 하나입니다.

- 하지만 이것이 "설계를 대충 해도 된다"는 뜻은 아닙니다.
- 오히려 변화에 유연하게 대응하기 위해 **더욱 탄탄한 객체 지향 설계(SOLID)**가 필요함을 역설적으로 보여주는 예시입니다.
