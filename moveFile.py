#!/usr/bin/python
import os, shutil, sys, getopt, re

auto_yes=False # Default to giving a chance to cancel

def usage(err=''):
    if (err):
        print('[ERROR] '+err)
    print('usage: '+sys.argv[0]+' [-y] <directory>')
    sys.exit(2)

# Do some checking of our command line
# Get any command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "y")
except getopt.GetoptError as err:
    usage(str(err))

# If -y is set, skip asking for confirmation
for o,a in opts:
    if o == "-y":
        auto_yes=True

if len(args) == 1:
    if os.path.isdir(args[0]):
        dir = args[0]
    else:
        usage('invalid path: '+args[0])
elif len(args) == 0:
    usage('missing path')
else:
    usage('too many arguments')

# Get started
os.chdir(dir)
print('Moving files in ['+os.getcwd()+']')
# Since we're making changes to the file system, give the user a chance to cancel unless they
# have used -y option
if not auto_yes:
    response = raw_input('WARNING! This action cannot be undone.  Continue? (y/n) ')
    # Simulate a do..while loop
    while True:
        if response.strip().upper() == 'N':
            print('Move has been cancelled.  Exiting...')
            sys.exit(1)
        elif response.strip().upper() == 'Y':
            break
        else:
            response = raw_input('Invalid input. Try again. Continue? (y/n) ')

# Move some stuff around
no_files_moved = True # Assume we haven't moved anything
for f in os.listdir('.'):
    # Only move regular files, ignore symbolic links, hidden files, and directories
    if not os.path.islink(f) and not f.startswith(".") and os.path.isfile(f):
        no_files_moved = False # Something has moved
        
        # Create the directory if it doesn't exist
        dest_file = re.sub(r'Season ',"S",f) 
        dest_file = re.sub(r' Episode ',"E",dest_file)
        dest_file = re.sub(r' -',"",dest_file)
        dest_file = re.sub(r' ',".",dest_file)
        dest_file = re.sub(r'.&.',"",dest_file)
        shutil.move(f, dest_file)
        print('File '+os.path.basename(f)+' has been moved to '+dest_file)

if no_files_moved:
    print('No files to move!  Exiting...')
