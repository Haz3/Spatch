#!/usr/bin/python

import json, urllib, urllib2, argparse, hashlib, re, sys
from pprint import pprint

class vtAPI():
    def __init__(self):
        self.api = '3f88f595761dffe7b9123923227afb21e2edaa6826b58df3ae88d6cc0554f776'
        self.base = 'https://www.virustotal.com/vtapi/v2/'

    def getReport(self,md5):
        param = {'resource':md5,'apikey':self.api}
        url = self.base + "file/report"
        data = urllib.urlencode(param)
        result = urllib2.urlopen(url,data)
        jdata =  json.loads(result.read())
        return jdata

    def rescan(self,md5):
        param = {'resource':md5,'apikey':self.api}
        url = self.base + "file/rescan"
        data = urllib.urlencode(param)
        result = urllib2.urlopen(url,data)
        print "\n\tVirus Total Rescan Initiated for -- " + md5 + " (Requery in 10 Mins)"


# Md5 Function

def checkMD5(checkval):
  if re.match(r"([a-fA-F\d]{32})", checkval) == None:
    md5 = md5sum(checkval)
    return md5.upper()
  else:
    return checkval.upper()

def md5sum(filename):
  fh = open(filename, 'rb')
  m = hashlib.md5()
  while True:
      data = fh.read(8192)
      if not data:
          break
      m.update(data)
  return m.hexdigest()

def parse(it, md5, verbose, jsondump):
  if it['response_code'] == 0:
    print md5 + " -- Not Found in Virus Total"
    return 0

  print"Results for MD5: " ,it['md5']
  print"Detected by: ", it['positives'], '/', it['total']

  if 'Sophos' in it['scans']:
    print'Sophos Detection:', it['scans']['Sophos']['result']

  if 'Kaspersky' in it['scans']:
    print'Kaspersky Detection:', it['scans']['Kaspersky']['result']

  if 'ESET-NOD32' in it['scans']:
    print'ESET Detection:', it['scans']['ESET-NOD32']['result']

  print'Scanned on:',it['scan_date']

  if jsondump == True:
    with open("Json/dump_" + md5 + ".json", "w") as jsondumpfile:
        jsondumpfile.write(json.dumps(it, sort_keys=True, indent=4))

    print "\ncJSON Written to File -- " + "Json/dump_" + md5 + ".json"

  if verbose == True:
    print '\n\tVerbose VirusTotal Information Output:\n'
    for x in it['scans']:
     print '\t', x, '\t' if len(x) < 7 else '','\t' if len(x) < 14 else '','\t',it['scans'][x]['detected'], '\t',it['scans'][x]['result']


def main():
    opt = argparse.ArgumentParser(description="Search from VirusTotal")
    opt.add_argument("HashorPath", help="Enter the MD5/SHA1/256 Hash or Path to File")
    opt.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="Turn on verbosity of VT reports")
    opt.add_argument("-j", "--jsondump", action="store_true",help="Dumps the full VT report to file (VTDLXXX.json)")
    opt.add_argument("-r", "--rescan",action="store_true", help="Force Rescan with Current A/V Definitions")

    if len(sys.argv)<=2:
        opt.print_help()
        sys.exit(1)

    options = opt.parse_args()
    vt = vtAPI()
    md5 = checkMD5(options.HashorPath)

    parse(vt.getReport(md5), md5 ,options.verbose, options.jsondump)

    if options.rescan:
        vt.rescan(md5)

if __name__ == '__main__':
    main()
