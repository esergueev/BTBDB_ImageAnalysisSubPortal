#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ar'

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from app.core.preprocessing import resizeNii
import app.core.preprocessing as preproc
import common as comm

def getMinMaxLungZ(pmsk):
    zsum = np.sum(pmsk, axis=(0, 1))
    tmpz = np.where(zsum>0)[0]
    if len(tmpz)>0:
        zmin = tmpz[0]
        zmax = tmpz[-1]
        return (zmin, zmax)
    else:
        return (-1.,-1.)

if __name__ == '__main__':
    dataDir = '../../experimental_data/dataentry_test0'
    dbWatcher = comm.DBWatcher()
    dbWatcher.load(dataDir, isDropEmpty=True, isDropBadSeries=True)
    dbWatcher.printStat()
    for ii, ser in enumerate(dbWatcher.allSeries()):
        fmskLung = '%s-lungs.nii.gz' % ser.pathNii
        fmskLesion = '%s-lesion.nii.gz' % ser.pathNii
        # (1) load nii
        niiOrig = nib.load(ser.pathNii)
        niiLung = nib.load(fmskLung)
        niiLesion = nib.load(fmskLesion)
        # (2) split lungs
        retMskLungs, retIsOk = preproc.makeLungedMaskNii(niiLung)
        img = preproc.niiImagePreTransform(niiOrig.get_data())
        imgLung = preproc.makeLungedMaskNii(niiLung.get_data())
        imgLungsDiv = preproc.niiImagePreTransform(retMskLungs.get_data())
        imgMskLesion = preproc.niiImagePreTransform(niiLesion.get_data())
        # (3) preview
        sizPrv = 256
        nx = 4
        ny = 3
        # (4) calc percent of lesion volume in lung volume
        arrLbl = np.sort(np.unique(imgLungsDiv))
        threshLesion=0.5
        numZ = 4
        ret4Lung = dict()
        for ilbl in [1, 2]:
            if ii in arrLbl:
                lstLesionP = []
                mskLung = (imgLungsDiv == ilbl)
                zmin, zmax = getMinMaxLungZ(mskLung)
                arrz = np.linspace(zmin, zmax, numZ)
                mskLesion = imgMskLesion.copy()
                mskLesion[~mskLung] = 0
                mskLesion = (mskLesion>threshLesion)
                for zzi in range(numZ-1):
                    z1 = int(arrz[zzi + 0])
                    z2 = int(arrz[zzi + 1])
                    volMsk = float(np.sum(mskLung[:, :, z1:z2]))
                    volLesion = float(np.sum(mskLesion[:, :, z1:z2]))
                    if volMsk<1:
                        volMsk = 1.
                    lstLesionP.append(volLesion/volMsk)
                ret4Lung[ilbl] = lstLesionP
        print ('[%d] --> [%s]' % (ii, fmskLesion))