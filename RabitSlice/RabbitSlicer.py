#!/usr/bin/env python
import pika, sys, settings, time, json, urllib2, uuid, os, requests
import subprocess as sub
    
class RabbitSlicer():

    def __init__(self, host = None):
        self.host = host
        if self.host == None:
            self.host = settings.host
            
        self.rmq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.host))
        self.rmq_channel = self.rmq_connection.channel()

        self.rmq_channel.queue_declare(queue='stlSlice', durable=True)
        self.rmq_channel.basic_qos(prefetch_count=1)
        self.rmq_channel.basic_consume(self.queueMsg, queue='stlSlice')        
    
    def startMQ(self):
        print "Starting RabbitSlicer"
        self.rmq_channel.start_consuming()
        
    def queueMsg(self, ch, method, properties, body):
        jsonObj = json.loads(body)
        
        try:
            self._setStatus(jsonObj["callback"]["progress"], jsonObj["id"], "10")
        
            stl = jsonObj["stl"]
            slicer = jsonObj["slicer"]

            print "\n\n\tReceived %(filename)s %(id)s - %(time)s" % ({"id": jsonObj["id"], "filename": stl["filename"], "time": time.strftime("%x %X")})
    
            tmpID = uuid.uuid4().hex
            tmpStlFilename = "%s%s.tmp.stl"% (settings._tmp_dir, tmpID)
            tmpGcodeFilename = "%s%s.tmp.gcode"% (settings._tmp_dir, tmpID)
            tmpSlicerFilename = "%s%s.tmp.ini"% (settings._tmp_dir, tmpID)
    
            f = open(tmpSlicerFilename, "w")
            f.write(slicer)
            f.close()
    
            print stl["url"]
            tmpDownload = DownloadFile(stl["url"], tmpStlFilename)
            tmpFilename = tmpDownload.download()
            if tmpFilename == None:
                print "\tdownload failed"
    
            tmp_filename = self._sliceFile(jsonObj["id"], tmpStlFilename, stl["position"]["x"], stl["position"]["y"], stl["position"]["z"], tmpSlicerFilename, tmpGcodeFilename, jsonObj["callback"]["progress"])
         
            if "callback" in jsonObj:
                self._sendFile(tmpGcodeFilename, stl["filename"], jsonObj, jsonObj["callback"]["complete"])
    
            os.remove(tmpStlFilename)
            os.remove(tmpGcodeFilename)
            os.remove(tmpSlicerFilename)
            print "\tDone - %s"% (stl["filename"])
        
            self._setStatus(jsonObj["callback"]["progress"], jsonObj["id"], "100")
        
        except Exception as er:
            print er
        
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def _sendFile(self, tmpfilename, filename, usrData, callback):
        try:
            fileobj = open(tmpfilename, 'rb')
            r = requests.post(callback, data=usrData, files={"gcode": (os.path.basename(filename), fileobj)})
        except Exception as err:
            print "\t"+str(err)
        
    def _sliceFile(self, id, stl_file, x, y, z, slicer_ini, gcode_file, callback):
        print "\tSlicing"
        load_cmd = "--load \"%s\""%(slicer_ini)
        cmd = "\"%(exe)s\" %(load_cmd)s --print-center %(x)f,%(y)f --z-offset %(z)f -o \"%(output_file)s\" \"%(stl_file)s\""% ({"x": x, "y": y,"z": z, "exe": settings._slic3r_exe, "output_file": gcode_file, "stl_file": stl_file, "load_cmd": load_cmd})

        print cmd
        p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        
        steps = 0 
        per = 100/11

        while True:
            nextline = p.stdout.readline()
            if nextline == '' and p.poll() != None:
                break
            
            if "=>" in nextline:
                steps += 1
                self._setStatus(callback, id, (steps*per))
                print "\t\t"+nextline.rstrip()
                
            else:
                if "Filament" in nextline:
                    filament = nextline[nextline.index(":")+2:].split(" ")
                    mm = filament[0]
                    cm = filament[1] 
                    
                elif "Process" in nextline:
                    timeData = nextline[nextline.index("took")+1:].split(" ")
                    mins = timeData[1]
                    secs = timeData[4]                
            
        print "\tSliced - %s Mins & %s Seconds"% (mins, secs)
        
        output, errors = p.communicate()
        return gcode_file
        
    def _setStatus(self, callback, id, status):
        try:
            r = requests.post(callback, data={"id": id, "progress": (status)})
        except Exception as err:
            print "\t"+str(err)
        
class DownloadFile():    

    def __init__(self, url, filename):
        self.filename = filename
        self.url = url
    
    def download(self):
        try:
            response = urllib2.urlopen(self.url);
            self.chunk_read(response, self.url, self.filename, report_hook=self.chunk_report) 
            
        except Exception:
            return None
            
        return self.filename
 
        
    def chunk_report(self, bytes_so_far, chunk_size, total_size):
        percent = float(bytes_so_far) / total_size
        percent = round(percent*100, 2)
    
    def chunk_read(self, response, url, filename, chunk_size=8192, report_hook=None):
        
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0
        
        print "\tDownloading: %s - %i mb"%(url, ((total_size/1024)/1024))
        start_time = time.time()
        file_out = open(filename, 'wb')
    
        while 1:
            chunk = response.read(chunk_size)
            bytes_so_far += len(chunk)
    
            if not chunk:
                break
            
            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)
                
            file_out.write(chunk)
    
        file_out.close()
        print "\tDownloaded: %s - %i Sec"%(url, int(time.time()-start_time))
        return bytes_so_far
        
if __name__ == "__main__":
    test = RabbitSlicer()
    test.startMQ()
