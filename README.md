
# Description
Small tool to search and get the total size of all files and folder within a given root folder, while specifying filters to exclude files from matching the search, in the format of a ".gitignore" syntax.
The need arises from the fact that in sourcetree its not possible to do so, hence the script

# How it works 
drop a .gitignore file into the top text field
drop a folder into the middle (text field), or click the button to select the root folder.
once dropped, the app will match all files and folders using the ignore text, and display the files count, the folders count and the total size of all matched elements.

# Environment Installation
 - Make sure you have python installed on your system
 - Install python dependencies: tkinterdnd2, pathspec, os, fnmatch\
`pip install tkinterdnd2`\
`pip install pathspec`

# How to run
execute the script and a window will show.
the python script uses the ".pyw" ext, meaning it will hide the underlying windows console.
if any issues occur such as exceptions, the file ext can be renamed to ".py" so when it is executed the console window will be shown.

# Contributing
Pull requests are welcome. Make me smarted if you will ;)

# License
Allowed for use only if you are either a human or a centipede.
