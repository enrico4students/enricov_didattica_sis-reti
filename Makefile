all: tcp_sender tcp_receiver udp_sender udp_receiver

tcp_sender:
	g++ tcp/tcp_sender.cpp -o tcp/tcp_sender.exe -lws2_32

tcp_receiver:
	g++ tcp/tcp_receiver.cpp -o tcp/tcp_receiver.exe -lws2_32

udp_sender:
	g++ udp/udp_sender.cpp -o udp/udp_sender.exe -lws2_32

udp_receiver:
	g++ udp/udp_receiver.cpp -o udp/udp_receiver.exe -lws2_32

clean:
	del /Q tcp\*.exe udp\*.exe