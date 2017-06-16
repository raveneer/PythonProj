#-*- coding: utf-8 -*-

import subprocess

class SVNClient(object):

    def __init__(self, repositoryList):
        print("SVNClient init")
        self.svnclientpath = 'svn'
        self.repositoryList = repositoryList[:]

    def svnUpdate(self):
        print("svn update")
        for repository in self.repositoryList:
            subprocess.call([self.svnclientpath, 'update', repository])

    def svnRevert(self):
        print("svn Revert")
        for repository in self.repositoryList:
            subprocess.call([self.svnclientpath, 'revert', '-R', repository])

    def svnCommit(self, commitLog):
        print("svn commit")

    def svnExport(self, svnRepository, destDir):
        print("svn export")
        subprocess.call([self.svnclientpath, 'export', svnRepository, destDir, '--force'])


