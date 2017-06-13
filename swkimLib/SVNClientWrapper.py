#-*- coding: utf-8 -*-


class SVNClient(object):

    def __init__(self, svnclientpath, repositorypath):
        print("SVNClient init")
        self.svnclientpath = svnclientpath
        self.repositorypath = repositorypath

    def svnUpdate(self):
        print("svn update")

    def svnRevert(self):
        print("svn Revert")

    def svnCommit(self, commitLog):
        print("svn commit")

