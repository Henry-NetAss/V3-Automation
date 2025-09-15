copy-item -Path "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk" -Destination "C:\Users\Public\Desktop\Word.lnk" -Recurse -Force
copy-item -Path "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Outlook (Classic).lnk" -Destination "C:\Users\Public\Desktop\Outlook.lnk" -Recurse -Force
copy-item -Path "$env:USERPROFILE\appdata\local\google\chrome\application\chrome.exe" -Destination "c:\na\installation\chrome.lnk" -Recurse -Force
