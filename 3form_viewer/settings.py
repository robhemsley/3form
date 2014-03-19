
#General
_PORT_NUM           = 8088
host = "um.media.mit.edu"


#Slic3r
#/Users/rob/Documents/Fall 2013/Machine/AutoSend/support/slicer/slic3r/Slic3r_1.0.1RC3.app
_slic3r_exe         = "/Applications/Repetier-Host Mac.app/Contents/Resources/Slic3r.app/Contents/MacOS/slic3r"

_tmp_dir            = "tmp/"

#Error Messages
_ERROR_MSGS         = {"TMS_ID_NOT_FOUND": '{"error_num": "1", "msg": "tms id not found"}',
                       "SPECIFY_API_VERSION": '{"error_num": "2", "msg": "api version required"}',
                       "CONVERTING_FILE": '{"error_num": "3", "msg": "converting requested file"}',
                       "NO_TMS_ID": '{"error_num": "4", "msg": "no tmsID found}',
                       "PROGRAM_ADDED": '{"error_num": "5", "msg": "program added to queue}',
                       "PROGAM_NOT_FOUND": '{"error_num": "6", "msg": "program could not be found}',
                       "DVR_NO_CHANNEL": '{"error_num": "7", "msg": "channel not available to record}'}