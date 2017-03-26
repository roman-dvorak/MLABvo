#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *
from . import _sql

import tornado.escape
import tornado.web

import glob
import time
import datetime


class api(tornado.web.RequestHandler):    # /rosapi/publist/(.*)

    def get(self, adr):
        project = adr.split('/')[1]
        print project
        
        if project == 'api' or project == 'upload': #TODO zde odstranit (je to tu pro zpetnou kompatibilitu od 2017/03), nyni se pouziva api.vo.mlab.cz/bolidozor/dataUpload...
            project = adr.split('/')[2]
            print project
            
        if project ==  'bolidozor':
            requestType = str(self.get_argument('requestType', 'dataUploaded'))
            
            if requestType == "dataUploaded":

                filename = str(self.get_argument('filename', None))
                filename_original = str(self.get_argument('filename_original', filename))
                filepath = str(self.get_argument('filepath', self.get_argument('filelocation', None)))  #TODO zde odstranit prijmani parametru filelocation (je to tu pro zpetnou kompatibilitu od 2017/03), nyni se pouziva parametr filepath
                checksum = str(self.get_argument('checksum', None))
                id_observer = int(self.get_argument('id_station', 0))
                station = str(self.get_argument('station', None))
                id_server = int(self.get_argument('id_server', 1)) # 1 je space.astro.cz
                uploadtime = str(self.get_argument('uploadtime', datetime.datetime.now()))
                lastaccestime = str(self.get_argument('lastaccestime', datetime.datetime.now()))
                indextime = str(self.get_argument('indextime', '0000-00-00 00:00:00'))

                id_station = _sql("SELECT id FROM bolidozor_station WHERE namesimple = '%s'" %(station))[0][0]
                #print id_station
                _sql("REPLACE INTO `MLABvo`.`bolidozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_station, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))
                
                return self.write("ACK<br> New bolidozor file was indexed")

        elif project ==  'ionozor':
            requestType = str(self.get_argument('requestType', 'dataUploaded'))
            
            if requestType == "dataUploaded":

                filename = str(self.get_argument('filename', None))
                filename_original = str(self.get_argument('filename_original', filename))
                filepath = str(self.get_argument('filepath', self.get_argument('filelocation', None))) #TODO zde odstranit prijmani parametru filelocation (je to tu pro zpetnou kompatibilitu od 2017/03)
                checksum = str(self.get_argument('checksum', None))
                id_observer = int(self.get_argument('id_station', 0))
                station = str(self.get_argument('station', None))
                id_server = int(self.get_argument('id_server', 1)) # 1 je space.astro.cz
                uploadtime = str(self.get_argument('uploadtime', datetime.datetime.now()))
                lastaccestime = str(self.get_argument('lastaccestime', datetime.datetime.now()))
                indextime = str(self.get_argument('indextime', '0000-00-00 00:00:00'))

                #id_station = _sql("SELECT id FROM ionozor_station WHERE namesimple = '%s'" %(station))[0][0]
                #print id_station

                _sql("REPLACE INTO `MLABvo`.`ionozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))
                #print "REPLACE INTO `MLABvo`.`ionozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum)

                return self.write("ACK<br> New Ionozor file was indexed")

        elif project ==  'geozor':
            requestType = str(self.get_argument('requestType', 'dataUploaded'))
            
            if requestType == "dataUploaded":

                filename = str(self.get_argument('filename', None))
                filename_original = str(self.get_argument('filename_original', filename))
                filepath = str(self.get_argument('filelocation', None))
                checksum = str(self.get_argument('checksum', None))
                id_observer = int(self.get_argument('id_station', 0))
                station = str(self.get_argument('station', None))
                id_server = int(self.get_argument('id_server', 1)) # 1 je space.astro.cz
                uploadtime = str(self.get_argument('uploadtime', datetime.datetime.now()))
                lastaccestime = str(self.get_argument('lastaccestime', datetime.datetime.now()))
                indextime = str(self.get_argument('indextime', '0000-00-00 00:00:00'))

                #id_station = _sql("SELECT id FROM ionozor_station WHERE namesimple = '%s'" %(station))[0][0]
                #print id_station

                _sql("REPLACE INTO `MLABvo`.`geozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))
                #print "REPLACE INTO `MLABvo`.`geozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s';" %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum)

                return self.write("ACK<br> New Ionozor file was indexed")
        else: 
            print "ERR, api #1"
            return self.write("ACK<br> New Ionozor file was indexed")