@echo off
cd ..
pyinstaller main.py --onefile --noconsole
rmdir /s /q release\alpha
mkdir release\alpha
copy NUL release\alpha\.gitkeep
move build release\alpha
move dist release\alpha
del main.spec
mkdir "release\alpha\entrepinoy"
move release\alpha\dist\main.exe release\alpha\entrepinoy
mkdir release\alpha\entrepinoy\assets
xcopy /e assets release\alpha\entrepinoy\assets\
mkdir release\alpha\entrepinoy\game
mkdir release\alpha\entrepinoy\game\config
xcopy /e game\config release\alpha\entrepinoy\game\config
mkdir release\alpha\entrepinoy\game\debug
xcopy /e game\debug release\alpha\entrepinoy\game\debug
mkdir release\alpha\entrepinoy\game\library
xcopy /e game\library release\alpha\entrepinoy\game\library
mkdir release\alpha\entrepinoy\game\progress
cd release\alpha\entrepinoy
 
main
cd ../../..
cmd -k