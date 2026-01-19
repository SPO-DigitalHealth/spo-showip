[Setup]
AppName=SpoShowIP
AppVersion=1.0.1
AppPublisher=Suphanburi Provincial Public Health Office
AppPublisherURL=https://spo.moph.go.th
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

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "SpoShowIP"; ValueData: "{app}\SpoShowIP.exe"; Flags: uninsdeletevalue

[Tasks]
Name: "startup"; Description: "&Run SpoShowIP at startup"; GroupDescription: "Startup Options:"

[Icons]
Name: "{group}\SpoShowIP"; Filename: "{app}\SpoShowIP.exe"
Name: "{commondesktop}\SpoShowIP"; Filename: "{app}\SpoShowIP.exe"

[Run]
Filename: "{app}\SpoShowIP.exe"; Description: "Launch SpoShowIP"; Flags: nowait postinstall skipifsilent