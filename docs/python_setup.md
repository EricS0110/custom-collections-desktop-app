# Getting Set Up with Python

This section will walk you through setting up a Python environment from scratch.  If you already have Python 
installed and a virtual environment set up that this application can use, you can skip this section!

## Downloading and Installing Python

This was supposed to be as easy as running a Windows batch file I set up to run the commands to download and install
Python 3.13 for you if it wasn't found on your system, but Microsoft Defender is too good at its job and will block any
such scripts from running if they were downloaded from the internet.  Hopefully these instructions are clear enough, 
but if not please leave an Issue with your hang-ups on the GitHub repo, and I'll try my best to keep the documentation
updated!

1. To get started, navigate to [this link](https://www.python.org/) to download Python.  Please look
for the latest version of the 3.13 version of Python.
![Python Download Page](images/PythonSetup/PythonSetup001.png)
2. Once the installer file finishes downloading, you'll want to run it.  You can do this by double-clicking the file in
your downloads folder, or by clicking the file in your browser if it's still in your downloads bar.
3. When you start the installation process, you should see a window similar to the one below.  The **most** important
part of this installation process is to make sure you've got the `Add python.exe to PATH` selected.  This will make
sure that Windows recognizes your installation of Python as the default.  Once you've double-checked that this box is 
selected, you're good to click on the `Install Now` option.  If you're an advanced user and want to go your own way,
you can click on `Customize installation`, but these instructions assume you just want the default installation.
![Python Installation Start](images/PythonSetup/PythonSetup002.png)