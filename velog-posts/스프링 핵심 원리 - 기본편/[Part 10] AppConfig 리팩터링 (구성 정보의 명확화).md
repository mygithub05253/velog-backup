# [Part 10] AppConfig 리팩터링 (구성 정보의 명확화)

**Published:** 2026-02-03T04:54:36.578Z
**Link:** https://velog.io/@kik328288/Part-10-AppConfig-리팩터링-구성-정보의-명확화

---

### 1. 현재 AppConfig의 문제점

---

방금 만든 `AppConfig` 코드를 다시 살펴봅시다.

```java
public class AppConfig {

    public MemberService memberService() {
        // 중복 1
        return new MemberServiceImpl(new MemoryMemberRepository());
    }

    public OrderService orderService() {
        return new OrderServiceImpl(
                new MemoryMemberRepository(), // 중복 2
                new FixDiscountPolicy());
    }
}
```

- **중복 발생:** `new MemoryMemberRepository()`가 두 번 호출되고 있습니다. 만약 나중에 DB를 **MySQL**로 바꾼다면 코드를 두 군데 다 고쳐야 합니다.
- **역할의 불명확:** `memberService()`라는 메서드 이름만 보면 알겠지만, 이 안에서 **'회원 저장소'** 역할이 무엇인지, **'할인 정책'** 역할이 무엇인지 한눈에 파악하기가 조금 어렵습니다.

### 2. 리팩터링: 역할과 구현을 명확하게 분리

---

메서드를 추출(Extract Method)하여 중복을 제거하고 역할을 명확히 드러냅니다.

`AppConfig.java` (리팩터링 후)

```java
package hello.core;

import hello.core.discount.DiscountPolicy;
import hello.core.discount.FixDiscountPolicy;
import hello.core.member.MemberRepository;
import hello.core.member.MemberService;
import hello.core.member.MemberServiceImpl;
import hello.core.member.MemoryMemberRepository;
import hello.core.order.OrderService;
import hello.core.order.OrderServiceImpl;

public class AppConfig {

    // [역할] MemberService: 회원 서비스
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    // [역할] OrderService: 주문 서비스
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

    // [역할] MemberRepository: 회원 저장소 (중복 제거됨!)
    public MemberRepository memberRepository() {
        // [구현] 현재는 메모리 저장소 사용
        return new MemoryMemberRepository();
    }

    // [역할] DiscountPolicy: 할인 정책
    public DiscountPolicy discountPolicy() {
        // [구현] 현재는 정액 할인 정책 사용
        return new FixDiscountPolicy();
    }
}
```

### 3. 리팩터링의 효과

---

1. **중복 제거 (DRY 원칙):** `new MemoryMemberRepository()` 코드가 단 한 번만 등장합니다.
2. **역할과 구현의 가시성:** 메서드 이름(`memberRepository`, `discountPolicy`)만 봐도 애플리케이션에 어떤 **역할**들이 있는지 바로 알 수 있습니다.
3. **변경의 용이성:**
    - 나중에 **할인 정책을 정률(Rate)로 바꾸고 싶다면?**
    - `discountPolicy()` 메서드의 리턴값만 `return new RateDiscountPolicy()`로 딱 한 줄 고치면 됩니다.
    - 애플리케이션의 **구성(Configuration) 정보**가 한곳에 모여 있어 관리가 매우 쉬워집니다.

![](https://velog.velcdn.com/images/kik328288/post/e75ae202-39a7-402e-8da2-af33f9baf7d5/image.png)

- 구성 영역(AppConfig) 안에서 `memberService`, `orderService`, `memberRepository`, `discountPolicy` 메서드들이 서로 연결된 구조도를 캡처해주세요. 리팩터링의 목적을 가장 잘 보여주는 그림입니다.
