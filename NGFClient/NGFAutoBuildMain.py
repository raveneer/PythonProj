#-*- coding: utf-8 -*-
from swkimLib import SVNClientWrapper


if __name__ == "__main__":
    print("NGF Client Auto Build Start")

    #SVN 정리
    svnclient = SVNClientWrapper.SVNClient("svn", "d:\\NGF")



    #end Main