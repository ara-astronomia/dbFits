# What does it do?
dbFit is a script that extrapolates in batch the fitsheader from astronomical images and a gui interface (in progress)

# How to use the batch?
python ${workspace}/dbFit/src/fits.py -i $image -o $csvname > $logfile

the above command creates a csv named $csvname with all the fitsheaders of the astronomical image found in directory $image
and log the operation in the log $logfile

# How to use the GUI
probabily it's useless yet :)
