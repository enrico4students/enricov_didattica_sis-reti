# @echo off
g++ udp_receiver.cpp -o udp_receiver.exe -lws2_32
start udp_receiver.exe
g++ udp_sender.cpp -o udp_sender.exe -lws2_32
start udp_sender.exe