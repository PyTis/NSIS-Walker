"""
A simple script to encode all the images the wxPython program needs into a Python
module
"""
import sys, os, glob
import img2py
def main():
    output = '../src/util/images.py'
    doc = '''

    '''
    # get the list of PNG files
    files = glob.glob('*.png')
    # get the list of ICON files
    files.extend(glob.glob('*.bmp'))
    files.extend(glob.glob('*.ico'))
    files.extend(glob.glob('*.gif'))
    files.extend(glob.glob('*.jpg'))
    files.extend(glob.glob('*.jpeg'))
    files.sort()
    # Truncate the inages module
    handle = open(output, 'w')
    #handle.write(doc)
    # call img2py on each file
    for file in files:
        # extract the basename to be used as the image name
        name = os.path.splitext(os.path.basename(file))[0]
        # encode it
        if file == files[0]:
            cmd = "-u -i -n %s %s %s" % (name, file, output)
        else:
            cmd = "-a -u -i -n %s %s %s" % (name, file, output)
        img2py.main(cmd.split())

if __name__ == "__main__":
    main()