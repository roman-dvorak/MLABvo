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
                filepath = str(self.get_argument('filepath'))
                checksum = str(self.get_argument('checksum', None))
                id_observer = int(self.get_argument('id_station', 0))
                station = str(self.get_argument('station', None))
                id_server = int(self.get_argument('id_server', 1)) # 1 je space.astro.cz
                uploadtime = str(self.get_argument('uploadtime', datetime.datetime.now()))
                lastaccestime = str(self.get_argument('lastaccestime', datetime.datetime.now()))
                indextime = str(self.get_argument('indextime', '0000-00-00 00:00:00'))

                id_station = _sql("SELECT id FROM bolidozor_station WHERE namesimple = '%s'" %(station))

                if len(id_station) == 0:    # pokud stanice neexistuje - vytvorit
                    _sql("INSERT INTO `MLABvo`.`bolidozor_station` (`name`, `namesimple`, `status`, `observatory`, `web`, `owner`, `hardware`, `comment`) VALUES ('%s', '%s', '10', '0', '0', '0', 'New station - automatically created', NOW());" %(station, station))
                    id_station = _sql("SELECT id FROM bolidozor_station WHERE namesimple = '%s'" %(station))

                id_station = id_station[0][0]
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

        elif project == 'meteor-observer':
            print "project", project, adr

            time = str(self.get_argument('time', None))
            trail_beg = str(self.get_argument('trail_beg', None))
            trail_end = str(self.get_argument('trail_end', None))
            loc_lat = str(self.get_argument('loc_lat', None))
            loc_lon = str(self.get_argument('loc_lon', None))
            observer_id = str(self.get_argument('observer_id', None))

            f = open('/home/roman/meteor-observer', 'a')
            f.write(observer_id + ',' + time + ',' + trail_beg + ',' + trail_end+ ',' +loc_lat+ ',' +loc_lon+ '\n')  
            f.close() 

            print "MeteorObserver:", observer_id, time, trail_beg, trail_end, loc_lat, loc_lon
            return self.write("ACK")

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
            return self.write("ERR, neznamy projekt: %s" %project)

'''
meteor-observer
project meteor-observer upload/meteor-observer
[I 170430 21:53:52 web:1908] 200 GET /upload/meteor-observer?time=1493589204594&trail_beg=%5B-0.9879979491233826%2C+0.1355455070734024%2C+0.07407671958208084%5D&trail_end=%5B0.6910881400108337%2C+0.6931741833686829%2C+0.2047112137079239%5D&loc_lat=0.0&loc_long=0.0&observer_id=unnamed-e1e9699a-3c4f-484d-b342-d815a9652b6e (127.0.0.1) 1.51ms
'''
