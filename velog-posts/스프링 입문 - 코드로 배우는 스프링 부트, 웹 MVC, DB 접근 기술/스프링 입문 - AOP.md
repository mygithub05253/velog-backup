# 스프링 입문 - AOP

**Published:** 2026-01-09T08:35:28.805Z
**Link:** https://velog.io/@kik328288/스프링-입문-AOP

---

## 16. AOP (Aspect Oriented Programming)

---

**AOP(관점 지향 프로그래밍)**는 애플리케이션의 핵심 비즈니스 로직과 공통으로 사용되는 부가 기능 로직을 분리하여 모듈화하는 프로그래밍 패러다임이다.

### 16-1. AOP가 필요한 상황

---

모든 메서드의 호출 시간을 측정해야 하는 상황을 가정해보자.

#### 16-1-1. 핵심 관심 사항 vs 공통 관심 사항

- **핵심 관심 사항 (Core Concern):** 회원 가입, 회원 조회 등 비즈니스의 핵심 로직.
- **공통 관심 사항 (Cross-cutting Concern):** 시간 측정, 로그 남기기, 보안 인증 등 여러 로직에서 공통적으로 필요한 기능.

#### 16-1-2. AOP 없이 구현할 때의 문제점

```java
package hello.hello_spring.service;

import hello.hello_spring.domain.Member;
import hello.hello_spring.repository.MemberRepository;
import hello.hello_spring.repository.MemoryMemberRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class MemberService {
    private final MemberRepository memberRepository;

    @Autowired // 생성자가 1개면 생략 가능
    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    /**
     *
     회원가입
     */
    public Long join(Member member) {
        long start = System.currentTimeMillis();
        try {
            validateDuplicateMember(member); //중복 회원 검증
            memberRepository.save(member);
            return member.getId();
        }
        finally {
            long finish = System.currentTimeMillis();
            long timeMs = finish - start;
            System.out.println("join " + timeMs + "ms");
        }
    }

    private void validateDuplicateMember(Member member) {
        memberRepository.findByName(member.getName())
                .ifPresent(m -> {
                    throw new IllegalStateException("이미 존재하는 회원입니다.");
                });
    }

    /**
     *
     전체 회원 조회
     */
    public List<Member> findMembers() {
        long start = System.currentTimeMillis();
        try {
            return memberRepository.findAll();
        }
        finally {
            long finish = System.currentTimeMillis();
            long timeMs = finish - start;
            System.out.println("findMembers " + timeMs + "ms");
        }
    }
}
```

모든 메서드에 `System.currentTimeMillis()`를 사용하여 시작과 끝 시간을 측정하는 코드를 넣는다면 다음과 같은 문제가 발생한다.

1. **유지보수 어려움:** 회원 가입, 조회 등 핵심 비즈니스 로직에 시간 측정 로직이 섞여 코드가 지저분해진다.
2. **중복 코드:** 시간을 측정하는 로직이 모든 메서드에 반복된다. 별도의 공통 메서드로 뽑아내기도 어렵다.
3. **변경의 어려움:** 시간 측정 로직을 변경해야 할 때, 수백 개의 메서드를 일일이 찾아다니며 수정해야 한다.

### 16-2. AOP 적용

---

AOP를 사용하면 공통 관심 사항(시간 측정)을 별도의 로직으로 분리하여 **원하는 곳에만 적용**할 수 있다.

- 시간 측정 AOP 구현 (`TimeTraceAop`)

```java
package hello.hello_spring.aop;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect // 1. AOP 클래스임을 명시
@Component // 2. 스프링 빈으로 등록 (Config 파일에 @Bean으로 등록해도 됨)
public class TimeTraceAop {

    // 3. 공통 관심 사항을 적용할 타겟팅 (패키지 하위 모든 메서드에 적용)
    @Around("execution(* hello.hello_spring..*(..))")
    public Object execute(ProceedingJoinPoint joinPoint) throws Throwable {
        long start = System.currentTimeMillis();
        System.out.println("START: " + joinPoint.toString()); // 어떤 메서드가 호출되었는지 로그 출력

        try {
            // 4. 다음 메서드(실제 비즈니스 로직)로 진행
            return joinPoint.proceed();
        } finally {
            long finish = System.currentTimeMillis();
            long timeMs = finish - start;
            System.out.println("END: " + joinPoint.toString() + " " + timeMs + "ms");
        }
    }
}
```

### 16-3. AOP 적용의 이점

---

- 핵심 관심 사항(비즈니스 로직)과 공통 관심 사항(시간 측정)이 완벽하게 분리된다.
- 핵심 비즈니스 로직은 깔끔하게 유지된다.
- 공통 로직 변경 시 이 AOP 클래스 하나만 수정하면 된다.
- `@Around` 설정을 통해 적용 대상을 원하는 대로 선택할 수 있다.

### 16-4. AOP 동작 방식 (Proxy 패턴)

---

스프링 AOP는 **프록시(Proxy)** 기반의 AOP이다.

#### 16-4-1. 적용 전 의존 관계

컨트롤러가 서비스를 의존할 때, 실제 서비스 객체를 직접 호출한다.

![](https://velog.velcdn.com/images/kik328288/post/15a21757-0f1e-4a5a-aadc-df133cfd9f59/image.png)

- `MemberController` ➔ `MemberService`

#### 16-4-2. 적용 후 의존 관계 (프록시 주입)

AOP를 적용하면 스프링은 **가짜(프록시) 스프링 빈**을 만들어 컨테이너에 등록한다.

1. 스프링 컨테이너가 뜰 때 `@Aspect`를 보고 "어? 이 서비스에는 AOP가 걸려있네?"라고 판단한다.
2. 실제 `MemberService` 대신 **프록시(Proxy) MemberService**를 생성하여 `MemberController`에 주입(DI)해준다.
3. 프록시 객체 내부에서 `joinPoint.proceed()`가 호출될 때 실제 `MemberService`가 호출된다.

![](https://velog.velcdn.com/images/kik328288/post/97c10bca-0289-4b69-ae61-ff3772672e59/image.png)

- **설명:** AOP 적용 전에는 컨트롤러가 실제 서비스를 가리키지만, 적용 후에는 **프록시(가짜) 서비스**를 거쳐서 실제 서비스가 호출되는 흐름을 보여준다.

#### 16-4-3. 전체 구조의 변화

컨트롤러, 서비스, 리포지토리 모든 계층에 AOP를 적용하면, 모든 구간 사이에 프록시가 끼어들어 동작한다.

- `Controller` ➔ **Proxy** ➔ `Service` ➔ **Proxy** ➔ `Repository`

![](https://velog.velcdn.com/images/kik328288/post/37c5b62c-dc40-434e-8bc5-14149f74211d/image.png)

- **설명:** 스프링 컨테이너 내에서 각 컴포넌트 앞에 프록시 객체가 생성되어 연결된 전체적인 구조도이다 .

### 16-5 AOP 적용 확인 방법

---

실제 코드로 프록시가 주입되었는지 확인해 볼 수 있다.

```java
// MemberController 생성자나 메서드에서 찍어봄
System.out.println("memberService = " + memberService.getClass());
```

결과를 보면 순수한 `MemberService`가 아니라 `MemberService$$EnhancerBySpringCGLIB...` 과 같이 복잡한 이름의 클래스(프록시)가 출력된다.

