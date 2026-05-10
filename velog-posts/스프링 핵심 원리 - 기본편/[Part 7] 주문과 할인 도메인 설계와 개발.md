# [Part 7] 주문과 할인 도메인 설계와 개발

**Published:** 2026-01-15T09:20:24.200Z
**Link:** https://velog.io/@kik328288/Part-7-주문과-할인-도메인-설계와-개발

---

## 1. 비즈니스 요구사항 분석

---

- **주문:** 회원은 상품을 주문할 수 있습니다.
- **할인 정책:**
    - 회원 등급(VIP)에 따라 할인 정책을 적용합니다.
    - **현재:** VIP는 무조건 **1000원**을 할인해 주는 **고정 금액 할인(FixDiscountPolicy)**을 적용합니다.
    - **미래:** 할인 정책은 변경 가능성이 높습니다. (회사 측에서 아직 확정을 못 함)

**🤔 개발자의 전략:**
"할인 정책이 정해질 때까지 기다릴까요?"
아닙니다. **역할(Interface)**과 **구현(Implementation)**을 분리하면 됩니다. `DiscountPolicy`라는 인터페이스를 만들고, 일단 `FixDiscountPolicy`를 구현해서 개발합니다. 나중에 정책이 바뀌면 갈아 끼우면 됩니다.

## 2. 주문 도메인 설계

---

### 1) 주문 도메인 협력 관계

---

