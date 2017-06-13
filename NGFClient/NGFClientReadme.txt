NGF Client 자동 빌드를 위한 계획

 0. 빌드전 주의 사항
 - 자동 빌드는 python-3.6.1-amd64 +  pycharm-community-2017.1.3 환경에서 테스트 되었음
 - 모든 변경 사항이 svn에 commit 되어 있는지 확인한다.
 - 배포되야 하는 모듈은 반드시 버전 정보가 이전 인스톨러와 달라야 한다.
 - 기존에 없던 모듈 추가시 svn에 추가 해야 정상적으로 인스톨러에 포함된다.
 
 
 1. svn 정리
	1.1 "trunk\OpenManager3.2x", "trunk\OpenManager 3.2 Installer" 폴더를 REVERT 한다.
	1.2 "trunk\OpenManager3.2x", "trunk\OpenManager 3.2 Installer" 폴더를 UPDATE 한다.
	
 2. Prject Clean
	2.1 Workspaces\MainFullVersion\MainFullVersion.dsw 프로젝트를 Clean한다.
	2.2 Workspaces\MainFullVersion\MainFullVersion.dsw 프로젝트에서 mesh build를 clean한다.
	2.3 Workspaces\ModulesCommon\ModulesCommon.dsw 프로젝트를 clean한다.
 
 3. 프로젝트 컴파일
	3.1 Mesh 버전에서 사용하는 icon이 다르기 때문에 일반버전 컴파일전 icon을 복사해준다.
		- omc_main.ico -> openmanager.ico, omc_NGF.ico -> NGF.ico
	3.2 Workspaces\MainFullVersion\MainFullVersion.dsw 프로젝트를 빌드 한다.
	3.3 Workspaces\ModulesCommon\ModulesCommon.dsw 프로젝트를 빌드한다.
	
	3.4 Mesh 버전에서 사용하는 icon이 다르기 때문에 Mesh 버전 컴파일전 icon을 복사해준다.
		- mesh_main.ico -> openmanager.ico, mesh_NGF.ico -> NGF.ico
	3.5 Workspaces\MainFullVersion\MainFullVersion.dsw 프로젝트 Mesh 빌드 한다.
	
 4. 모듈의 복사 
	4.1 빌드 완료된 모듈들을 이전 모듈과 버전 정보를 비교하여 installer 프로젝트와 patch 폴더에 복사해준다.
	4.2.1 일반 버전 인스톨러 처리
		- trunk\OpenManager3.2x\OpenManager\Release\bin\*.*		-> trunk\OpenManager 3.2 Installer\SetupFile\Common\Bin\*.* 복사한다.
		- trunk\OpenManager3.2x\OpenManager\Release\modules\*.* -> trunk\OpenManager 3.2 Installer\SetupFile\Common\Modules\*.* 복사한다.
	4.2.2 일반버전 Patch 처리
		- trunk\OpenManager3.2x\OpenManager\Release\bin\*.*		-> D:\Upload\OpenManager3\release\autobuild\3.4.YYYYMMDD_HHMM\patch\NGFClient.Auth\Bin\*.* 복사한다.
		- trunk\OpenManager3.2x\OpenManager\Release\modules\*.* -> D:\Upload\OpenManager3\release\autobuild\3.4.YYYYMMDD_HHMM\patch\NGFClient.Auth\Modules\*.* 복사한다.
	
	
	4.3.1 Mesh 버전 인스톨러 처리
		- trunk\OpenManager3.2x\OpenManager\Release\bin\CloudMesh.exe	-> trunk\OpenManager 3.2 Installer\CustomSetupFile\MESH\bin\cloudmesh.exe 복사 한다.
		- trunk\OpenManager3.2x\OpenManager\Release\bin\OMUpdater.exe	-> trunk\OpenManager 3.2 Installer\CustomSetupFile\MESH\bin\OMUpdater.exe 복사 한다.
		- trunk\OpenManager3.2x\OpenManager\Release\modules\*.*			-> trunk\OpenManager 3.2 Installer\CustomSetupFile\MESH\modules*.* 복사한다.
		# Mesh module 목록
			* SendSMS.dll
			* ServerStatus.dll
			* VMCreate.dll
			* VMDataInfo.dll
			* VMManagement.dll
			* VMOperation.dll
			* VM_GuestResOp.dll
			* VM_StatusDlg.dll
			* VM_StatusDlg1.dll
			* VRInfoView.dll
	4.3.2 Mesh Patch 처리
		- trunk\OpenManager3.2x\OpenManager\Release\bin\CloudMesh.exe	-> D:\Upload\OpenManager3\release\autobuild\3.4.YYYYMMDD_HHMM\patch\MESH\bin\cloudmesh.exe 복사 한다.
		- trunk\OpenManager3.2x\OpenManager\Release\bin\OMUpdater.exe	-> D:\Upload\OpenManager3\release\autobuild\3.4.YYYYMMDD_HHMM\patch\MESH\bin\OMUpdater.exe 복사 한다.
		- trunk\OpenManager3.2x\OpenManager\Release\modules\*.*			-> D:\Upload\OpenManager3\release\autobuild\3.4.YYYYMMDD_HHMM\patch\MESH\modules*.* 복사한다.
	
	
 5. 인스톨러 생성
	5.1 아래의 ISM 파일에서 각각  <ProductVersion> node를 찾아서 오늘 날짜를 기준으로 ProductVersion을 변경한다.
		* "trunk\\OpenManager 3.2 Installer\\OpenManager 3.2.ism"
		* "trunk\\OpenManager 3.2 Installer\\CloudMesh_Lite.ism"
		* "trunk\\OpenManager 3.2 Installer\\OpenManager 3.2_IOMC.ism"
	4.2 trunk\autobuild\YYYYMMDD_HHMM\ 폴더에 installer 프로젝트를 export 한다.
	4.3 인스톨러 프로젝트를 빌드 한다.
	4.4 빌드된 인스톨러를 빌드 날짜에 맞게 파일명 변경 후 Upload 폴더에 복사한다.
	
 6. FTP 업로드
	6.1 Upload 폴더에 복사된 patch module(파일 버전이 변경되어 4번 단계에서 복사된 모듈)과 인스톨러를 WinSCP를 이용해 FTP로 복사한다.
		* OpenManager3/release/client/autobuild/3.4.YYYYMMDD_HHMM/ 에 업로드 된다.

 7. GIT 으로 백업
    7.1 "D:\svn_backup\NGF" 경로에 svn fetch를 이용하여 GIT 백업을 한다.
	
 8. 업로드 완료 후 Slack 채널에 작업 완료를 알려준다.
 
 
	