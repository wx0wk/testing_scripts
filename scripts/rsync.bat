set SOURCE_DIR=/f/Projects/gpsil
set REMOTE_DIR=find:/mnt/nfs/wxin/front/files/frontend/gpsil
set CHOWN=globspot:www-data
C:\msys64\msys2_shell.cmd -c "rsync.exe -rlptD -zzhP --stats --chown=%CHOWN% --exclude-from=%SOURCE_DIR%/.gitignore %SOURCE_DIR% %REMOTE_DIR% 2> %SOURCE_DIR%/../err.log && echo Finished && read -n 1 -s -r -p 'Press any key to exit..'"
