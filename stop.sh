pid1=$(awk -F ' ' 'NR==1{pid=$4;sub(/\[/,"",pid);sub(/\]/,"",pid);print pid}' client1.log)
pid2=$(awk -F ' ' 'NR==1{pid=$4;sub(/\[/,"",pid);sub(/\]/,"",pid);print pid}' client2.log)
kill -9 $pid1
kill -9 $pid2
