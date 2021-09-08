一、启动软件

1.首先检查文件夹内文件，分别为main.py, denoised.py, env.txt

[![hHdvGt.png](https://z3.ax1x.com/2021/09/08/hHdvGt.png)](https://imgtu.com/i/hHdvGt)


2.打开文件夹，在上方路径栏内输入cmd，回车

[![hHwfeg.png](https://z3.ax1x.com/2021/09/08/hHwfeg.png)](https://imgtu.com/i/hHwfeg)


3.在黑框内输入pip install -r env.txt（注意空格）

[![hHwoYn.png](https://z3.ax1x.com/2021/09/08/hHwoYn.png)](https://imgtu.com/i/hHwoYn)

4.等待安装完成后，输入python main.py启动软件

[![hHwvTJ.png](https://z3.ax1x.com/2021/09/08/hHwvTJ.png)](https://imgtu.com/i/hHwvTJ)

二、软件各部分说明

采集数据临时地址：是一个采集数据临时存放的文件夹，我们初采的数据会放至该文件夹内，待程序检测没有问题后进行处理，须人工填写，仅需在文件夹的地址栏点击进行复制即可。如C:\Users\PLM\Desktop\src\采集数据临时存放地址

[![hH0Pl6.png](https://z3.ax1x.com/2021/09/08/hH0Pl6.png)](https://imgtu.com/i/hH0Pl6)


采样数据存放地址：是我们采样的波形最终存放的地址，须人工填写，方法同上，注意，以上两个地址不能共用一个文件夹


采集设备编号：为采集设备机身条形码下长编号的后7位，三位数字+R+三位数字，如941R050


采集员姓名：为执行当前采集任务的采集人员姓名拼音全拼，如zhangsan


采集日期：为当前采集任务的日期


采集地点：为当前采集任务的地点，精确到市，如上海市


布匹编号和成分：编号为布匹的全局唯一编号，格式为部门代码+数字编号，例如 AS1919，成分为所有涉及成分的字母代码加百分占比，例如L55C45代表linen含量55%， cotton 含量 45%，故该栏正确填法为AS1919_L55C45


织法：针织或梭织，W是针织，K是梭织，不确定是U。


三、使用软件
1.打开软件填好采集数据临时地址和采样数据存放地址后，点击开始检测，之后进行数据采集，此时开始检测会变成红色，再次点击可以停止检测

[![hH0VTH.png](https://z3.ax1x.com/2021/09/08/hH0VTH.png)](https://imgtu.com/i/hH0VTH)


2.采集过程中，软件会实时检测所采集的数据是否符合要求，若有不符合要求的数据，软件会进行弹框提醒，请采集人员点击“Yes”删除该条数据后重新进行采集


[![hH0mtA.png](https://z3.ax1x.com/2021/09/08/hH0mtA.png)](https://imgtu.com/i/hH0mtA)


3.采集完成后，请采集人员完善程序下方所有信息，并点击本匹布样采集完成，将符合要求的采集数据转移至最终存放地址，注意，下方左侧数据，整个采集过程仅需填写一次，如果更换采集人员或者关闭重开软件后须重新填写，右侧布匹编号和成分以及织法，每匹布样采集完成都需要根据当前采集布匹的信息进行更新，注意需要在点击本匹布样采集完成按钮前进行更新

[![hH0Kpt.png](https://z3.ax1x.com/2021/09/08/hH0Kpt.png)](https://imgtu.com/i/hH0Kpt)