[Setup]
AppName=Typing Tutor
AppVersion=1.0
DefaultDirName={pf32}\Typing Tutor
VersionInfoDescription="Test your typing with this simple and fun program"
DefaultGroupName=Typing Tutor
OutputBaseFilename=TypingTutor-1.0

[files]
Source: "dist\main\*"; DestDir: "{app}"; flags: recursesubdirs
Source: "lib\*"; DestDir: "{app}\accessible_output2\lib"; flags: recursesubdirs
Source: "exercises\*"; DestDir: "{app}\exercises"; flags: recursesubdirs
Source: "sounds\*"; DestDir: "{app}\sounds"; flags: recursesubdirs
Source: "readme.html"; DestDir: "{app}"; flags: ISREADME

[Icons]
Name: "{group}\Typing Tutor"; Filename: "{app}\Typing Tutor.EXE"
Name: "{group}\Typing Tutor User Guide"; FileName: "{app}\readme.html"
Name: "{group}\Uninstall Typing Tutor"; Filename: "{uninstallexe}"

