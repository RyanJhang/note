
import asyncio
from aiortsp.rtsp.reader import RTSPReader

async def main():
    # Open a reader (which means RTSP connection, then media session)
    async with RTSPReader("rtsp://root:12345678z@192.168.1.119:554/live1s1.sdp") as reader:
        # Iterate on RTP packets
        async for pkt in reader.iter_packets():
            print('PKT', pkt.seq, pkt.pt, len(pkt))

asyncio.run(main())