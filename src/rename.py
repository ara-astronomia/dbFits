import os
import pyfits
import shutil

bias = 1
dark = 1
dark_flat_r = 1
dark_flat_v = 1
dark_flat_b = 1

fr = 1
fv = 1
fb = 1

lr = 1
lv = 1
lb = 1

tr = '1.8'
tv = '3.0'
tb = '8.0'

i = 1
directory = '/home/ara/Scrivania/2011-09-09'
try:
  os.mkdir(directory + 'renamed')
except:
  print 'esiste'
for root, dirs, files in os.walk(directory):
  for file in files:
    if os.path.splitext(file)[-1] == '.fit' or os.path.splitext(file)[-1] == '.fts':
      file_path = root + "/" + file
      hdulist = pyfits.open(file_path)
      prihdr = hdulist[0].header
      imagetype = prihdr['IMAGETYP']
      try:  
        filtro = prihdr['FILTER']
      except:
        filtro = ''
      
      #if prihdr['EXPOSURE'] is not None and prihdr['EXPOSURE'] != '':
      #  exptime = prihdr['EXPOSURE']
      #else:
      exptime = prihdr['EXPTIME']
      
      if imagetype == 'LIGHT':
        if filtro == 'R':
          i = lr
          lr = lr + 1
        elif filtro == 'V':
          i = lv
          lv = lv + 1
        elif filtro == 'B':
          i = lb
          lb = lb + 1
      
      if imagetype == 'DARK':
        if str(exptime) == tr:
          i = dark_flat_r
          dark_flat_r = dark_flat_r + 1
        elif str(exptime) == tv:
          i = dark_flat_v
          dark_flat_v = dark_flat_v + 1
        elif str(exptime) == tb:
          i = dark_flat_b
          dark_flat_b = dark_flat_b + 1
        else:
          i = dark
          dark = dark + 1
      
      if imagetype == 'BIAS':
        i = bias
        bias = bias + 1
      
      if imagetype == 'FLAT':
        if filtro == 'R':
          i = fr
          fr = fr + 1
        if filtro == 'V':
          i = fv
          fv = fv + 1
        if filtro == 'B':
          i = fb
          fb = fb + 1
      if filtro != '':
        imagetype = imagetype + '_' + filtro
      newfile = directory + 'renamed/' + imagetype + '_' + str(exptime) + '_' + str(i)  + os.path.splitext(file)[-1] 
      shutil.copy2(file_path,newfile)
