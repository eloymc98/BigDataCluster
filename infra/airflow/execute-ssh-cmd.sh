#!/usr/bin/expect

set host [lindex $argv 0]
set password [lindex $argv 1]
set dir [lindex $argv 2]
set command [lindex $argv 3]

spawn ssh $host
expect {
      "Are you sure you want to continue connecting*" {
            send "yes\r"
            exp_continue
      }
      "Password:*" {
            send "$password\r"
            expect "*$host*"
            send "cd $dir\r"
            expect "$ "
            send "$command\r"
            expect "$ "
            send "exit\r"
            expect eof
      }
}
