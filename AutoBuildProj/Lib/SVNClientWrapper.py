#-*- coding: utf-8 -*-

import subprocess
import logging

class SVNClient(object):

    def __init__(self, repositoryList):
        self.svnclientpath = 'svn'
        self.repositoryList = repositoryList[:]
        self.mylogger = logging.getLogger('ngf_auto_build_logger')

    def svnUpdate(self):
        for repository in self.repositoryList:
            result = subprocess.run([self.svnclientpath, 'update', repository], stdout=subprocess.PIPE)
            self.mylogger.info('SVN UPDATE - {0}'.format(result.stdout.decode('utf-8')) )

    def svnRevert(self):
        for repository in self.repositoryList:
            subprocess.call([self.svnclientpath, 'revert', '-R', repository])
            self.mylogger.info('SVN REVERT - {0}'.format(repository))

    def svnCommit(self, commitLog):
        print("svn commit")

    def svnExport(self, svnRepository, destDir):
        subprocess.call([self.svnclientpath, 'export', svnRepository, destDir, '--force'])
        self.mylogger.info('SVN EXPORT - [{0}] to [{1}]'.format(svnRepository, destDir))


