import os, fnmatch

lingvolive_certpath = "./lingvocert/lingvolive_cert1.pem"

def locate(certfile="cacert.pem", root=os.curdir):
    matches = []
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, certfile):
            matches.append(os.path.join(path, filename))
    return matches

def addcert(certfile, nucert):
    with open(certfile, 'a') as cert:
        with open(nucert) as nucert:
            cert.write(nucert.read())

certfiles = locate()
for certfile in certfiles:
    addcert(certfile, lingvolive_certpath)

