#-*- coding: utf-8 -*-

import subprocess
import logging

class SVNClient(object):

    def __init__(self, repositoryList):
        self.svnclientpath = 'svn'
        self.repositoryList = repositoryList[:]
        self.mylogger = logging.getLogger('auto_build_logger')

    def svnUpdate(self):
        for repository in self.repositoryList:
            self.mylogger.info('SVN CleanUp And UPDATE : [{0}]'.format(repository))
            subprocess.run([self.svnclientpath, 'cleanup', repository])
            subprocess.run([self.svnclientpath, 'update', repository])

    def svnRevert(self):
        for repository in self.repositoryList:
            self.mylogger.info('SVN CleanUp And Revert : [{0}]'.format(repository))
            subprocess.run([self.svnclientpath, 'cleanup', repository])
            subprocess.run([self.svnclientpath, 'revert', '-R', repository])


    def svnCommit(self, commitLog):
        for repository in self.repositoryList:
            subprocess.run([self.svnclientpath, 'commit', '-m', commitLog, repository])
            self.mylogger.info('SVN COMMIT - [{0}]  LOG : [{1}]'.format(repository, commitLog))

    def svnExport(self, svnRepository, destDir):
        subprocess.run([self.svnclientpath, 'export', svnRepository, destDir, '--force'])
        self.mylogger.info('SVN EXPORT - [{0}] to [{1}]'.format(svnRepository, destDir))

    def svnLogExport(self, svnRepository, logfile):
        proc = subprocess.run([self.svnclientpath, 'log', '-r', 'HEAD', svnRepository ], stdout=subprocess.PIPE)
        out, err = proc.communicate()

    def getHeadRevision(self, repository):
        proc = subprocess.Popen(['svn', 'log', '-r', 'HEAD', repository], stdout=subprocess.PIPE)
        headlog = str(proc.stdout.read(), 'euc-kr')
        new_headlog = headlog.replace('-', '')
        headrevision = new_headlog.split('|')[0]
        headrevision = headrevision.replace('r', '').strip('\r\n ')  # 줄바꿈 및 공백
        return headrevision

    def getCommitLog(self, repository, revision):
        proc = subprocess.Popen(['svn', 'log', '-r', revision, repository], stdout=subprocess.PIPE)
        headlog = str(proc.stdout.read(), 'euc-kr')
        new_headlog = headlog.replace('-', '')
        headrevision = new_headlog.split('\r\n')[3]
        return headrevision

    def dumpCommitlog(self, repository, commitfile):

        headrevision = self.getHeadRevision(repository)
        revision = int(headrevision.strip())
        commitdump = open(commitfile, 'a')

        while revision > 0:
            commitlog = self.getCommitLog(repository, str(revision))
            if commitlog.find('Auto Build Commit') < 0:
                addLog = '[{0}] : {1}\r\n'.format(revision, commitlog)
                commitdump.write(addLog)
            else:
                break

            revision -= 1




