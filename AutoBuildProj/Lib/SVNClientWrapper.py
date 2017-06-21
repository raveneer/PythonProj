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
            result = subprocess.run([self.svnclientpath, 'cleanup', repository], stdout=subprocess.PIPE)
            self.mylogger.info('SVN Cleanup - {0}'.format(result.stdout.decode('utf-8')))
            result = subprocess.run([self.svnclientpath, 'update', repository], stdout=subprocess.PIPE)
            self.mylogger.info('SVN UPDATE - {0}'.format(result.stdout.decode('utf-8')) )

    def svnRevert(self):
        for repository in self.repositoryList:
            self.mylogger.info('SVN CleanUp And Revert : [{0}]'.format(repository))
            subprocess.run([self.svnclientpath, 'cleanup', repository], stdout=subprocess.PIPE)
            subprocess.call([self.svnclientpath, 'revert', '-R', repository])


    def svnCommit(self, commitLog):
        print("svn commit")

    def svnExport(self, svnRepository, destDir):
        subprocess.call([self.svnclientpath, 'export', svnRepository, destDir, '--force'])
        self.mylogger.info('SVN EXPORT - [{0}] to [{1}]'.format(svnRepository, destDir))


