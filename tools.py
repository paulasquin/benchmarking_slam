import subprocess

from PIL import Image

def get_files_names(extension, path=""):
    """" Send a list of file with given extension under given (optional) path.
    Path can be relative or absolute
    example : '.pgm', 'carte' """
    p = subprocess.Popen(["ls", path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', extension], stdin=p.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = p2.communicate()
    names = out.decode('utf-8')
    names = names.split('\n')
    names.pop()  # We delete last, empty, element
    return names

def getImage(filename, path=""):
    """" Load an image with given filename and path (optional) """
    if path != "":
        path += "/"
    return Image.open(path + filename)
