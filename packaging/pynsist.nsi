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
[[ super() ]]

Function LaunchLink
  [% for scname in ib.shortcuts %]
    ExecShell "" "$SMPROGRAMS\[[scname]].lnk"
  [% endfor %]
FunctionEnd

[% endblock sections  %]