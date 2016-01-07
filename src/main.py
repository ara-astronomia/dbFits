#!/usr/bin/env python
"""
__version__ = "$Revision: 1.00 $"
__date__ = "$Date: 2004/04/24 22:13:31 $"
"""
from PythonCard import model
import os
import sqlite3
import pyfits

configFile = 'dbfit.ini'
class Main(model.Background):
            
    def on_initialize(self, event):
        import ConfigParser
        self.parser = ConfigParser.RawConfigParser()
        self.parser.read( configFile )
        self.components.db.text = self.parser.get('dbFit','db')
        self.components.cartelle.text = self.parser.get('dbFit','cartelle')
        self.resetDbText = self.components.db.text
        self.resetCartelleText = self.components.cartelle.text

#    def on_idle(self, event):
#        print "on_idle entered"
#        self.components.message.text = ""

    def on_save_mouseClick(self, event):
        self.parser.set('dbFit','db',self.components.db.text)
        self.parser.set('dbFit','cartelle',self.components.cartelle.text)
        with open(configFile, 'wb') as configfile:
            self.parser.write(configfile)
        self.components.message.text = "Impostazioni salvate"
        
    def on_upBtn_mouseClick(self, event):
        self.fai(self.components.db.text,self.components.cartelle.text)

    def on_upDateBtn_mouseClick(self, event):
        self.aggiorna_date(self.components.db.text)

    def on_resetBtn_mouseClick(self, event):
        self.components.db.text = self.resetDbText
        self.components.cartelle.text = self.resetCartelleText

    def conn(self,sqlitedb):
        if not os.path.exists(sqlitedb):
            #create new DB, create table fits_headers
            conn = sqlite3.connect(sqlitedb)
            c = conn.cursor()
            c.execute('''CREATE TABLE "fits_headers" ("id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "FILENAME" varchar(255), "SIMPLE" varchar(255), "NAXIS1" integer, "NAXIS2" integer, "DATE_OBS" datetime, "EXPOSURE" integer, "SET_TEMP" integer, "CCD_TEMP" decimal, "XPIXSZ" integer, "YPIXSZ" integer, "XBINNING" integer, "YBINNING" integer, "FILTER" varchar(255), "IMAGETYP" varchar(255), "FOCUSPOS" integer, "FOCUSTEM" decimal, "OBJCTRA" varchar(255), "OBJCTDEC" varchar(255), "OBJCTALT" decimal, "OBJCTAZ" decimal, "OBJCTHA" decimal, "SITELAT" varchar(255), "SITELONG" varchar(255), "AIRMASS" decimal, "FOCALLEN" integer, "APTDIA" integer, "APTAREA" decimal, "OBJECT" varchar(255), "TELESCOP" varchar(255), "INSTRUME" varchar(255), "OBSERVER" varchar(255), "NOTES" varchar(255), "RDNOISE" integer, "GAIN" decimal, "p_invest" varchar(255))''')
            #c.execute('''CREATE UNIQUE INDEX "index_fits_headers_on_DATE_OBS" ON "fits_headers" ("DATE_OBS")''')
            c.execute('''CREATE UNIQUE INDEX "index_fits_headers_on_FILENAME" ON "fits_headers" ("FILENAME")''')
            print("Creo il db e mi connetto")
        else:
            #use existing DB
            conn = sqlite3.connect(sqlitedb)
            c = conn.cursor()
            print("Db esistente, mi connetto")
        return conn

    def get_header(self,prihdr):
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

    def fai(self,sqlitedb,path):
        conn = self.conn(sqlitedb)
        c = conn.cursor()
        id = None
        new = 0
        err = 0
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if os.path.splitext(file)[-1] == '.fit' or os.path.splitext(file)[-1] == '.fts':
                        file_path = root + "/" + file
                        try:
                            hdulist = pyfits.open(file_path)
                            prihdr = hdulist[0].header
                            headers = self.get_header(prihdr)
                            try:
                                if headers[4] is not None and headers[4] != '' and len(headers[3]) == 10:
                                    headers[3] = str(headers[3])+"T"+headers[4]
                                if headers[5] is None or headers[5] == '':
                                    headers[5] = str(headers[6])
                                if headers[8] is None or headers[8] == '':
                                    headers[8] = str(headers[9])
                                #print headers[3]
                                del headers[4]
                                #print headers[4]
                                del headers[5]
                                #print headers[5]
                                del headers[7]
                                list = [id, file_path] + headers
                                #c.execute('insert into fits_headers values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', list)
                                #csv = open("fits.csv",  "a")
                                for field in list:
                                    print(field)
                                    #csv.write(field)
                                #csv.close()
                                new += 1
                            except:
                                print("i dati sono presenti nel db per: "+file_path)
                            conn.commit()
                            hdulist.close()
                        except:
                            err += 1
                            print("errore nel fits header, file non inserito: "+file_path)
            if new is not 0:
                result =  "Nuovi dati inseriti nel db: "+str(new)+" fits header aggiunti."
            else:
                result =  "Nessun cambiamento nel db"
            if err is not 0:
                result = result+". Ci sono stati "+str(err)+" errori."
        except:
            conn.rollback()
            result =  "Ci sono stati degli errori, dati non aggiornati"
        c.close()
        self.components.message.text = result

    def aggiorna_date(self,sqlitedb):
        conn = self.conn(sqlitedb)
        c = conn.cursor()
        c.execute("select * from fits_headers")
        tab = c.fetchall()
        for row in tab:
            if len(str(row[5]).split('/')) > 1:
                day, month, year = str(row[5]).split('/')
                prith = '20'+year+'-'+month+'-'+day
                print(str(len(row[5].split('/')))+" "+row[5])
                print(prith)
                update_tuple = (prith, row[5])
                try:
                    c.execute('update fits_headers set DATE_OBS = ? where DATE_OBS = ?', update_tuple)
                except:
                    print("errore")
            if row[5] == "":
                update_tuple = ('1900-01-01T00:00:00', row[5])
                try:
                    c.execute('update fits_headers set DATE_OBS = ? where DATE_OBS = ?', update_tuple)
                except:
                    print("errore")
        conn.commit()
        c.close()
        self.components.message.text = "Aggiornamento date eseguito"

if __name__ == '__main__':
    app = model.Application(Main)
    app.MainLoop()
