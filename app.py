# app.py - coronavirus death chart
# to install:
# pip3 install numpy
# pip3 install matplotlib
# pip3 install requests
# to run:
# python3 ./app.py

import requests
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

threshold=10

# 0=deaths, 1=confirmed cases
datatype=0

# Download the file from https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases
# Original wide form (new column for each day)
fname='./time_series_covid19_deaths_global.csv'
fname2='./time_series_covid19_confirmed_global.csv'
url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
fdata = requests.get(url+fname)
fdata2 = requests.get(url+fname2)
# write the file to the file system
open(fname, 'wb').write(fdata.content)
open(fname2, 'wb').write(fdata2.content)

# this function is used to plot any row (country)
def do_plot(row, name):
    temprow=tbl[row]
    tempc=np.array(temprow.tolist())[5:]
    tempthresh=tempc[tempc>threshold]
    idx=tempthresh.size
    if (idx>1):
        plt.plot(tempthresh)
        plt.text(idx-1, tempthresh[idx-1], name+'('+str(int(tempthresh[idx-1]))+')')

# this function is used to plot summed-up rows
# (needed for large countries with multiple regions, like China and Australia)
def do_plotsum(rowfirst, rowlast, name):
    temprow=tbl[rowfirst]
    tempc=np.array(temprow.tolist())[5:]
    i=rowfirst+1
    while 1:
        temprow=tbl[i]
        tempc=tempc+np.array(temprow.tolist())[5:]
        if (i==rowlast):
            break
        i=i+1
    tempthresh=tempc[tempc>threshold]
    idx=tempthresh.size
    if (idx>1):
        plt.plot(tempthresh)
        plt.text(idx-1, tempthresh[idx-1], name)

if datatype==0:
    f = open(fname, "r")
elif datatype==1:
    f = open(fname2, "r")
line=f.readline()
tblcolnames=line.split(',')
tbl=genfromtxt(f, delimiter=',', names=tblcolnames, usecols=np.arange(0,len(tblcolnames)))
f.close()

# row numbers (as viewed in Excel) for selected countries, subtract 2 to suit numpy
row_uk=225-2
row_us=227-2
row_italy=139-2
row_france=118-2
row_germany=122-2
row_spain=203-2
row_skorea=145-2
row_japan=141-2
row_chinafirst=51-2
row_chinalast=83-2
row_ausfirst=10-2
row_auslast=17-2
row_iran=135-2
row_venez=229-2
row_india=133-2
row_pak=179-2
row_russia=189-2
row_neth=171-2
row_belgium=25-2
row_bulgaria=32-2
row_bosnia=29-2
row_canadafirst=37-2
row_canadalast=47-2
row_serbia=196-2
row_turkey=215-2
row_romania=188-2
row_centafrica=48-2
row_southafrica=202-2
row_greece=124-2
row_sweden=207-2

# plot each country of interest
do_plot(row_uk, 'UK')
do_plot(row_us, 'US')
do_plot(row_italy, 'Italy')
do_plot(row_france, 'France')
do_plot(row_germany, 'Germany')
do_plot(row_spain, 'Spain')
do_plot(row_skorea, 'South Korea')
do_plot(row_japan, 'Japan')
do_plotsum(row_chinafirst, row_chinalast, 'China')
do_plotsum(row_ausfirst, row_auslast, 'Australia')
do_plot(row_iran, 'Iran')
do_plot(row_venez, 'Venezuela')
do_plot(row_india, 'India')
do_plot(row_pak, 'Pakistan')
do_plot(row_russia, 'Russia')
do_plot(row_neth, 'Netherlands')
do_plot(row_belgium, 'Belgium')
do_plot(row_bulgaria, 'Bulgaria')
do_plot(row_bosnia, 'Bosnia')
do_plotsum(row_canadafirst, row_canadalast, 'Canada')
do_plot(row_serbia, 'Serbia')
do_plot(row_turkey, 'Turkey')
do_plot(row_romania, 'Romania')
do_plot(row_centafrica, 'Central Africa')
do_plot(row_southafrica, 'South Africa')
do_plot(row_greece, 'Greece')
do_plot(row_greece, 'Sweden')

# tweak and then finally display the plot
plt.xlim(xmin=0)
plt.ylim(ymin=0)

# set x ticks
start, end = plt.xlim()
plt.xticks(np.arange(start, end, 2))
# set y ticks
start, end = plt.ylim()
plt.yticks(np.arange(start, end, 1000))


plt.gca().set_prop_cycle(None)
plt.grid()
if datatype==0:
    plt.title('Cumulative Deaths from Coronavirus')
    plt.xlabel('Number of days since '+str(threshold)+'th death')
    plt.ylabel('Cumulative number of deaths')
elif datatype==1:
    plt.title('Cumulative Reported Cases from Coronavirus')
    plt.xlabel('Number of days since '+str(threshold)+'th reported case')
    plt.ylabel('Cumulative number of cases')
plt.show()

