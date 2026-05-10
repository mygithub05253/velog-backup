# [Part 3] 좋은 객체 지향 설계의 5가지 원칙 (SOLID)

**Published:** 2026-01-14T07:35:40.119Z
**Link:** https://velog.io/@kik328288/Part-3-좋은-객체-지향-설계의-5가지-원칙-SOLID

---


## 1. SOLID란 무엇인가?

---

SOLID는 클린코드로 유명한 로버트 마틴이 설계한 원칙으로 다음 5가지 원칙의 앞 글자를 따서 만든 단어입니다.

1. **SRP:** 단일 책임 원칙 (Single Responsibility Principle)
2. **OCP:** 개방-폐쇄 원칙 (Open/Closed Principle)
3. **LSP:** 리스코프 치환 원칙 (Liskov Substitution Principle)
4. **ISP:** 인터페이스 분리 원칙 (Interface Segregation Principle)
5. **DIP:** 의존관계 역전 원칙 (Dependency Inversion Principle)

## 2. 각 원칙 상세 정리

---

### 1) SRP: 단일 책임 원칙 (Single Responsibility Principle)

---

- **정의:** 한 클래스는 하나의 책임만 가져야 합니다 .
- **핵심 기준:** '책임'이라는 단어는 모호할 수 있습니다. 중요한 판단 기준은 **'변경'**입니다 .
    - 변경이 있을 때 파급 효과가 적으면 단일 책임 원칙을 잘 따른 것입니다.
    - 예) UI를 변경하는데 비즈니스 로직(SQL 등)까지 고쳐야 한다면 SRP 위반입니다.

### 2) OCP: 개방-폐쇄 원칙 (Open/Closed Principle) ⭐ **(가장 중요)**

---

- **정의:** 소프트웨어 요소는 **확장에는 열려** 있으나 **변경에는 닫혀** 있어야 합니다 .
- **의문:** "기능을 확장하려면 당연히 코드를 변경해야 하는 것 아닌가?"
- **해결책:** **다형성(Polymorphism)**을 활용합니다 . 인터페이스를 구현한 새로운 클래스를 하나 만들어서 새로운 기능을 구현하면, 기존 코드를 변경하지 않고 확장할 수 있습니다 .

**⚠️ OCP의 문제점 (순수 자바의 한계)**
아래 코드를 보면, 다형성을 사용했음에도 불구하고 OCP가 깨지는 것을 볼 수 있습니다.

```java
public class MemberService {
    // 기존 코드
    // private MemberRepository memberRepository = new MemoryMemberRepository();
    
    // 변경 코드 (구현체를 변경하려면 클라이언트 코드를 직접 수정해야 함!)
    private MemberRepository memberRepository = new JdbcMemberRepository();
}
```

- 구현 객체를 변경하려면 **클라이언트(`MemberService`) 코드를 변경**해야 합니다 .
- 분명 다형성을 사용했지만 **OCP 원칙을 지킬 수 없습니다** .
- 이 문제를 해결하려면 객체를 생성하고 연관관계를 맺어주는 별도의 **조립, 설정자(Spring Container)**가 필요합니다 .

### 3) LSP: 리스코프 치환 원칙 (Liskov Substitution Principle)

---

- **정의:** 프로그램의 객체는 프로그램의 정확성을 깨뜨리지 않으면서 하위 타입의 인스턴스로 바꿀 수 있어야 합니다 .
- **핵심:** 단순히 컴파일에 성공하는 것을 넘어서는 이야기입니다. **'인터페이스의 규약'**을 지켜야 한다는 뜻입니다 .
- **예시:** 자동차 인터페이스의 '엑셀' 기능은 앞으로 가라는 기능입니다. 만약 뒤로 가게 구현한다면 컴파일은 되더라도 LSP 위반입니다 .

### 4) ISP: 인터페이스 분리 원칙 (Interface Segregation Principle)

---

- **정의:** 특정 클라이언트를 위한 인터페이스 여러 개가 범용 인터페이스 하나보다 낫습니다 .
- **예시:**
    - 자동차 인터페이스 $\rightarrow$ 운전 인터페이스, 정비 인터페이스로 분리 .
    - 사용자 클라이언트 $\rightarrow$ 운전자 클라이언트, 정비사 클라이언트로 분리 .
- **장점:** 인터페이스가 명확해지고, 대체 가능성이 높아집니다 .

### 5) DIP: 의존관계 역전 원칙 (Dependency Inversion Principle) ⭐ **(가장 중요)**

---

- **정의:** 프로그래머는 **"추상화에 의존해야지, 구체화에 의존하면 안 된다"** .
- **쉬운 설명:** 구현 클래스(구현)에 의존하지 말고, **인터페이스(역할)에 의존**하라는 뜻입니다 .

**⚠️ DIP 위반 (순수 자바의 한계)**
앞서 본 OCP 문제 코드를 다시 보면 DIP도 위반하고 있습니다.

```java
// MemberService는 인터페이스(MemberRepository)에도 의존하지만,
// 구현 클래스(MemoryMemberRepository)에도 동시에 의존한다.
MemberRepository m = new MemoryMemberRepository();
```

- `MemberService`가 구현 클래스를 직접 선택하고 있습니다 (`new ...`) .
- 이는 **DIP 위반**입니다 .

## 3. 정리: 객체 지향의 핵심과 한계

---

- 객체 지향의 핵심은 **다형성(Polymorphism)**입니다 .
- 하지만 다형성만으로는 구현 객체를 변경할 때 클라이언트 코드도 함께 변경됩니다 .
- 즉, **다형성만으로는 OCP, DIP를 지킬 수 없습니다** .
- **뭔가 더 필요합니다.** (그것이 바로 **Spring**입니다!) .
