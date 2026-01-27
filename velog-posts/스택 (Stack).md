# 스택 (Stack)

**Published:** Mon, 26 Jan 2026 03:35:32 GMT
**Link:** https://velog.io/@kik328288/%EC%8A%A4%ED%83%9D-Stack

---

<h1 id="자료구조">자료구조</h1>
<ol>
<li><p>선형 자료구조</p>
<ul>
<li>리스트 (List) =&gt; array (배열)</li>
<li>스택 (Stack)</li>
<li>큐 (Queue)</li>
</ul>
</li>
<li><p>비션형 자료구조</p>
<ul>
<li><p>트리 (Tree)</p>
</li>
<li><p>그래프 (Graph)</p>
</li>
</ul>
</li>
<li><p>기타</p>
<ul>
<li>정렬 (Sort)</li>
<li>힙 (Heap)<h2 id="데이터의-분류">데이터의 분류</h2>
</li>
</ul>
</li>
</ol>
<ul>
<li>기본 타입<ul>
<li>정수 타입, 실수 타입, 불 타입</li>
</ul>
</li>
<li>참조(객체) 타입 : 객체의 주소 번지를 참조하는 타입<ul>
<li>배열 타입 : List, Array, Arrays, ArrayList</li>
<li>열거 타입 : Enum</li>
<li>클래스</li>
<li>인터페이스<h1 id="스택-stack">스택 (Stack)</h1>
</li>
</ul>
</li>
<li>정의 : 데이터를 쌓는다 =&gt; 데이터를 관리하는 방법</li>
<li>목적 : 데이터를 좀 더 찾기 쉽게 하는 것</li>
<li>특징 : FILO =&gt; 제일 먼저 들어온 데이터가 제일 나중에 나간다. (후입선출)
<img alt="" src="https://velog.velcdn.com/images/kik328288/post/3385dedc-2d62-4699-bacf-4c39f62dfe4b/image.png" /><h2 id="스택과-힙">스택과 힙</h2>
<img alt="" src="https://velog.velcdn.com/images/kik328288/post/03cf2cfb-8af1-4410-8cfd-f589c32f765d/image.png" /></li>
</ul>
<h2 id="메모리-영역">메모리 영역</h2>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/1d4cd745-f62c-4c53-9d37-9e7e11b446b8/image.png" /></p>
<h2 id="스택-구현-원리">스택 구현 원리</h2>
<ol>
<li>데이터를 삽입 =&gt; push(스택 이름, 데이터 값)</li>
<li>데이터를 삭제 =&gt; pop(스택 이름)
<img alt="" src="https://velog.velcdn.com/images/kik328288/post/ba8376c4-d2c2-4202-802f-3f5c5cdc6a4b/image.png" /></li>
</ol>
<h2 id="스택을-정적으로-구현하는-경우">스택을 정적으로 구현하는 경우</h2>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/75f81b8c-ba98-4215-8ebb-cf576438475f/image.png" /></p>
<h2 id="스택을-동적으로-구현하는-경우">스택을 동적으로 구현하는 경우</h2>
<p><img alt="" src="https://velog.velcdn.com/images/kik328288/post/ee728134-bc3c-4c24-a82e-01108c894fca/image.png" /></p>