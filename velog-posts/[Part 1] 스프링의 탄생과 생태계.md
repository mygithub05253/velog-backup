# [Part 1] 스프링의 탄생과 생태계

**Published:** Wed, 14 Jan 2026 07:34:27 GMT
**Link:** https://velog.io/@kik328288/Part-1-%EC%8A%A4%ED%94%84%EB%A7%81%EC%9D%98-%ED%83%84%EC%83%9D%EA%B3%BC-%EC%83%9D%ED%83%9C%EA%B3%84-g184zqg3

---

<h3 id="1-스프링의-탄생-배경-자바-진영의-추운-겨울-ejb-지옥">1. 스프링의 탄생 배경: 자바 진영의 추운 겨울 (EJB 지옥)</h3>
<hr />
<p>과거(2000년대 초반) 자바 진영에는 <strong>EJB(Enterprise Java Beans)</strong>라는 기술이 표준으로 자리 잡고 있었습니다 . 이론적으로는 분산 처리 지원 등 훌륭한 기술이었지만, 실제 개발 현장에서는 큰 문제가 있었습니다.</p>
<ul>
<li><strong>EJB의 문제점:</strong><ul>
<li><strong>복잡하고 어렵다:</strong> 코드가 매우 복잡하고 EJB 스펙에 의존적이라 코드 작성이 번거로웠습니다 .</li>
<li><strong>느리고 비싸다:</strong> EJB 컨테이너를 구동하는 데 많은 시간이 걸렸고, 수천만 원에 달하는 고가의 장비가 필요했습니다 .</li>
<li><strong>객체 지향의 상실:</strong> EJB에 의존적인 코드를 짜다 보니, 자바가 가진 가장 큰 장점인 '객체 지향적 설계'가 무너졌습니다.</li>
</ul>
</li>
</ul>
<p>이 시기를 개발자들은 <strong>&quot;자바 진영의 추운 겨울(Winter)&quot;</strong>이라고 부르며, EJB 지옥에서 고통받았습니다 .</p>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/d790c81c-7c25-4631-89cd-27d676d93211/image.png" /></p>
<h3 id="2-구세주의-등장-로드-존슨과-스프링의-시작">2. 구세주의 등장: 로드 존슨과 스프링의 시작</h3>
<hr />
<p>2002년, <strong>로드 존슨(Rod Johnson)</strong>이라는 개발자가 <strong>『J2EE Design and Development』</strong>라는 책을 출간하며 전설이 시작됩니다 .</p>
<ul>
<li><strong>책의 핵심 내용:</strong><ul>
<li>EJB의 문제점을 신랄하게 비판했습니다 .</li>
<li>*&quot;EJB 없이도 충분히 고품질의 확장 가능한 애플리케이션을 개발할 수 있다&quot;**는 것을 예제 코드로 증명했습니다 .</li>
<li>이 책에 수록된 30,000라인 이상의 예제 코드에 지금의 <strong>BeanFactory, ApplicationContext, POJO, 제어의 역전(IoC), 의존관계 주입(DI)</strong> 개념이 모두 포함되어 있었습니다 .</li>
</ul>
</li>
</ul>
<p>이 책은 개발자들 사이에서 폭발적인 반응을 얻었고, 유겐 휠러(Juergen Hoeller)와 얀 카로프(Yann Caroff)가 로드 존슨에게 <strong>오픈소스 프로젝트</strong>를 제안하면서 <strong>'스프링(Spring)'</strong>이 시작되었습니다 .</p>
<ul>
<li><strong>스프링(Spring) 이름의 유래:</strong><ul>
<li>EJB라는 <strong>'겨울'</strong>을 넘어, 자바 진영에 새로운 시작인 <strong>'봄'</strong>이 왔다는 뜻입니다 .</li>
</ul>
</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/37f2a32e-2dc3-4a65-88d0-9e57718aa197/image.png" /></p>
<h3 id="3-또-다른-변화-하이버네이트와-jpa">3. 또 다른 변화: 하이버네이트와 JPA</h3>
<hr />
<p>EJB는 비즈니스 로직뿐만 아니라 데이터베이스 처리(엔티티 빈)에서도 최악이었습니다 . 이에 반발하여 <strong>개빈 킹(Gavin King)</strong>이라는 개발자가 <strong>하이버네이트(Hibernate)</strong>라는 오픈소스 기술을 만들었습니다 .</p>
<ul>
<li><strong>하이버네이트의 성공:</strong> EJB 엔티티 빈보다 훨씬 가볍고 편리하여 개발자들의 선택을 받았습니다.</li>
<li><strong>JPA 표준 탄생:</strong> 결국 자바 표준(Java Standard) 진영에서도 반성하고, 하이버네이트를 기반으로 <strong>JPA(Java Persistence API)</strong>라는 새로운 표준을 정의했습니다 .</li>
</ul>
<p><strong>[JPA와 구현체의 관계]</strong></p>
<ul>
<li><strong>JPA:</strong> 자바 표준 <strong>인터페이스</strong> (껍데기) .</li>
<li><strong>Hibernate:</strong> JPA를 실제로 동작하게 만드는 <strong>구현체</strong> (가장 많이 사용됨) .</li>
<li>기타 구현체: EclipseLink 등 .</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/a27856cc-fe8b-4331-b686-f85b9ed0e02f/image.png" /></p>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/cda31e93-59a1-4b21-9421-29ac1c4720e7/image.png" /></p>
<h3 id="4-스프링-생태계-spring-ecosystem">4. 스프링 생태계 (Spring Ecosystem)</h3>
<hr />
<p>스프링은 이제 단순한 프레임워크가 아니라 거대한 <strong>생태계</strong>입니다 .</p>
<h3 id="1-스프링-프레임워크-spring-framework">1) 스프링 프레임워크 (Spring Framework)</h3>
<hr />
<ul>
<li>생태계의 <strong>핵심</strong>입니다.</li>
<li><strong>핵심 기술:</strong> 스프링 DI 컨테이너, AOP, 이벤트 등 .</li>
<li><strong>웹 기술:</strong> 스프링 MVC, WebFlux .</li>
<li><strong>데이터 접근:</strong> 트랜잭션, JDBC, ORM, XML 지원 .</li>
<li><strong>기술 통합:</strong> 캐시, 이메일, 원격 접근, 스케줄링</li>
<li><strong>테스트</strong>: 스프링 기반 테스트 지원</li>
<li><strong>언어</strong>: 코틀린, 그루비</li>
</ul>
<h3 id="2-스프링-부트-spring-boot">2) 스프링 부트 (Spring Boot)</h3>
<hr />
<ul>
<li>최근에는 스프링 프레임워크를 편리하게 사용할 수 있도록 도와주는 <strong>스프링 부트를 기본으로 사용</strong>합니다 .</li>
<li><strong>주요 특징:</strong><ul>
<li><strong>단독 실행 가능:</strong> Tomcat 같은 웹 서버를 내장(Embedded)하여 별도 설치가 필요 없습니다 .</li>
<li><strong>쉬운 설정:</strong> 빌드 구성을 위한 Starter 종속성을 제공하고, 외부 라이브러리 버전을 자동으로 맞춰줍니다 .</li>
<li><strong>운영 편의성:</strong> 메트릭, 상태 확인 기능을 제공합니다 .<ul>
<li>메트릭, 상태 확인, 외부 구성 같은 프로덕션 준비 기능을 제공합니다.</li>
<li>관례에 의한 간결한 설정을 제공합니다.</li>
</ul>
</li>
</ul>
</li>
</ul>
<h3 id="3-스프링-프레임워크-역사">3) 스프링 프레임워크 역사</h3>
<hr />
<ul>
<li>2003년 스프링 프레임워크 1.0 출시 - XML</li>
<li>2006년 스프링 프레임워크 2.0 출시 - XML 편의 기능 지원</li>
<li>2009년 스프링 프레임워크 3.0 출시 - 자바 코드로 설정</li>
<li>2013년 스프링 프레임워크 4.0 출시 - 자바8</li>
<li>2014년 스프링 부트 1.0 출시</li>
<li>2017년 스프링 프레임워크 5.0, 스프링 부트 2.0 출시 - 리엑티브 프로그래밍 지원</li>
<li>2020년 9월 스프링 프레임워크 5.2.x, 스프링 부트 2.3.x</li>
</ul>
<h3 id="4-그-외-기술들">4) 그 외 기술들</h3>
<hr />
<ul>
<li><strong>스프링 데이터:</strong> 데이터베이스 접근(CRUD)을 편리하게 도와주는 기술 (Spring Data JPA 등) .</li>
<li><strong>스프링 세션, 스프링 시큐리티, 스프링 배치, 스프링 클라우드</strong> 등 다양한 확장 기술이 존재합니다 .</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/fcc428a5-544e-467b-abcd-9e5e3a86542b/image.png" /></p>
<h3 id="5-스프링의-진짜-핵심-the-essence-of-spring">5. 스프링의 진짜 핵심 (The Essence of Spring)</h3>
<hr />
<p>많은 개발자가 스프링을 단순히 &quot;웹 사이트를 편하게 만들어주는 도구&quot; 혹은 &quot;DB 접근을 쉽게 해주는 기술&quot; 정도로 생각합니다 . 하지만 이는 결과론적인 이야기입니다.</p>
<p><strong>스프링의 본질은 무엇일까요?</strong></p>
<ol>
<li>자바 언어의 가장 큰 특징은 <strong>'객체 지향 언어(Object Oriented Language)'</strong>라는 점입니다 .</li>
<li>스프링은 이 <strong>객체 지향 언어가 가진 강력한 특징을 살려내는 프레임워크</strong>입니다 .</li>
<li>즉, 스프링은 <strong>&quot;좋은 객체 지향 애플리케이션을 개발할 수 있게 도와주는 프레임워크&quot;</strong>입니다 .</li>
</ol>
<p>EJB 시절에는 기술의 복잡성 때문에 객체 지향의 장점을 잃어버렸지만, 스프링은 다시 <strong>'객체 지향의 본질'</strong>로 돌아가게 해주는 도구입니다. 그렇다면 <strong>'좋은 객체 지향'</strong>이란 무엇일까요? 이 내용은 다음 파트에서 자세히 다루겠습니다.</p>