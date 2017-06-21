@echo off
setlocal

@set project=EMPTY

:redo
echo.
echo =========================================
echo NGF Client Auto Build
echo =========================================
set /p type= 0(exit), 1(NGF Build ), 2(DOF Build ), 3(Agent Build)

echo 선택한 빌드 타입은 : %type%

if %type%== 0 goto QUIT
if %type%== 1 goto ngf_build
if %type%== 2 goto dof_build
if %type%== 3 goto agent_build

echo 잘못된 선택입니다. 

goto redo


:ngf_build

echo.
echo =========================================
echo NGF Client 프로젝트를 build 합니다. 
echo 소스 수정이 발생한 모듈만 변경되어 인스톨러를 작성하고, FTP에 업로드 합니다.
echo 작업 완료 후 슬랙으로 완료 메시지가 나갑니다.
echo =========================================
call python NGFAutobuildMain.py
set project=NGF

goto confirm_commit

:dof_build

echo.
echo =========================================
echo DOF Client 프로젝트를 build 합니다. 
echo 소스 수정이 발생한 모듈만 변경되어 인스톨러를 작성하고, FTP에 업로드 합니다.
echo 작업 완료 후 슬랙으로 완료 메시지가 나갑니다.
echo =========================================
call python DOFAutobuildMain.py
set project=DOF

goto confirm_commit

:agent_build
echo.
echo =========================================
echo OMAGENT 프로젝트를 build 합니다. 
echo 소스 수정이 발생한 모듈만 변경되어 인스톨러를 작성하고, FTP에 업로드 합니다.
echo 작업 완료 후 슬랙으로 완료 메시지가 나갑니다.
echo =========================================
call python AgentAutoBuildMain.py
set project=AGENT

goto confirm_commit

:confirm_commit
echo.
echo =========================================
echo 빌드가 완료 되었습니다. SVN에 커밋 하시겠습니까?
echo =========================================
set /p commit= y(commit), n(continue)

if %commit%== y call python autocommit.py %project%

goto redo



:QUIT
PAUSE
