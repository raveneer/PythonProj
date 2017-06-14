#-*- coding: utf-8 -*-
import subprocess


if __name__ == "__main__":

    ngf_proj_xml = '"D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\ngf_release.xml"'
    ngf_build_log = 'd:\\NGF_FULL\\trunk\\autobuild\\_logs\\slackbot.log'

    #subprocess.call(['Nant', ' -buildfile:"D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\ngf_release.xml" build -logfile:{0}'.format( ngf_build_log)])
    #subprocess.call(['Nant', ' -logfile:{1} -buildfile:{0} build '.format(ngf_proj_xml, ngf_build_log)])

    #subprocess.call(['Nant.exe', '-buildfile:"D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\ngf_release.xml"'])
    subprocess.call(['E:\\Program Files\\nant-0.92\\bin\\nant.exe', '-buildfile:D:\\NGF_FULL\\Branches\\swkim_brach\\AutoBuild\\Nant Script\\ngf_release.xml'])
