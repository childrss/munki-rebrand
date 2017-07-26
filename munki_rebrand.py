#!/usr/bin/python
# -*- coding: utf-8 -*-

# Arjen van Bochoven Oct 2014
# Script to rebrand/customize Managed Software Center
#
# Customised for University of Oxford by
# Ben Goodstein Mar 2015
#
# Matt "M@" Childress, University of Illinois:
#   * if it exists, only updates local git repo of munki source
#     doesn't nuke and redownload each time
#   * builds multiple installers based on how many postinstall_scripts-* are in root directory
#   * renames installers based on postinstall_script-(*) name
#   * commented out a lot of stuff I didn't need
#
# Prerequisites: You need Xcode (5/6) installed
# For Xcode 6 you need to add the 10.8 SDK
# See: https://github.com/munki/munki/wiki/Building%20Munki2%20Pkgs
#
# Put this script in an *empty* directory
# and make it executable
#
# Set appNameWanted to your preferred name
# Add an optional AppIcon.icons file
# Add an optional postinstall_script
#
# Then run ./munki_rebrand.py
#
# ! Caveat: this is a very rudimentary script that is likely
# to break in future MSC releases. Use at your own risk

import glob
import fileinput
import subprocess
import re
from os import listdir, stat, chmod, makedirs, rename
from os.path import isfile, isdir, join
from shutil import copyfile

# Desired new app name
appNameWanted = 'Managed Software Center'

# Optional icon file to replace the MSC icon
# srcIcon = 'AppIcon.icns'

# Read in a list of files starting with postinstall_script to be executed upon install

postinstall_script_files = glob.glob("./postinstall_script*")
print ( postinstall_script_files )

# Git release tag (leave empty for latest build)
tag = ''

### Probably don't need to edit below this line

# App name requiring replacement
appNameOriginal = 'Managed Software Center'

# Localized forms of app name
appNameLocalized = {    'da'       : 'Managed Software Center',
                                'de'       : 'Geführte Softwareaktualisierung',
                                'en'       : 'Managed Software Center',
                                'en_AU'  : 'Managed Software Centre',
                                'en_GB'  : 'Managed Software Centre',
                                'en_CA'  : 'Managed Software Centre',
                                'es'       : 'Centro de aplicaciones',
                                'fi'       : 'Managed Software Center',
                                'fr'       : 'Centre de gestion des logiciels',
                                'it'       : 'Centro Gestione Applicazioni',
                                'ja'       : 'Managed Software Center',
                                'nb'       : 'Managed Software Center',
                                'nl'       : 'Managed Software Center',
                                'ru'       : 'Центр Управления ПО',
                                'sv'       : 'Managed Software Center'
                            }


# Make Munki pkg script
make_munki = 'munki/code/tools/make_munki_mpkg.sh'

# Git repo
# Munki2 git repo
# git_repo = "https://github.com/munki/munki/tree/Munki2"
# this gets the latest (currently munki 3)
git_repo = "https://github.com/munki/munki"

# if we already have a munki subdirectory, we've already downloaded the repo (no need to 
if isdir( "./munki" ): 

    '''
    # code for tessting
    subprocess.call(["ls", "-l"], cwd='./munki')
    if isdir ( "./munki/bad-directory" ): 
        print ( "bad-directory exists" )     
    else:
        makedirs ( "./munki/bad-directory" )
        print ( "creating bad-directory" )     
        
    if isfile ( "./munki/bad-file" ):
        print ( "bad-file exists" )     
    else:
        subprocess.call(['touch', join("./munki/", "bad-file")])
        print ( "creating bad-file" )     

    subprocess.call(["ls", "-l"], cwd='./munki')
    print ""
    ''' 
           
    # -d clears directories AND fies
    # -x clears untracked files
    # shell=True is not advised, but the only way I could get git to work 
    print 'Cleaning munki git repo'
    subprocess.call(['/usr/bin/git clean -f -x -d', git_repo], shell=True, cwd='./munki')

    print 'Updating git repo'
    proc = subprocess.call(['/usr/bin/git fetch', git_repo], shell=True, cwd="./munki")
    proc = subprocess.call(['/usr/bin/git reset --hard', git_repo], shell=True, cwd="./munki")
else:
    # ./munki does exist, so create it 
    print 'Cloning git repo'
    proc = subprocess.Popen(['git','clone', git_repo])
    proc.communicate()

if tag:
      print 'Checkout tag %s' % tag
      proc = subprocess.Popen(['git','-C', 'munki', 'checkout', 'tags/%s' % tag])
      proc.communicate()

# Replace in required files

print 'Replacing %s with %s' % (appNameOriginal, appNameWanted)

replaceList = ['InfoPlist.strings', 'Localizable.strings', 'MainMenu.strings']

appDirs = ['munki/code/apps/Managed Software Center/Managed Software Center','munki/code/apps/MunkiStatus/MunkiStatus']

def searchReplace(search, replace, fileToSearch):
      if isfile(fileToSearch):
            try:
                for line in fileinput.input(fileToSearch, inplace=True):
                      print(re.sub(search, replace, line)),
            except Exception, e:
                print "Error replacing in %s" % fileToSearch

for appDir in appDirs:
      
      if isfile(join(appDir, 'en.lproj/MainMenu.xib')):
            searchReplace(appNameOriginal, appNameWanted, join(appDir, 'en.lproj/MainMenu.xib'))
      if isfile(join(appDir, 'MSCMainWindowController.py')):
            searchReplace(appNameOriginal, appNameWanted, join(appDir, 'MSCMainWindowController.py'))
      
      for f in listdir(appDir):
            for countryCode, localizedName in appNameLocalized.iteritems():
                if f.endswith('%s.lproj' % countryCode):
                      for i in replaceList:
                            fileToSearch = join(appDir, f, i)
                            if isfile(fileToSearch):
                                # Replaces all instances of original app name
                                searchReplace(appNameOriginal, appNameWanted, fileToSearch)
                                # Matches based on localized app name
                                searchReplace(localizedName, appNameWanted, fileToSearch)

# Copy icons
#if isfile(srcIcon):
#      print("Replace icons with %s" % srcIcon)
#      destIcon = "munki/code/apps/Managed Software Center/Managed Software Center/Managed Software Center.icns"
#      copyfile(srcIcon, destIcon)
#      destIcon = "munki/code/apps/MunkiStatus/MunkiStatus/MunkiStatus.icns"
#      copyfile(srcIcon, destIcon)

for postinstall_script in postinstall_script_files:
      
      # the 18: strips off the first 21 characters, which are "./postinstall_script-" 
      config_file_directory_name = postinstall_script[ 21: ]
      print ( config_file_directory_name )
      print("Add postinstall script: %s" % postinstall_script)
      postinstall_dest = "munki/code/pkgtemplate/Scripts_app/postinstall"
      copyfile(postinstall_script, postinstall_dest)
      # Set execute bit
      st = stat(postinstall_dest)
      chmod(postinstall_dest, (st.st_mode | 0111))


      print("Building Munki ")
      proc = subprocess.Popen(['./munki/code/tools/make_munki_mpkg.sh','-r','munki'])
      proc.communicate()

      # rename the resultant built .pkg installer file to reflect the imbedded config filename
      munki_installer_files = glob.glob("munkitools-*.pkg")
      munki_installer_name = munki_installer_files[0]
      print ( munki_installer_name )
      print ( config_file_directory_name + munki_installer_name )
      rename( munki_installer_name, config_file_directory_name + "-" +munki_installer_name )
