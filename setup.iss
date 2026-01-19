[Setup]
AppName=SpoShowIP
AppVersion=1.0.1
AppId={{12345678-1234-1234-1234-123456789012}
DefaultDirName={pf}\SpoShowIP
DefaultGroupName=SpoShowIP
OutputDir=.\dist
OutputBaseFilename=SpoShowIP_Portable
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=none
VersionInfoVersion=1.69.1.19.0
UninstallDisplayIcon={app}\SpoShowIP.exe
CloseApplications=yes

[Files]
Source: "dist\SpoShowIP.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "img\*"; DestDir: "{app}\img"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\SpoShowIP"; Filename: "{app}\SpoShowIP.exe"
Name: "{commondesktop}\SpoShowIP"; Filename: "{app}\SpoShowIP.exe"

[Run]
Filename: "{app}\SpoShowIP.exe"; Description: "Launch SpoShowIP"; Flags: nowait postinstall skipifsilent