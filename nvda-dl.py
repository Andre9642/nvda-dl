import hashlib, json, optparse, os.path, urllib 
from urllib.request import quote

versionTypeS = ["stable", "beta", "alpha"]
versionAliases = {"alpha": "snapshot:alpha"}
url = "https://www.nvaccess.org/nvdaUpdateCheck?autoCheck=False&allowUsageStats=False&version={version}&versionType={versionType}&osVersion=10.0.19619+workstation&x64=True"

def sha1sum(filename):
	h = hashlib.sha1()
	b = bytearray(128*1024)
	mv = memoryview(b)
	with open(filename, 'rb', buffering=0) as f:
		for n in iter(lambda : f.readinto(mv), 0):
			h.update(mv[:n])
	return h.hexdigest()

def parseResponse(res):
	o = {}
	lines = res.strip().replace('\r', '').split('\n')
	for line in lines:
		if not ':' in line: raise ValueError(line)
		line = line.strip().split(':', 1)
		o[line[0]] = line[1].strip()
	return o

def processDL(data):
	if not isinstance(data, dict): raise TypeError("wrong type")
	hash = data["launcherHash"]
	url = data["launcherUrl"].split('?')[0]
	fileName = url.split('/')[-1]
	if not os.path.exists(DOWNLOAD_DIR):
		os.mkdir(DOWNLOAD_DIR)
	fp = os.path.join(DOWNLOAD_DIR, fileName)
	if os.path.exists(fp) and os.path.isfile(fp):
		print(f"* File seems already downloaded ({fileName})...", end=' ', flush=1)
		hash2 = sha1sum(fp)
		hashSame = hash2 == hash
		print("hashes %s" % "match, skipping" if hashSame else "don't match", flush=1)
		if hashSame: return
	try:
		print(f"Downloading {fileName}...", flush=1, end=' ')
		urllib.request.urlretrieve(url, fp)
		print("done", flush=1)
		print("Checking hash...", flush=1, end=' ')
		hash2 = sha1sum(fp)
		hashSame = hash2 == hash
		print("OK" if hashSame else "KO, retrying")
		if not hashSame:
			urllib.request.urlretrieve(url, fp)
			hash2 = sha1sum(fp)
			print("hashes %s" % ("match" if hash2 == hash else "don't match"), flush=1)
	except urllib.error.HTTPError:
		print("failure")
		print(f"! Invalid URL: {url}", flush=1)

def download(versionType):
	if versionType in versionAliases.keys():
		versionType = versionAliases[versionType]
	url_ = url.format(version="2019.3", versionType=quote(versionType))
	try:
		with urllib.request.urlopen(url_) as res:
			text = res.read().decode()
			res = parseResponse(text)
			processDL(res)
	except urllib.error.HTTPError:
		print(f"! Invalid URL: {url_}", flush=1)



def downloadAll(versionTypes=versionTypeS):
	for versionType in versionTypes:
		print(f": Processing {versionType} version", flush=1)
		download(versionType)

parser = optparse.OptionParser()
parser.add_option('-d', "--download-dir",
	action="store", dest="DOWNLOAD_DIR", help="download dir", default='.')
parser.add_option('-t', '--version-type',
	action="append", dest="versionTypes", type = "choice", choices=versionTypeS,
	help=f"version type ({', '.join(versionTypeS)})", default=[])

options, args = parser.parse_args()

DOWNLOAD_DIR = options.DOWNLOAD_DIR
versionTypes = options.versionTypes or versionTypeS
print(f"Download dir: {DOWNLOAD_DIR}")
downloadAll(versionTypes)
