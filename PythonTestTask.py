import os,sys
import gzip
from urllib2 import Request, urlopen, URLError, HTTPError

debian_mirror_path = 'http://ftp.uk.debian.org/debian/dists/stable/main/' 
architectures = ['amd64','arm64','armel','armhf','i386','mips','mips64el','mipsel','ppc64el','s390x']
download_dir = './downloads/'

# download routine from urlib2 examples
# it's downloads file from given url and save it with given name
def download_file(url,name):
    req = Request(url)
    try:
        filedata = urlopen(url)
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
        exit()
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        exit()
    data = filedata.read()
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    with open(download_dir+name, 'wb') as f:
        f.write(data)

print('Python test task')

# arguments check
input_arguments = sys.argv[1:]
if ((len(input_arguments) != 1) or (input_arguments[0] not in architectures)):
    print 'usage: python '+__file__+' [ARCHITECTURE]'
    print 'avaliable architectures: '
    print ', '.join(architectures)
    exit()
selected_arch = input_arguments[0]

# downloading archive
content_name = 'Contents-'+selected_arch
archive_name = content_name+'.gz'
print 'downloading '+debian_mirror_path+archive_name+' ...'
download_file(debian_mirror_path + archive_name, archive_name)

# extracting archive to file
print 'extracting '+archive_name+' ...'
with gzip.open(download_dir+archive_name, 'r') as file_gz:
    with open(download_dir+content_name, 'w+') as file_data:
        file_data.write(file_gz.read())
        file_data.seek(0)

# appending packet names to huge dictionary and counting
        print 'counting packets ...'
        packages_dict = {}
        for line in file_data:
            pkg_name = line.split()[1]
            if (packages_dict.has_key(pkg_name)):
                packages_dict[pkg_name] += 1
            else:
                packages_dict[pkg_name] = 1

# sorting
        print 'finding top-10 ...'
        sorted_packages_dict = sorted(packages_dict.iteritems(), key=lambda (k, v): (-v, k))[:10]

# printing result
        print 'package name:'.ljust(40, ' ').rjust(44), 'number of files:'
        i=1
        for pkg_name, number_of_lines in sorted_packages_dict:
            print str(i).rjust(2), pkg_name.ljust(40, '.').rjust(41), number_of_lines
            i+=1
