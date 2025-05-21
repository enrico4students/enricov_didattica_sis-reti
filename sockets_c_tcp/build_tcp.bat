# @echo off
echo Compilazione TCP Receiver...
g++ tcp_receiver.cpp -o tcp_receiver.exe -lws2_32
g++ tcp_sender.cpp   -o tcp_sender.exe -lws2_32
pause