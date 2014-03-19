#!/usr/bin/env python
import pika
import sys, settings, json, uuid

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.host))
channel = connection.channel()

channel.queue_declare(queue='stlSlice', durable=True)
            
message = {"stl": {"filename": "octocat.stl", "url": "http://www.thingiverse.com/download:32770", "position": {"x": 10, "y": 10, "z": 0}},
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
"id": uuid.uuid4().hex}

channel.basic_publish(exchange='',
                      routing_key='stlSlice',
                      body= json.dumps(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print " [x] Sent"
connection.close()