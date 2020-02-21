import os
from astropy.io import fits as pyfits
import sys
import getopt

def get_header(prihdr):
    #use this list
    header = ['SIMPLE', 'NAXIS1', 'NAXIS2', 'DATE-OBS', 'TIME-OBS', 'EXPOSURE',
        'EXPTIME', 'SET-TEMP', 'CCD-TEMP', 'TEMPERAT', 'XPIXSZ', 'YPIXSZ', 'XBINNING',
        'YBINNING', 'FILTER', 'IMAGETYP', 'FOCUSPOS', 'FOCUSTEM', 'OBJCTRA', 'OBJCTDEC',
        'OBJCTALT', 'OBJCTAZ', 'OBJCTHA', 'SITELAT', 'SITELONG', 'AIRMASS',
        'FOCALLEN', 'APTDIA', 'APTAREA', 'OBJECT', 'TELESCOP', 'INSTRUME',
        'OBSERVER', 'NOTES', 'RDNOISE', 'GAIN', 'P_INVEST']
    #insert fitsheader in a new list and return
    headerList = []
    for th in header:
        try:
            prith = prihdr[th]
            if th == 'DATE-OBS' and len(prith.split('/')) > 1:
                day, month, year = prith.split('/')
                prith = '20'+year+'-'+month+'-'+day
            if th == 'DATE-OBS' and (prith == '' or prith is None):
                prith = '1900-01-01T00:00:00'
            headerList.append(prith)
        except:
            headerList.append("")
    return headerList

def main(argv):
    new = 0
    err = 0

    inputdir = '/media/ara/Immagini/src'
    outputfile = '/home/ara/dbFit/src/fits.csv'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputdir> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputdir> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    csv = open(outputfile,  "a")
    for root, dirs, files in os.walk(inputdir):
        for file in files:
            if os.path.splitext(file)[-1] == '.fit' or os.path.splitext(file)[-1] == '.fts':
                file_path = root + "/" + file
                hdulist = pyfits.open(file_path)
                prihdr = hdulist[0].header
                headers = get_header(prihdr)
                if headers[4] is not None and headers[4] != '' and len(headers[3]) == 10:
                    headers[3] = str(headers[3])+"T"+headers[4]
                if headers[5] is None or headers[5] == '':
                    headers[5] = str(headers[6])
                if headers[8] is None or headers[8] == '':
                    headers[8] = str(headers[9])
                print(headers[3])
                del headers[4]
                print(headers[4])
                del headers[5]
                print(headers[5])
                del headers[7]
                list = [ file_path ] + headers
                #c.execute('insert into fits_headers values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', list)
                for field in list:
                    csv.write(str(field)+";#;")
                csv.write("\n")
                new += 1
                hdulist.close()
    csv.close()
    if new != 0:
        result =  "Nuovi dati inseriti nel db: "+str(new)+" fits header aggiunti."
    else:
        result =  "Nessun cambiamento nel db"
    if err != 0:
        result = result+". Ci sono stati "+str(err)+" errori."
    print(result)

if __name__ == "__main__":
   main(sys.argv[1:])
