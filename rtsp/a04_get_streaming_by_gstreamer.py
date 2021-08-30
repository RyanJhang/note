from gsp import GstreamerPlayer

player = GstreamerPlayer(None)

player.queue("rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp")