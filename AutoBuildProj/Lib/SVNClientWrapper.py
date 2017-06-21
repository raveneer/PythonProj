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
            result = subprocess.run([self.svnclientpath, 'cleanup', repository], stdout=subprocess.PIPE)
            result = subprocess.run([self.svnclientpath, 'update', repository], stdout=subprocess.PIPE)
            self.mylogger.info('{0}'.format(result.stdout.decode('utf-8')) )

    def svnRevert(self):
        for repository in self.repositoryList:
            self.mylogger.info('SVN CleanUp And Revert : [{0}]'.format(repository))
            subprocess.run([self.svnclientpath, 'cleanup', repository], stdout=subprocess.PIPE)
            subprocess.call([self.svnclientpath, 'revert', '-R', repository])


    def svnCommit(self, commitLog):
        for repository in self.repositoryList:
            subprocess.call([self.svnclientpath, 'commit', '-m', commitLog, repository])
            self.mylogger.info('SVN COMMIT - [{0}]  LOG : [{1}]'.format(repository, commitLog))

    def svnExport(self, svnRepository, destDir):
        subprocess.call([self.svnclientpath, 'export', svnRepository, destDir, '--force'])
        self.mylogger.info('SVN EXPORT - [{0}] to [{1}]'.format(svnRepository, destDir))


