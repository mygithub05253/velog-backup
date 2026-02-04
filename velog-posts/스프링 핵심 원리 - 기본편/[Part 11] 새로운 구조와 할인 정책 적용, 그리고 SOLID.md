# [Part 11] 새로운 구조와 할인 정책 적용, 그리고 SOLID

**Published:** 2026-02-03T04:55:47.801Z
**Link:** https://velog.io/@kik328288/Part-11-새로운-구조와-할인-정책-적용-그리고-SOLID

---

### 1. 사용 영역과 구성 영역의 분리

---

`AppConfig`의 등장으로 애플리케이션의 구조가 완전히 달라졌습니다.

- **사용 영역 (Usage):** 실제 비즈니스 로직이 실행되는 곳 (`OrderServiceImpl` 등).
- **구성 영역 (Configuration):** 객체를 생성하고 연결(조립)하는 곳 (`AppConfig`).

![](https://velog.velcdn.com/images/kik328288/post/6a50d500-348d-4003-8485-b7b08084293b/image.png)

### 2. 새로운 할인 정책 적용 (정액 $\rightarrow$ 정률)

---

이제 처음의 문제로 돌아가 봅시다. 기획자가 **"고정 할인(Fix) 말고 정률 할인(Rate)으로 바꿔주세요"**라고 했을 때, 예전에는 클라이언트 코드(`OrderServiceImpl`)를 고쳐야 했습니다.
지금은 어떨까요? **구성 영역인 `AppConfig`만 수정**하면 됩니다.

`AppConfig.java` (변경 전후 비교)

```java
public class AppConfig {

    // ... (생략) ...

    public DiscountPolicy discountPolicy() {
        // [변경 전] 정액 할인 정책
        // return new FixDiscountPolicy();
        
        // [변경 후] 정률 할인 정책 (여기만 고치면 끝!)
        return new RateDiscountPolicy();
    }
}
```

**✅ 결과:**

- `AppConfig`의 코드 **딱 한 줄**만 변경했습니다.
- **중요:** 클라이언트 코드인 `OrderServiceImpl`을 포함해서 **사용 영역의 어떤 코드도 변경할 필요가 없습니다.**
- `OrderServiceImpl`은 여전히 `DiscountPolicy` 인터페이스만 바라보고 있으며, `AppConfig`가 알아서 `RateDiscountPolicy` 객체를 생성해서 넣어줍니다.

![](https://velog.velcdn.com/images/kik328288/post/a1f19559-59c2-4118-a093-2a74d8709147/image.png)

### 3. 좋은 객체 지향 설계의 3가지 원칙 적용 (SOLID)

---

우리는 지금까지의 리팩터링 과정을 통해 **SOLID 원칙 중 3가지**를 완벽하게 지켜냈습니다. 면접이나 기술 문서 작성 시 이 논리를 그대로 사용하시면 좋습니다.

### 1) SRP: 단일 책임 원칙 (Single Responsibility Principle)

---

**"한 클래스는 하나의 책임만 가져야 한다."**

- **기존:** 클라이언트 객체(`OrderServiceImpl`)가 **'실행'**도 하고 **'구현 객체 생성/연결'**도 했습니다. 책임이 과했습니다.
- **변경 후:**
    - **AppConfig:** 구현 객체를 생성하고 연결하는 **'구성'** 책임 담당.
    - **클라이언트:** 본연의 기능인 **'실행'** 책임만 담당.
    - 관심사가 확실하게 분리되었습니다.

### 2) DIP: 의존관계 역전 원칙 (Dependency Inversion Principle)

---

**"추상화에 의존해야지, 구체화에 의존하면 안 된다."**

- **기존:** 클라이언트(`OrderServiceImpl`)가 인터페이스(`DiscountPolicy`)뿐만 아니라 구체 클래스(`FixDiscountPolicy`)에도 의존했습니다 (`new Fix...`).
- **변경 후:**
    - 클라이언트 코드에서 `new`를 지우고 인터페이스만 남겼습니다.
    - 하지만 실행하려면 구현체가 필요하죠?
    - `AppConfig`가 객체 인스턴스를 대신 생성해서 클라이언트 코드에 **의존관계 주입(DI)**을 해주었습니다.
    - 결국 클라이언트는 **인터페이스에만 의존**하게 되어 DIP를 만족했습니다.

### 3) OCP: 개방-폐쇄 원칙 (Open/Closed Principle)

---

**"확장에는 열려 있으나 변경에는 닫혀 있어야 한다."**

- **확장(Open):** 새로운 할인 정책(`RateDiscountPolicy`)을 개발해서 적용하는 것(기능 확장)은 자유롭습니다.
- **변경(Closed):** 기능을 확장해도 **사용 영역(클라이언트 코드)은 변경할 필요가 없습니다.**
- **비결:** 다형성을 사용하고, `AppConfig`가 의존관계를 대신 주입해 주었기 때문입니다. 소프트웨어 요소를 새롭게 확장해도 사용 영역의 변경은 닫혀 있습니다.
