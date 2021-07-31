import os, sys, requests as req

ARGV    = sys.argv
URL     = "http://cloud.park-cloud.co19.kr:{}/"
PORT    = 5000
HOST    = URL.format(PORT)
route   = "helmet"
data    = {'state': ARGV[1]}

res     = req.post(HOST+route, data=data)
print(res)
print(res.status_code)
print(res.text)
