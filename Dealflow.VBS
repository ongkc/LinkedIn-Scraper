Function Tilak()
dim shell
set shell=createobject("wscript.shell")
shell.Run "C:\Users\ongkc\Desktop\Run_Dealflow_Script.bat",0,True
set shell=nothing
End Function

Tilak()