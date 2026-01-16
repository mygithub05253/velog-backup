# [Part 5] 프로젝트 생성 및 환경 설정

**Published:** Thu, 15 Jan 2026 09:16:22 GMT
**Link:** https://velog.io/@kik328288/Part-5-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EC%83%9D%EC%84%B1-%EB%B0%8F-%ED%99%98%EA%B2%BD-%EC%84%A4%EC%A0%95

---

<h2 id="1-스프링-부트-프로젝트-생성-startspringio">1. 스프링 부트 프로젝트 생성 (start.spring.io)</h2>
<hr />
<p>스프링 부트 기반의 프로젝트를 만들어주는 공식 사이트인 <strong>Spring Initializr</strong>를 사용합니다.</p>
<ul>
<li><strong>사이트 접속:</strong> <a href="https://start.spring.io/">https://start.spring.io</a></li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/fe5b977c-067d-4e1c-b335-4aa25cf81e70/image.png" /></p>
<ul>
<li><strong>프로젝트 설정 값 (필수):</strong><ul>
<li><strong>Project:</strong> Gradle - Groovy</li>
<li><strong>Language:</strong> Java</li>
<li><strong>Spring Boot:</strong> 4.x.x (SNAPSHOT이나 M1이 아닌 정식 버전을 선택하세요)</li>
<li><strong>Project Metadata:</strong><ul>
<li>Group: <code>hello</code></li>
<li>Artifact: <code>core</code></li>
<li>Packaging: <strong>Jar</strong> (Tomcat 내장)</li>
<li>Java: <strong>17</strong> 또는 <strong>21</strong> (스프링 부트 3.0부터는 Java 17 이상이 필수입니다)</li>
</ul>
</li>
<li><strong>Dependencies:</strong> <strong>아무것도 선택하지 않습니다.</strong> (이번 예제는 순수 자바 코드로 진행하기 위함입니다)</li>
</ul>
</li>
</ul>
<h2 id="2-intellij-gradle-설정-실행-속도-및-호환성">2. IntelliJ Gradle 설정 (실행 속도 및 호환성)</h2>
<hr />
<p>프로젝트를 IntelliJ로 오픈한 후, 빌드 및 실행 설정을 확인해야 합니다. 여기서 <strong>버전에 따른 중요한 차이</strong>가 있습니다.</p>
<h3 id="⚠️-스프링-부트-32-이상-사용-시-주의사항">⚠️ 스프링 부트 3.2 이상 사용 시 주의사항</h3>
<hr />
<p>최신 버전(3.2 이상)을 사용하신다면, 반드시 <strong>Gradle</strong>을 통해 빌드하도록 설정해야 합니다.</p>
<ul>
<li><strong>설정 위치:</strong> <code>Settings/Preferences</code> $\rightarrow$ <code>Build, Execution, Deployment</code> $\rightarrow$ <code>Build Tools</code> $\rightarrow$ <code>Gradle</code></li>
<li><strong>설정 변경:</strong><ul>
<li>Build and run using: <strong>Gradle</strong> (권장)</li>
<li>Run tests using: <strong>Gradle</strong> (권장)</li>
<li>Gradle JVM: <strong>Java 17</strong> 이상 선택</li>
</ul>
</li>
</ul>
<blockquote>
<p>왜 IntelliJ IDEA 빌더가 아닌 Gradle을 써야 하나요?
스프링 부트 3.2(스프링 프레임워크 6.x)부터는 자바 컴파일 시 -parameters 옵션이 필수입니다. Gradle 플러그인은 이를 자동으로 처리해주지만, IntelliJ Native Builder는 별도 설정 없이는 이 옵션을 누락하여 파라미터 이름을 인식 못 하는 오류가 발생할 수 있습니다.</p>
</blockquote>
<h2 id="3-buildgradle-확인">3. <code>build.gradle</code> 확인</h2>
<hr />
<p>생성된 프로젝트의 <code>build.gradle</code> 파일이 아래와 같은지 확인합니다.</p>
<pre><code class="language-java">plugins {
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
        exclude group: &quot;org.junit.vintage&quot;, module: &quot;junit-vintage-engine&quot;
    }
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

tasks.named('test') {
    useJUnitPlatform()
}
</code></pre>
<h2 id="4-참고-자료">4. 참고 자료</h2>
<hr />
<p>단순히 따라 하는 것을 넘어, 실무 지식을 쌓을 수 있는 참고 자료입니다.</p>
<ol>
<li><strong>Spring Boot 3.0 릴리즈 노트 (공식):</strong><ul>
<li><strong>내용:</strong> 왜 Java 17이 필수가 되었는지, <code>javax</code> 패키지가 왜 <code>jakarta</code>로 바뀌었는지(Java EE $\rightarrow$ Jakarta EE 이관 이슈)에 대한 공식 설명입니다.</li>
<li><strong>링크:</strong> <a href="https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Release-Notes">Spring Boot 3.0 Release Notes</a></li>
</ul>
</li>
<li><strong><code>javax</code> vs <code>jakarta</code> 마이그레이션 이슈:</strong><ul>
<li><strong>내용:</strong> 스프링 부트 3.0 이상을 쓸 때 가장 많이 겪는 에러인 <code>ClassNotFoundException: javax.servlet...</code> 등의 원인을 파악할 수 있습니다.</li>
<li><strong>핵심:</strong> <code>import javax.persistence.*</code> $\rightarrow$ <code>import jakarta.persistence.*</code> 로 변경해야 합니다.</li>
<li><strong>참고:</strong> <a href="https://ai-coding-mom.tistory.com/13">Spring Boot 3.x 마이그레이션 가이드 (티스토리)</a></li>
</ul>
</li>
<li><strong>Gradle vs IntelliJ 빌드 차이점:</strong><ul>
<li><strong>내용:</strong> 과거에는 IntelliJ 빌더가 빨라서 선호되었으나, 최근 버전 호환성 문제로 Gradle 빌드가 다시 권장되는 이유에 대한 심층 토론입니다.</li>
<li><strong>참고:</strong> <a href="https://www.google.com/search?q=https://www.inflearn.com/community/questions/1482281">인프런 커뮤니티: Spring Boot 3.2 파라미터 추론 관련 이슈</a></li>
</ul>
</li>
</ol>