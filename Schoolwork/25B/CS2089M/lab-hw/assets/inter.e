#!/usr/bin/expect -f

# 使用方法: expect run_interactive.exp test.sql
set timeout -1
set sqlfile [lindex $argv 0]

# 这里直接写密码（或改为交互式输入）
set password "root"

# 读取 SQL 文件，按行拆分为命令列表
set f [open $sqlfile r]
set data [read $f]
close $f
set commands [split $data "\n"]

# 启动容器内的 mysql 交互式会话（必须用 -it）
spawn docker exec -it b953 mysql -u root -p

# 等待密码提示，输入密码
expect "Enter password:"
send "$password\r"

# 等待 mysql> 提示符出现
expect "mysql>"

# 逐条发送 SQL，每发送一条都等待下一条提示符出现后再继续
foreach cmd $commands {
    set cmd [string cat $cmd]
    if { $cmd ne "" } {
        send "$cmd\r"
        expect ">"
        # 可选：睡眠 0.3 秒，让输出更自然
        sleep 0.3
    }
}

# 最后退出
send "exit\r"
expect eof