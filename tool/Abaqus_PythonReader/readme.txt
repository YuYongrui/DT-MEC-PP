===========================
  PythonReader
===========================
操作提示：
1、该程序无须放在ABAQUS的工作目录下，可随意放置。另外程序可以随时打开，无须考虑与ABAQUS CAE的打开次序；
1、程序第一次运行时需要指定abaqus.rpy的位置，以后运行会自动加载上一次设置；
2、在窗口中拖动右键可以移动窗口位置；
3、把鼠标移动到窗口边缘可以拖动改变窗口大小。

该程序主要是给使用ABAQUS的朋友们学习Python用的,可以作为ABAQUS PDE的辅助工具，

对于ABAQUS和Python的关系我就不多说了，在ABAQUS CAE中的每一个菜单或按钮操作都是被解释为Python语句，然后才提交上去。
而这些Python语句被适时地保存在工作目录下的abaqus.rpy文件中，这就给我们提供了一个绝好的Python学习途径：进行CAE的操作，然后查看abaqus.rpy文件中的对应的Python语句//

该程序会适时的读取abaqus.rpy文件，以便你把相应的CAE操作对照起来//

==========================================================
如果你根本就不能运行本程序,那很有可能你还没有安装.NET Framework 2.0以上的平台.
.NET Framework是在Microsoft .NET平台上进行程序开发和程序运行的基础.

给出解决方法:

你可以通过以下几个网址下载:
http://www.onlinedown.net/soft/38669.htm
http://www.microsoft.com/downloads/details.aspx?FamilyID=0856eacb-4362-4b0d-8edd-aab15c5e04f5&DisplayLang=zh-cn#QuickInfoContainer

如果安装.NET Framework时提示installer错误,则你需要先安装Windows Installer（一般不会遇到）:
http://www.onlinedown.net/soft/12668.htm
http://www.microsoft.com/downloads/details.aspx?displaylang=zh-cn&FamilyID=889482fc-5f56-4a38-b838-de776fd4138c
