[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D2363885-B21A-478B-8E1F-CCCD4C0EA533}
AppName=App Name
AppVersion=0.1
AppPublisher=Citec
AppPublisherURL=https://github.com/wlaur/gui-template
AppSupportURL=https://github.com/wlaur/gui-template
AppUpdatesURL=https://github.com/wlaur/gui-template
DefaultDirName={userappdata}\App Name
DisableProgramGroupPage=yes
OutputBaseFilename=app_name_0.1_installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UsePreviousTasks=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\willlaur\Desktop\app.dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\willlaur\Desktop\app.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\App Name"; Filename: "{app}\app.exe"
Name: "{commondesktop}\App Name"; Filename: "{app}\app.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\app.exe"; Description: "{cm:LaunchProgram,App Name}"; Flags: nowait postinstall skipifsilent