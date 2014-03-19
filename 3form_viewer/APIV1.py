import settings

import uuid
import os, sys, requests, WebHandlers, pika, json

import subprocess as sub

from twisted.web.static import File

# Import Twisted 
from twisted.web.server import NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.host))
channel = connection.channel()

channel.queue_declare(queue='stlSlice', durable=True)

state = {}

class API1(Resource):
    
    def __init__(self,):
        Resource.__init__(self)
        self.putChild('slice', APISlice()) 
        self.putChild('complete', APIComplete()) 
        self.putChild('progress', APIProgress()) 
        self.putChild('gcode', APIGcode()) 
        self.putChild('stl', APIStl()) 

    def getChild(self, path, request):
        if path == '':
            return self
        
        if len(request.postpath) >= 1:
            return APITMSID(path)
        
        return Resource.getChild(self, path, request)

    def render_GET(self, request):
        return settings._ERROR_MSGS["SPECIFY_API_VERSION"]
        
class APIGcode(Resource):
    
    def getChild(self, name, request):  
        if name == '':
            return self
        
        return Resource.getChild(self, name, request)

    def render_GET(self, request):        
        request.setHeader('Content-Type', 'text/text')
        filename = settings._tmp_dir+request.args["id"][0]+".gcode"
        data = open(filename, 'r').read()
        os.remove(filename)
        return data
        
    def render_POST(self, request):        
        request.setHeader('Content-Type', 'text/plain')
        filename = settings._tmp_dir+request.args["id"][0]+".gcode"
        data = open(filename, 'r').read()
        os.remove(filename)
        return data
        
class APIStl(Resource):
    
    def getChild(self, name, request):  
        if name == '':
            return self
        
        return Resource.getChild(self, name, request)

    def render_GET(self, request):        
        request.setHeader('Content-Type', 'text/plain')
        filename = settings._tmp_dir+request.args["id"][0]+".stl"
        data = open(filename, 'r').read()
        os.remove(filename)
        return data
        
    def render_POST(self, request):        
        request.setHeader('Content-Type', 'text/plain')
        filename = settings._tmp_dir+request.args["id"][0]+".stl"
        data = open(filename, 'r').read()
        os.remove(filename)
        return data
        
class APIProgress(Resource):
    
    def getChild(self, name, request):  
        if name == '':
            return self
        
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        if request.args["id"][0] not in state:
            state[request.args["id"][0]] = 0
            
        return str(state[request.args["id"][0]])
        
    def render_POST(self, request):
        state[request.args["id"][0]] = request.args["progress"][0]
        
        return str(state[request.args["id"][0]])
        
class APIComplete(Resource):
    
    def getChild(self, name, request):  
        if name == '':
            return self
        
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "cats"
        
    def render_POST(self, request):
                        
        tmp_filename_gcode = request.args["id"][0]+".gcode"
        f = open(settings._tmp_dir+tmp_filename_gcode, "w")
        f.write(request.args["gcode"][0])
        f.close()
        
        return request.args["gcode"][0]
    
