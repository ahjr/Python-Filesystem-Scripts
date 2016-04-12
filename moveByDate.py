#!/usr/bin/python
# Move files into directories by their last modification date in the format YYYY-MM-DD, YYYY-MM-WK# or YYYY-MM
# Ignores directories (does not recurse), symbolic links and hidden files
import os, time, shutil, sys, getopt

monthly=False # Default to using YYYY-MM-DD
weekly=False
format_string="YYYY-MM-DD" 
auto_yes=False # Default to giving a chance to cancel

def usage(err=''):
    if (err):
        print('[ERROR] '+err)
    print('usage: '+sys.argv[0]+' [-m][-w][-y] <directory>')
    sys.exit(2)

# Do some checking of our command line
# Get any command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "mwy")
except getopt.GetoptError as err:
    usage(str(err))

# If -m is set, change our output directories to YYYY-MM
# If -w is set, change our output directories to YYYY-MM-WK#
# If -y is set, skip asking for confirmation
for o,a in opts:
    if o == "-m":
        monthly=True
        format_string="YYYY-MM" 
    elif o == "-w":
        weekly = True
        format_string="YYYY-MM-WK#"
    elif o == "-y":
        auto_yes=True

# Can't use both -m and -w together
if monthly and weekly:
    usage('-m and -w must not be used together')
    
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
print('Moving files in ['+os.getcwd()+'] to directories in the format ['+format_string+']')
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
        mod_time = time.gmtime(os.path.getmtime(f)) # Get modification time
        if monthly:
            new_dir = str(time.strftime("%Y",mod_time))+'-'+str(time.strftime("%m",mod_time))
        elif weekly:
            # Figure out what week - starting from first of the month
            week_num = int(time.strftime("%d", mod_time))/7+1
            new_dir = str(time.strftime("%Y",mod_time))+'-'+str(time.strftime("%m",mod_time))+'-'+'WK'+str(week_num)
        else:
            new_dir = str(time.strftime("%Y",mod_time))+'-'+str(time.strftime("%m",mod_time))+'-'+str(time.strftime("%d",mod_time))
        
        # Create the directory if it doesn't exist
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        dest_file = new_dir+'/'+f
        shutil.move(f, dest_file)
        print('File '+os.path.basename(f)+' has been moved to '+dest_file)

if no_files_moved:
    print('No files to move!  Exiting...')
