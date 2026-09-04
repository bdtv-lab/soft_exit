## Soft exit

在关闭服务器时将玩家转移至一个临时服务器

服务器即将终止
转移玩家
初始化bar
显示bar
State.Closing
服务器关闭
bar进度设置为等待启动
State.Custom
bar 0%
此处可以有自定义逻辑
服务器启动中
State.Starting
bar 75%
启动完毕
bar 100%
State.Started
15分钟后
隐藏 bar
State.Hide