class APISlice(Resource):
    
    def getChild(self, name, request):  
        if name == '':
            return self
        
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        """gcode_file = self.sliceSTL("/Users/rob/Library/Repetier/tempobj.stl", "/Users/rob/Library/Repetier/tempobj.stl.gcode")
        
        request.setHeader("content-disposition","attachment;filename=%s"% (os.path.basename(gcode_file)))
        return open(gcode_file, 'r').read()"""
        return ""
        
    def render_POST(self, request):
        for key, value in request.args.iteritems():
            print key
            if key != "stl":
                print value

        if "stl" not in request.args:
            return "Error"
            
        x = y = z = 0
        if "x" in request.args:
            x = float(request.args["x"][0])
        if "y" in request.args:
            y = float(request.args["y"][0])
        if "z" in request.args:
            z = float(request.args["z"][0])
                    
        uid = uuid.uuid4()
        tmp_filename_stl = settings._tmp_dir+uid.hex+".stl"
        f = open(tmp_filename_stl, "w")
        f.write(request.args["stl"][0])
        f.close()
        
        print x, y, z
        
        message = {"stl": {"filename": "octocat.stl", "url": "http://localhost:8088/v1/stl/?id="+uid.hex, "position": {"x": x, "y": y, "z": z}},
        "slicer": """
        support_material_extrusion_width = .31
        infill_acceleration = 0
        slowdown_below_layer_time = 30
        skirt_distance = 5
        extra_perimeters = 1
        travel_speed = 75
        min_skirt_length = 0
        bridge_flow_ratio = 1
        support_material_angle = 0
        fan_below_layer_time = 30
        toolchange_gcode = 
        raft_layers = 2
        threads = 4
        infill_speed = 60
        temperature = 215
        output_filename_format = [input_filename_base].gcode
        first_layer_bed_temperature = 105
        retract_before_travel = 2
        resolution = 0
        first_layer_temperature = 215
        first_layer_acceleration = 0
        layer_height = 0.200
        support_material_threshold = 45
        skirt_height = 1
        z_offset = 0
        support_material_interface_layers = 4
        avoid_crossing_perimeters = 0
        default_acceleration = 0
        extrusion_width = .42
        layer_gcode = 
        top_infill_extrusion_width = .42
        gcode_flavor = reprap
        fill_pattern = honeycomb
        retract_speed = 150
        first_layer_height = .3500
        retract_length_toolchange = 3
        use_relative_e_distances = 0
        support_material = 1
        end_gcode = 
        only_retract_when_crossing_perimeters = 0
        overhangs = 1
        support_material_interface_spacing = 0
        solid_fill_pattern = rectilinear
        infill_extruder = 1
        extruder_clearance_height = 20
        print_center = 75,75
        disable_fan_first_layers = 1
        external_perimeters_first = 0
        retract_length = 2.5
        first_layer_extrusion_width = .42
        infill_only_where_needed = 
        retract_restart_extra_toolchange = 0
        external_perimeter_speed = 35
        thin_walls = 1
        bridge_fan_speed = 100
        min_fan_speed = 35
        max_fan_speed = 100
        support_material_enforce_layers = 0
        top_solid_layers = 4
        spiral_vase = 0
        infill_every_layers = 2
        cooling = 1
        bridge_acceleration = 0
        start_perimeters_at_concave_points = 0
        skirts = 2
        brim_width = 3
        fill_density = .2
        standby_temperature_delta = -5
        start_perimeters_at_non_overhang = 0
        bottom_solid_layers = 3
        perimeters = 8
        start_gcode = 
        min_print_speed = 25
        perimeter_extrusion_width = .42
        extruder_offset = 0x0
        solid_infill_speed = 60
        fill_angle = 45
        support_material_pattern = rectilinear
        support_material_interface_extruder = 1
        solid_infill_extrusion_width = .42
        solid_infill_every_layers = 0
        extruder_clearance_radius = 20
        small_perimeter_speed = 40
        retract_layer_change = 1
        ooze_prevention = 0
        top_solid_infill_speed = 40
        support_material_spacing = 2.5
        first_layer_speed = 75%
        complete_objects = 0
        fan_always_on = 0
        randomize_start = 
        perimeter_acceleration = 0
        perimeter_speed = 50
        perimeter_extruder = 1
        infill_first = 0
        nozzle_diameter = .4
        vibration_limit = 0
        retract_restart_extra = 0
        retract_lift = 0
        filament_diameter = 1.68
        support_material_extruder = 1
        post_process = 
        solid_infill_below_area = 0
        bridge_speed = 75
        gcode_comments = 0
        notes = Please note that the first layer is set at 0.3500mm to avoid sticking and warping issues. For further precision, consider adjusting this value to 0.2000mm.
        bed_temperature = 105
        extrusion_multiplier = .6
        support_material_speed = 50
        gap_fill_speed = 30
        infill_extrusion_width = .42
        bed_size = 159,150
        """,
        "callback": {"complete": "http://localhost:8088/v1/complete/", "progress": "http://localhost:8088/v1/progress/"},
        "id": uid.hex}
        
        channel.basic_publish(exchange='',
                      routing_key='stlSlice',
                      body= json.dumps(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
        
        """gcode_file = self.sliceSTL(tmp_filename_stl, x, y, z, tmp_filename_gcode)
        
        request.setHeader("content-disposition","attachment;filename=%s"% (os.path.basename(tmp_filename_gcode)))
        
        if "print" in request.args:
            if  request.args["print"][0] == "true":
                self.postToPrinter(tmp_filename_gcode)
            
        data_out = open(tmp_filename_gcode, 'r').read()
        
        os.remove(tmp_filename_gcode)
        os.remove(tmp_filename_stl)
        return data_out"""
        #print uid
        return uid.hex
        
        
    def sliceSTL(self, stl_file, x, y, z, output_file):
        load_cmd = "--load \"/Users/rob/Library/Repetier/slic3r.ini\""

        cmd = "\"%(exe)s\" %(load_cmd)s --print-center %(x)f,%(y)f --z-offset %(z)f -o \"%(output_file)s\" \"%(stl_file)s\""% ({"x": x, "y": y,"z": z, "exe": settings._slic3r_exe, "output_file": output_file, "stl_file": stl_file, "load_cmd": load_cmd})

        print cmd
        p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
        output, errors = p.communicate()
        return output_file

    def postToPrinter(self, filename):
        fileobj = open(filename, 'rb')
        r = requests.post('http://octopi.media.mit.edu/api/load?apikey=246AC6F0229D4313954B796E7F1C165A', data={"print":"true"}, files={"file": (os.path.basename(filename), fileobj)})

    
