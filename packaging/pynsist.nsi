[% extends "pyapp.nsi" %]

; Add/remove desktop shortcut
[% block install_shortcuts %]
[% for scname, sc in ib.shortcuts.items() %]
CreateShortcut "$DESKTOP\[[scname]].lnk" "[[sc['target'] ]]" '[[ sc['parameters'] ]]' "$INSTDIR\[[ sc['icon'] ]]"
[% endfor %]
[[ super() ]]
[% endblock install_shortcuts %]

[% block uninstall_shortcuts %]
[% for scname in ib.shortcuts %]
Delete "$DESKTOP\[[scname]].lnk"
[% endfor %]
[[ super() ]]
[% endblock uninstall_shortcuts %]

; Option to run after installation
[% block ui_pages  %]
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"

[[ super() ]]
[% endblock ui_pages  %]


[% block sections %]

; The "" makes the section hidden.
Section "" SecUninstallPrevious

    Call UninstallPrevious

SectionEnd

[[ super() ]]

Function LaunchLink
  [% for scname in ib.shortcuts %]
    ExecShell "" "$SMPROGRAMS\[[scname]].lnk"
  [% endfor %]
FunctionEnd

Function UninstallPrevious
    ; Check for uninstaller.
    ReadRegStr $R0 SHCTX "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}" "UninstallString"
      
    ${If} $R0 == ""        
        Goto Done
    ${EndIf}

    DetailPrint "$R0"
    DetailPrint "Removing previous installation."    

    ; Run the uninstaller silently.
    ExecWait '"$R0 /S"'

    Done:
FunctionEnd

[% endblock sections  %]