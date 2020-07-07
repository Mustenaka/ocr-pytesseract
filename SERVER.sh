time_start=$(date)
echo "服务器开始后台运行,$time_start"
nohup python3 app.py &>log.txt
