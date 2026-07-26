[Setup]
; --- Información General ---
AppName=OpenStroke
AppVersion=0.5.0.0.1
AppPublisher=exyron & Gemini AI
DefaultDirName={autopf}\OpenStroke
DefaultGroupName=OpenStroke
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

; Silenciamos el aviso de áreas de usuario
UsedUserAreasWarning=no
OutputDir=Instalador_Final
OutputBaseFilename=Instalar_OpenStroke_v0.5.0.0.1

; --- El Escudo del Desinstalador ---
AppMutex=OpenStroke_App_Mutex_Definitivo
CloseApplications=yes

; --- Estética del Instalador ---
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\openstroke.exe
Compression=lzma2/ultra64
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "Crear un acceso directo normal en el Escritorio"; GroupDescription: "Accesos directos:"
Name: "startup"; Description: "Arrancar OpenStroke automáticamente con Windows"; GroupDescription: "Arranque automático:"
Name: "debugicon"; Description: "Crear acceso directo extra para el Modo Debug (con consola)"; GroupDescription: "Herramientas de Desarrollador:"

[Files]
; 1. LA ASPIRADORA: Cogemos TODO lo que haya generado PyInstaller en modo carpeta
Source: "dist\openstroke\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; 2. Aseguramos el icono de debug si lo tienes suelto en la raíz para los accesos directos
Source: "icono_debug.ico"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist

; 3. Inyectamos tu archivo de gestos base en el AppData del usuario
Source: "gestos.yaml"; DestDir: "{userappdata}\OpenStroke"; Flags: onlyifdoesntexist

[Icons]
; 1. Accesos en la carpeta del Menú de Inicio ({group})
Name: "{group}\OpenStroke"; Filename: "{app}\openstroke.exe"
Name: "{group}\Desinstalar OpenStroke"; Filename: "{uninstallexe}"
Name: "{group}\OpenStroke (Modo Debug)"; Filename: "{app}\openstroke.exe"; Parameters: "--debug"; IconFilename: "{app}\icono_debug.ico"; Tasks: debugicon

; 2. Accesos en el Escritorio ({autodesktop})
Name: "{autodesktop}\OpenStroke"; Filename: "{app}\openstroke.exe"; Tasks: desktopicon
Name: "{autodesktop}\OpenStroke (Modo Debug)"; Filename: "{app}\openstroke.exe"; Parameters: "--debug"; IconFilename: "{app}\icono_debug.ico"; Tasks: debugicon

[Registry]
; Matriculamos el programa en el arranque si el usuario marca la casilla
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "OpenStroke"; ValueData: """{app}\openstroke.exe"""; Tasks: startup

[Run]
Filename: "{app}\openstroke.exe"; Description: "Ejecutar OpenStroke ahora"; Flags: nowait postinstall skipifsilent