![](https://velog.velcdn.com/images/kik328288/post/f93f251a-dec4-4f8e-a767-a717aefdd729/image.png)

1. **주문 생성:** 클라이언트가 주문 서비스에 요청.
2. **회원 조회:** 할인을 위해 회원 등급이 필요하므로 회원 저장소에서 조회.
3. **할인 적용:** 주문 서비스는 할인 여부를 **할인 정책(DiscountPolicy)**에 위임.
4. **반환:** 주문 결과 반환.

![](https://velog.velcdn.com/images/kik328288/post/03fa7910-bc7d-4db8-80a3-76c46ac5e70d/image.png)

- 역할과 구현을 분리해서 자유롭게 구현 객체를 조립할 수 있게 설계했습니다.
- 이를 통해 회원 저장소 뿐만 아니라, 할인 정책 역시 유연하게 변경할 수 있습니다.

### 2) 클래스 다이어그램

---

![](https://velog.velcdn.com/images/kik328288/post/5088e19b-4dfd-4650-8bc8-9a05e52746f4/image.png)

- **역할:** `OrderService`, `MemberRepository`, **`DiscountPolicy`**.
- **구현:** `OrderServiceImpl`, `MemoryMemberRepository`, **`FixDiscountPolicy`**.
- **특징:** `OrderServiceImpl`은 `DiscountPolicy` 인터페이스에 의존합니다. (이상적으로는)

### 3) 객체 다이어그램

---

1. 주문 도메인 객체 다이어그램 1

![](https://velog.velcdn.com/images/kik328288/post/0692722c-8788-440a-a64d-c635658f94d7/image.png)

- 회원을 메모리에서 조회하고, 정액 할인 정책(고정 금액)을 지원해도 주문 서비스를 변경하지 않아도 됩니다.
- 역할들의 협력 관계를 그대로 재사용 할 수 있습니다.
1. 주문 도메인 객체 다이어그램 2

![](https://velog.velcdn.com/images/kik328288/post/b6ddc88f-5067-414e-81a4-7a4a7a541e77/image.png)

- 회원을 메모리가 아닌 실제 DB에서 조회하고, 정률 할인 정책(주문 금액에 따라 % 할인)을 지원해도 주문 서비스를 변경하지 않아도 됩니다.
- 협력 관계를 그대로 재사용 할 수 있습니다.

## 3. 주문과 할인 도메인 개발 (Code)

---

### 1) 할인 정책 인터페이스 (`DiscountPolicy`)

---

```java
package hello.core.discount;

import hello.core.member.Member;

public interface DiscountPolicy {

    // @return 할인 대상 금액
    int discount(Member member. int price);

}
```

### 2) 정액 할인 정책 구현체 (`FixDiscountPolicy`)

---

**VIP**면 1000원, 아니면 0원을 반환하는 단순한 로직입니다.

```java
package hello.core.discount;

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
}
```

### 3) 주문 엔티티 (`Order`)

---

주문 결과 데이터를 담고 있는 객체입니다. 계산 로직(`calculatePrice`)을 포함하고 있습니다.

```java
package hello.core.order;

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
        return "Order{" +
                "memberId=" + memberId +
                ", itemName='" + itemName + '\'' +
                ", itemPrice=" + itemPrice +
                ", discountPrice=" + discountPrice +
                '}';
    }
}
```

### 4) 주문 서비스 인터페이스 (`OrderService`)

---

```java
package hello.core.order;

public interface OrderService {
    Order createOrder(Long memberId, String itemName, int itemPrice);
}
```

### 5) 주문 서비스 구현체 (`OrderServiceImpl`) 🚨 **중요!**

---

여기가 가장 중요합니다. 설계를 잘한 것 같지만 **치명적인 문제**가 숨어 있습니다.

```java
package hello.core.order;

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
}
```

## 4. 테스트 코드 작성 (JUnit 5 + AssertJ)

---

- `OrderApp`

```java
package hello.core;

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
        Member member = new Member(memberId, "memberA", Grade.VIP);
        memberService.join(member);

        Order order = orderService.createOrder(memberId, "itemA", 10000);

        System.out.println("order = " + order);
        System.out.println("order.calculatePrice = " + order.calculatePrice());
    }
}
```

![](https://velog.velcdn.com/images/kik328288/post/fa2d4386-6d19-4a65-9d85-ec23f7b70c1d/image.png)

- `OrderServiceTest`

단위 테스트를 통해 로직이 정상 동작하는지 검증합니다.

```java
package hello.core.order;

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
        Member member = new Member(memberId, "memberA", Grade.VIP);
        memberService.join(member);

        // when
        Order order = orderService.createOrder(memberId, "itemA", 10000);

        // then
        // VIP는 1000원 할인이 적용되어야 한다.
        assertThat(order.getDiscountPrice()).isEqualTo(1000);
    }
}
```

![](https://velog.velcdn.com/images/kik328288/post/813c1fea-a0b3-4c1e-95f9-393a01ccd074/image.png)


## 5. 참고 자료

---

### 1. 돈을 다룰 때 `int`를 써도 될까요?

---

강의 예제에서는 편의상 `int`를 사용했지만, 실무에서 돈(화폐)을 다룰 때는 **절대 `int`나 `double`을 사용하면 안 됩니다.**

- **이유:** 부동 소수점 문제로 인한 계산 오차가 발생할 수 있고, 표현 범위를 넘어서는 경우가 생깁니다.
- **해결:** 자바에서는 **`BigDecimal`** 클래스를 사용해야 정확한 금융 계산이 가능합니다.
- **참고 자료:** [Java 공식 문서 - BigDecimal](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html)

### 2. Enum 비교, `==` vs `equals`?

---

`FixDiscountPolicy`에서 `member.getGrade() == Grade.VIP`로 비교했습니다.

- **Enum:** 자바의 Enum은 싱글톤처럼 유일한 객체임이 보장되므로 `==` (참조 비교)를 사용하는 것이 `NullPointerException` 안전성 면에서나 성능 면에서 더 권장됩니다.

### 3. 테스트 메서드 이름 (`@DisplayName`)

---

실무에서는 테스트 메서드 이름만 보고도 내용을 알 수 있게 **한글**로 적거나, JUnit 5의 `@DisplayName`을 사용합니다.

```java
@Test
@DisplayName("VIP 회원은 1000원 고정 할인이 적용되어야 한다")
void createOrder_VIP() { ... }
```
