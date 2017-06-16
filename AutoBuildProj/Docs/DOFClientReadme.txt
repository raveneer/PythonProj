DOF Client 자동 빌드를 위한 계획

 0. 빌드전 주의 사항
 - 자동 빌드는 python-3.6.1-amd64 +  pycharm-community-2017.1.3 환경에서 테스트 되었음
 - 모든 변경 사항이 svn에 commit 되어 있는지 확인한다.
 - 배포되야 하는 모듈은 반드시 버전 정보가 이전 인스톨러와 달라야 한다.
 - 기존에 없던 모듈 추가시 svn에 추가 해야 정상적으로 인스톨러에 포함된다.
 
 
 1. svn 정리
	1.1 "trunk\OpenManager_DOF", "trunk\OpenManager 5.0 Installer" 폴더를 REVERT 한다.
	1.2 "trunk\OpenManager_DOF", "trunk\OpenManager 5.0 Installer" 폴더를 UPDATE 한다.
  
 2. 프로젝트 컴파일
	2.1 프로젝트를 순서대로 Rebuild All 한다.
		* VS2008에서는 Rebuile 옵션이 있기 때문에 NGF와 다르게 Clean 단계가 필요 없다.
	2.2 Common version을 Release 모드로 컴파일 한다.
		* trunk\OpenManager_DOF\OpenManager\Workspaces\MainFullVersion\MainFullVersion.sln
		* trunk\OpenManager_DOF\OpenManager\Workspaces\ModulesCommon\ModulesCommon.sln
	2.3 Anycatcher Version을 Release_AnyCatcher 모드로 컴파일 한다.
		* trunk\OpenManager_DOF\OpenManager\Workspaces\MainFullVersion\AnyCatcher.sln
	2.4 BTV Version을 Release_BTV 모드로 컴파일 한다.
		* trunk\OpenManager_DOF\OpenManager\Modules\Custom\BTV\BTV_full.sln
	
 3. 모듈의 복사 
	3.1 빌드 완료된 모듈들을 이전 모듈과 버전 정보를 비교하여 installer 프로젝트와 patch 폴더에 복사해준다.
	3.2.1 일반 버전 인스톨러 처리
		- trunk\OpenManager_DOF\OpenManager\Release\bin\*.exe | *.dll | *.ocx	-> trunk\OpenManager 5.0 Installer\SetupFile\Common\Bin\*.* 복사한다.
		- trunk\OpenManager_DOF\OpenManager\Release\modules\*.dll				-> trunk\OpenManager 5.0 Installer\SetupFile\Common\Modules\*.* 복사한다.
	3.2.2 일반버전 Patch 처리
		- trunk\OpenManager_DOF\OpenManager\Release\bin\*.exe | *.dll | *.ocx	-> D:\Upload\OpenManager5\release\autobuild\5.0.YYYYMMDD_HHMM\Patch\DOFClient\bin
		- trunk\OpenManager_DOF\OpenManager\Release\modules\*.dll				-> D:\Upload\OpenManager5\release\autobuild\5.0.YYYYMMDD_HHMM\Patch\DOFClient\Modules
	
	3.3.1 Anycatcher 버전 인스톨러 처리
		- trunk\OpenManager_DOF\OpenManager\ReleaseAnycatcher\bin\*.exe		-> trunk\OpenManager 5.0 Installer\CustomSetupFile\AnyCatcher\Common\Bin\*.* 복사한다.
		- trunk\OpenManager_DOF\OpenManager\ReleaseAnycatcher\modules\*.* 	-> trunk\OpenManager 5.0 Installer\CustomSetupFile\AnyCatcher\Common\Modules\*.* 복사한다.
	3.3.2 Anycatcher Patch 처리
		- trunk\OpenManager_DOF\OpenManager\ReleaseAnycatcher\bin\*.exe		-> D:\Upload\OpenManager5\release\autobuild\5.0.YYYYMMDD_HHMM\Patch\AnycatcherClient\bin
		- trunk\OpenManager_DOF\OpenManager\ReleaseAnycatcher\modules\*.*	-> D:\Upload\OpenManager5\release\autobuild\5.0.YYYYMMDD_HHMM\Patch\AnycatcherClient\modules
		
	3.4.1 BTV 버전 인스톨러 처리
		- trunk\OpenManager_DOF\OpenManager\ReleaseBtv\modules\*.* -> trunk\OpenManager 5.0 Installer\CustomSetupFile\BTV\Common\Modules\*.* 복사한다.
	3.4.2 BTV Patch 처리
		- trunk\OpenManager_DOF\OpenManager\ReleaseBtv\modules\*.* -> D:\Upload\OpenManager5\release\autobuild\5.0.YYYYMMDD_HHMM\Patch\btv\modules

4. 인스톨러 생성
	4.1 아래의 ISM 파일에서 <ProductVersion> node를 찾아서 오늘 날짜를 기준으로 ProductVersion을 변경한다.
		* "trunk\\OpenManager 5.0 Installer\\AnyCatcher.ism"
		* "trunk\\OpenManager 5.0 Installer\\OpenManager 5.0_Lite.ism"		
	4.2 trunk\autobuild\YYYYMMDD_HHMM\ 폴더에 installer 프로젝트를 export 한다.
	4.3 인스톨러 프로젝트를 빌드 한다.
	4.4 빌드된 인스톨러를 빌드 날짜에 맞게 파일명 변경 후 Upload 폴더에 복사한다.
	
5. FTP 업로드
	6.1 Upload 폴더에 복사된 patch module(파일 버전이 변경되어 4번 단계에서 복사된 모듈)과 인스톨러를 WinSCP를 이용해 FTP로 복사한다.
		* OpenManager5/release/client/autobuild/5.0.YYYYMMDD_HHMM/ 에 업로드 된다.
	
7. GIT 으로 백업
    7.1 "D:\svn_backup\DOF" 경로에 svn fetch를 이용하여 GIT 백업을 한다.

 8. 업로드 완료 후 Slack 채널에 작업 완료를 알려준다.