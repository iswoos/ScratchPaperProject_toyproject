# ScratchPaperProject
Scratch Paper 프로젝트입니다.


1. 프로젝트 설명
낙서장(Scratch Paper) 

- 자신만의 낙서를 공유하며 소통할 수 있는 플랫폼입니다.

( 게시글 작성 페이지에 그림판 기능 첨부 예정입니다.)


[Trouble shooting]


"1. Ajax 기술로 데이터 이동이 원활하지않은 상황이 발생. 이로 인해 상세페이지 구현기능이 어렵게 됨.
-> 게시물 작성할 시, 게시물 고유넘버를 DB에 저장  
-> 메인화면 HTML에 게시물 나열된 후, 이미지를 누르면 고유넘버가 서버측에 넘겨지게 하였음.
-> jinja2템플릿을 활용하여 HTML <-> 서버간 고유넘버를 넘겨 상세페이지를 구현하였음.

2. 작성페이지에서 만든 그림판이미지(canvas)를 메인페이지 img 파일로 출력할 시 데이터 전송이 안됨
-> toDataURL()로 BASE64 문자열로 이루어진 url로 치환한 뒤 jpeg 타입값 지정 높은 화질을 요하지 않는 이미지니 퀄리티는 0.5로 지정함
-> 해당 url을 DB로 보낸 뒤, 값을 가져와서 이미지 출력하였음"


[아쉬웠던 점]
1. 깃은 사용하였으나, 잔실수가 많이 발생하였음 
ex) merge conflict발생하였을 때 허둥지둥 등등.. (결국 해결못하고 수기로 합쳤다)



2. 좀 더 구현할 수 있는 기능이 있었으나, 시간의 부족함으로 인해 시현못함

ex) 좋아요 취소 기능, 좋아요한 사람들 리스트 노출 등



[개선점]
1. 깃은 사용하였으나, 잔실수가 많이 발생하였음 + 현업에서는 깃배쉬같은 터미널로 깃을 이용한다고 함.

-> 깃 배쉬를 통하여 merge conflict상황 대처법 및 사용법 알아놓자



2. 어떤 서비스를 기획할 것인지 -> 어떤 기능을 우선순위로 구현할 것인지.

중점을 확실하게 잡고 프로젝트에 임해야겠다.






2. 와이어 프레임



3. API
기능	Method	Url	Request	Response	비고	배정
로그인	POST	/login	

JWT 	조정우
회원가입	POST	/signup	id, pw	'result' :
'success'

'msg' :
회원가입 완료 


조정우
게시글 불러오기	GET	/show_post	picture	
최신 게시글부터
상단노출	송제윤
게시글 기록하기	POST	/save_post	post_num
id, title, text
picture
like_count
like_id	'result' :
'success'

'msg' :
등록 완료 	글번호  
아이디(작성자)
글제목 / 글 
그림파일
좋아요개수
좋아요한 아이디
(조회자) 리스트	이승우
게시글 좋아요	POST	/like	post_num
like_id	'result' :
'success'

'msg' :
❤️ 	post_num값으로 기존 DB내
> like_count
> like_id
2개 DB값 최신화	조정우
좋아요 리스트 확인	GET	/like_post	like_id	
시간 남으면
구현 예정 기능

DB내 likeId_give 리스트값 불러오기	이승우
그림판	



JS를 활용한 
그림판 기능 구현	송제윤

상세 페이지	GET	/view_post	post_num
id, title, text
picture
like_count
like_id	

이승우
