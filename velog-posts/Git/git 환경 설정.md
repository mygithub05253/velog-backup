# git 환경 설정

**Published:** 2025-09-21T06:40:03.601Z
**Link:** https://velog.io/@kik328288/git-환경-설정

---

1. Git 파일 다운로드
https://git-scm.com/downloads
<img src="https://velog.velcdn.com/images/kik328288/post/a35c791e-d03b-456b-bdd9-bd570f8c8d6c/image.png" width="50%" align="left">
<img src="https://velog.velcdn.com/images/kik328288/post/5d60f5c5-ced0-4432-b2dc-f31385282875/image.png" width="50%" align="right">
---
- 사이트에 접속해서 운영체제에 맞는 아이콘 클릭
- Standalone Installer : 실행 파일 다운로드
- Portable : 무설치 버전 파일 => exe 파일이 아닌 7z 압축 파일 설치
2. Git  설치 파일 실행
![](https://velog.velcdn.com/images/kik328288/post/6a01ce06-0a39-453f-beef-2d376699b31c/image.png)
![](https://velog.velcdn.com/images/kik328288/post/502afc45-46b3-42d4-b2fa-a7db9fab29d4/image.png)
![](https://velog.velcdn.com/images/kik328288/post/1d848ca3-e52d-4a52-8716-8ac3a7ee3fd6/image.png)
- 기본적인 것만 설치하고 추가 파일은 설치하지 않음
- 설치 파일 종류
  - Additional icons
    - On the Desktop : 바탕화면에 바로가기 아이콘 생성
  - Windows Explorer integration
    - Git Bash Here : 폴더에서 바로 Git에 접속하는 Git Bash Here 추가
    - Git GUI Here : 폴더에서 바로 Git GUI로 접속하는 Git GUI Here 추가
  - Git LFS (Large File Support) : 대용량 파일 지원
  - Associate .git* configuration files with the default text editor : .git* 구성 파일을 기본 텍스트 편집기와 연결
  - Associate .sh files to be run with Bash : 실행할 .sh 파일을 Bash와 연결
  - Check daily for git for Windows updates : 윈도우 업데이트에 대한 새로운 업데이트 매일 확인
  - (NEW!) Add a Git Bash Profile to Windows Terminal : 윈도우 터미널에 Git Bash 프로파일 추가
---

![](https://velog.velcdn.com/images/kik328288/post/8fa19db1-e488-408a-82be-af622898fe19/image.png)
<div style="text-align: center"><span>Git이 시작될 시작 메뉴 폴더 선택</span></div>

---
![](https://velog.velcdn.com/images/kik328288/post/a268566b-cba1-4fc5-9f88-4a689facd1f0/image.png)
<div style="text-align: center"><span>Git을 사용할 기본 에디터 선택 (Vim, Visual Studio 등)</span></div>

---
![](https://velog.velcdn.com/images/kik328288/post/dc519138-f00a-4f10-b049-1c4db1b45336/image.png)
<div style="text-align: center"><span>Let Git decide : git이 기본 분기 이름(master) 사용</span></div>
<div style="text-align: center"><span>Override the default branch name for new repositories : 새 레포지토리의 기본 분기 이름 재정의</span></div>

---
![](https://velog.velcdn.com/images/kik328288/post/e32c4270-08f0-414d-ac6a-10296d608782/image.png)
- PATH 환경 조정 설정
  - Use Git from git bash only : Git bash의 Git만 이용
  - Git from the command line and also frm 3rd-party software : 명령줄에서 Git 및 타사 소프트웨어에서도 Git 제공
  - Use git and optional unix tools from the command prompt : 명령 프롬프트에서 git 및 선택적 유닉스 도구 사용
---
![](https://velog.velcdn.com/images/kik328288/post/891e30bb-ba7c-40ab-b732-cd2bf3666d50/image.png)
- ssh 실행 도구 선택
  - Use bundled openssh : Git에서 제공되는 opensh 번들 사용
  - Use external openssh : 외부 opensh 사용
---
![](https://velog.velcdn.com/images/kik328288/post/61908934-b162-4ab9-a6a2-2f49cb3dd005/image.png)
- Http 연결 설정
  - Use the OpenSSL library : OpenSSL 라이브러리 사용
  - Use the native Windows Secure Channel library
    - 기본 Windows 보안 채널 라이브러리 사용
    - Windows 인증서 저장소를 사용하여 검증
---
![](https://velog.velcdn.com/images/kik328288/post/e5401fc9-d94a-4cc0-a54d-1c0c3d388c22/image.png)
- 줄 바꿈 옵션 선택
  - Checkout Windows-style, commit Unix-style line endings
    - Git이 저장소에서 파일을 체크아웃할 때, Windows 스타일의 줄 바꿈 문자(CRLF)를 Unix 스타일의 줄 바꿈 문자(LF)로 자동 변환
    - Git이 커밋할 때, Unix 스타일의 줄 바꿈 문자(LF)를 사용하여 커밋
  - Checkout as-is, commit Unix-style line endings
    - Git이 체크아웃할 때 줄바꿈 문자를 변환하지 않음
    - Git이 커밋할 때 Unix 스타일의 줄 바꿈 문자(LF)를 사용하여 커밋
  - Checkout as-is, commit as-is
    - Git이 체크아웃할 때 줄 바꿈 문자를 변환하지 않음
    - Git이 커밋할 때 줄 바꿈 문자 그대로 커밋
- 이 옵션은 저장소에서 이미 다른 줄 바꿈 문자 처리 방식
- 커밋된 파일들이 함께 있을 때, 파일의 줄 바꿈 문자를 변경하지 않고 그대로 유지하고자 할 때 사용
---
![](https://velog.velcdn.com/images/kik328288/post/3499f29b-45e6-4040-85f6-bbc549187ff4/image.png)
- Use MinTTY (the default terminal of MSYS2)
  - Git Bash를 실행할 때, MSYS2 프로젝트에서 개발한 MinTTY 터미널 애뮬레이터 사용
  - MinTTY는 리눅스와 유사한 터미널 환경 제공
- Use Windows' default console window : Git Bash를 실행할 때, 윈도우 기본 콘솔 창 사용
---
![](https://velog.velcdn.com/images/kik328288/post/ccfb024f-613b-4f79-af18-29e2654cfaa2/image.png)
- git pull의 기본 동작 선택
- git pull : 원격 저장소에서 변경 사항을 가져와 로컬 브랜치에 병합하는 명령어
- 종류
  - Default(fast-forward or merge) : fast-forward가 가능한 경우, fast-forward 병합 수행하고 그렇지 않은 경우 merge 병합 수행
  - Rebase : 'git pull --rebase'를 실행할 때, Git은 원격 저장소에서 변경 사항을 가져온 후 로컬 브랜치의 이력을 원격 브랜치의 이력 위에 쌓아 올리는 작업 수행
  - Only ever fast-forward
    - 'git pull --ff-only' 실행할 때, Git은 fast-forward 가능한 경우에만 fast-forward 병합 수행
    - 그렇지 않은 경우, 병합 수행하지 않고 오류 발생
- fast-forward : Git에서 브랜치 병합을 수행할 때, 브랜치 이력을 간단히 이동시키는 방법
- merge : 두 개 이상의 브랜치를 병합하는 작업
---
![](https://velog.velcdn.com/images/kik328288/post/de3a300a-372e-4357-96a3-0a04fe6610ba/image.png)
- Git을 사용할 때 인증 정보를 관리하는 도구인 자격 증명 도우미 선택
  - Git Credential Manager
    - 자격 증명 도우미 사용
    - 인증 정보를 한 번 입력하면 그 이후로 자동으로 인증 정보를 사용해 Git 저장소에 접근
  - None
    - 자격 증명 도우미 사용 x
    - Git에서 인증 정보를 입력할 때마다 매번 사용자 이름과 비밀번호 입력
---
![](https://velog.velcdn.com/images/kik328288/post/04ef8652-1286-4834-aaf8-8320a9854dce/image.png)
- 추가적인 옵션 선택
  - Enable file system caching
    - Git이 파일 시스템 캐시를 사용하는 옵션
    - Git이 파일을 읽고 쓰는 속도가 더 향상
  - Enable symbolic links
    - Git이 심볼릭 링크를 지원하는 옵션
    - 심볼릭 링크는 파일이나 디렉토리를 가리키는 포인터
    - 사용하지 않으면 Git이 심볼릭 링크를 저장소에 저장하지 않고 대신 링크 대상 파일의 내용 저장
    - 링크 대상 파일이 변경되었을 때 Git에서 적절하게 대처할 수 없으므로 심볼릭 링크를 사용하는 경우 이 옵션 활성화
---
![](https://velog.velcdn.com/images/kik328288/post/1fa29b1f-0615-46f3-a5ae-74ccd09f1b17/image.png)

---
3. Git Bash 실행화면
![](https://velog.velcdn.com/images/kik328288/post/d78917d8-e1c3-4c7c-8cb2-78362d5263dd/image.png)

