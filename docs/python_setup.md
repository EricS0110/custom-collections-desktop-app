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
4. Once you click the `Install Now` option, you'll see Python start installing on your system.  This process can take
a few minutes depending on your system, so please be patient.
![Python Installation Progress](images/PythonSetup/PythonSetup003.png)
5. Once the installation is complete, you should see a window similar to the one below.  You can click the `Close` 
button to finish the installation process, and you're ready to move on to the next step!  If you plan on installing 
multiple versions of Python or multiple other programming languages, you may wish to click on the
`Disable path lenght limit` option, but this is not necessary for just this application.
![Python Installation Complete](images/PythonSetup/PythonSetup004.png)

## Verifying Your Installation
The easiest way to verify that Python is installed correctly is to open a new command prompt or Windows Terminal 
instance and type `python --version`.  You can open the command prompt by pressing the `Windows` key and typing `cmd`, 
then pressing `Enter`.  You can open Windows Terminal by pressing the `Windows` key and typing `Terminal`, then
pressing `Enter`.  If you see a version number similar to `Python 3.13.2`, then you're good to go!  If you see an error
message, please uninstall Python and try the installation process again, being sure to follow all the steps laid out
above.

The screenshot below shows how to check for the Python version in Windows Terminal.
![Python Version Check](images/PythonSetup/PythonSetup005.png)

## [OPTIONAL] Setting Up a Virtual Environment
If you're planning on using Python for other projects, or you just want to keep your base Python installation only 
containing the default packages, you may want to set up a virtual environment.  This will allow you to install packages
for this application without affecting your base Python installation.  If you're not interested in setting up a virtual
environment, you can skip this step.

1. To set up a virtual environment, you'll need to open a new command prompt or Windows Terminal instance.  The screen
captures for this section are captured from Windows Terminal, but the process is very similar in Command Prompt.