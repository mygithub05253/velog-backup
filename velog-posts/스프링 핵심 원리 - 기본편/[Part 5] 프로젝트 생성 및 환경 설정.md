# [Part 5] 프로젝트 생성 및 환경 설정

**Published:** 2026-01-15T09:16:22.829Z
**Link:** https://velog.io/@kik328288/Part-5-프로젝트-생성-및-환경-설정

---

## 1. 스프링 부트 프로젝트 생성 (start.spring.io)

---

스프링 부트 기반의 프로젝트를 만들어주는 공식 사이트인 **Spring Initializr**를 사용합니다.

- **사이트 접속:** [https://start.spring.io](https://start.spring.io/)

![](https://velog.velcdn.com/images/kik328288/post/fe5b977c-067d-4e1c-b335-4aa25cf81e70/image.png)

- **프로젝트 설정 값 (필수):**
    - **Project:** Gradle - Groovy
    - **Language:** Java
    - **Spring Boot:** 4.x.x (SNAPSHOT이나 M1이 아닌 정식 버전을 선택하세요)
    - **Project Metadata:**
        - Group: `hello`
        - Artifact: `core`
        - Packaging: **Jar** (Tomcat 내장)
        - Java: **17** 또는 **21** (스프링 부트 3.0부터는 Java 17 이상이 필수입니다)
    - **Dependencies:** **아무것도 선택하지 않습니다.** (이번 예제는 순수 자바 코드로 진행하기 위함입니다)

## 2. IntelliJ Gradle 설정 (실행 속도 및 호환성)

---

프로젝트를 IntelliJ로 오픈한 후, 빌드 및 실행 설정을 확인해야 합니다. 여기서 **버전에 따른 중요한 차이**가 있습니다.

### ⚠️ 스프링 부트 3.2 이상 사용 시 주의사항

---

최신 버전(3.2 이상)을 사용하신다면, 반드시 **Gradle**을 통해 빌드하도록 설정해야 합니다.

- **설정 위치:** `Settings/Preferences` $\rightarrow$ `Build, Execution, Deployment` $\rightarrow$ `Build Tools` $\rightarrow$ `Gradle`
- **설정 변경:**
    - Build and run using: **Gradle** (권장)
    - Run tests using: **Gradle** (권장)
    - Gradle JVM: **Java 17** 이상 선택

> 왜 IntelliJ IDEA 빌더가 아닌 Gradle을 써야 하나요?
스프링 부트 3.2(스프링 프레임워크 6.x)부터는 자바 컴파일 시 -parameters 옵션이 필수입니다. Gradle 플러그인은 이를 자동으로 처리해주지만, IntelliJ Native Builder는 별도 설정 없이는 이 옵션을 누락하여 파라미터 이름을 인식 못 하는 오류가 발생할 수 있습니다.
> 

## 3. `build.gradle` 확인

---

생성된 프로젝트의 `build.gradle` 파일이 아래와 같은지 확인합니다.

```java
plugins {
	id 'java'
	id 'org.springframework.boot' version '4.0.1'
	id 'io.spring.dependency-management' version '1.1.7'
}

group = 'hello'
version = '0.0.1-SNAPSHOT'
description = 'Demo project for Spring Boot'

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(21)
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation 'org.springframework.boot:spring-boot-starter'
	testImplementation ('org.springframework.boot:spring-boot-starter-test') {
		exclude group: "org.junit.vintage", module: "junit-vintage-engine"
	}
	testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

tasks.named('test') {
	useJUnitPlatform()
}

```

## 4. 참고 자료

---

단순히 따라 하는 것을 넘어, 실무 지식을 쌓을 수 있는 참고 자료입니다.

1. **Spring Boot 3.0 릴리즈 노트 (공식):**
    - **내용:** 왜 Java 17이 필수가 되었는지, `javax` 패키지가 왜 `jakarta`로 바뀌었는지(Java EE $\rightarrow$ Jakarta EE 이관 이슈)에 대한 공식 설명입니다.
    - **링크:** [Spring Boot 3.0 Release Notes](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes)
2. **`javax` vs `jakarta` 마이그레이션 이슈:**
    - **내용:** 스프링 부트 3.0 이상을 쓸 때 가장 많이 겪는 에러인 `ClassNotFoundException: javax.servlet...` 등의 원인을 파악할 수 있습니다.
    - **핵심:** `import javax.persistence.*` $\rightarrow$ `import jakarta.persistence.*` 로 변경해야 합니다.
    - **참고:** [Spring Boot 3.x 마이그레이션 가이드 (티스토리)](https://ai-coding-mom.tistory.com/13)
3. **Gradle vs IntelliJ 빌드 차이점:**
    - **내용:** 과거에는 IntelliJ 빌더가 빨라서 선호되었으나, 최근 버전 호환성 문제로 Gradle 빌드가 다시 권장되는 이유에 대한 심층 토론입니다.
    - **참고:** [인프런 커뮤니티: Spring Boot 3.2 파라미터 추론 관련 이슈](https://www.google.com/search?q=https://www.inflearn.com/community/questions/1482281)

