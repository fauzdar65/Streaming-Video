import sys
from time import time
HEADER_SIZE = 12

class RtpPacket:	
	header = bytearray(HEADER_SIZE)
	
	def __init__(self):
		pass
		
	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""
		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		
		header[0] = version << 6| padding << 5 | extension << 4 | cc 
		header[1] = marker << 7| pt
		header[2] = seqnum >> 8
		header[3] = seqnum & 0x00ff
		header[4] = (timestamp & 0xff000000) >> 24
		header[5] = (timestamp & 0x00ff0000) >> 16
		header[6] = (timestamp & 0x0000ff00) >> 8
		header[7] = timestamp & 0x000000ff
		header[8] = (ssrc & 0xff000000) >> 24
		header[9] = (ssrc & 0x00ff0000) >> 16
		header[10] = (ssrc & 0x0000ff00) >> 8
		header[11] = ssrc & 0x000000ff
		self.header = header
		self.payload = payload
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	
	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)
	
	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)
	
	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)
	
	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)
	
	def getPayload(self):
		"""Return payload."""
		return self.payload
		
	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload
