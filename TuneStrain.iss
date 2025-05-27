[Setup]
AppName=TuneStrain
AppVersion=1.0
DefaultDirName={pf}\TuneStrain
DefaultGroupName=TuneStrain
OutputDir=dist
OutputBaseFilename=TuneStrainSetup
SetupIconFile=assets\icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\TuneStrain.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ffmpeg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\ffprobe.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\style.qss"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "assets\icon.png"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "fonts\Montserrat-Regular.ttf"; DestDir: "{app}\fonts"; Flags: ignoreversion
Source: "fonts\Montserrat-Bold.ttf"; DestDir: "{app}\fonts"; Flags: ignoreversion

[Dirs]
Name: "{app}\converted"
Name: "{app}\output"

[Icons]
Name: "{group}\TuneStrain"; Filename: "{app}\TuneStrain.exe"; IconFilename: "{app}\assets\icon.ico"
Name: "{group}\Uninstall TuneStrain"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\TuneStrain.exe"; Description: "Запустить TuneStrain"; Flags: nowait postinstall skipifsilent