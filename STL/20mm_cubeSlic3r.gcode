; generated by Slic3r 1.2.9 on 2017-10-22 at 20:55:24

; external perimeters extrusion width = 10.00mm
; perimeters extrusion width = 10.50mm
; infill extrusion width = 10.50mm
; solid infill extrusion width = 10.50mm
; top infill extrusion width = 10.50mm

; external perimeters extrusion width = 10.00mm
; perimeters extrusion width = 10.50mm
; infill extrusion width = 10.50mm
; solid infill extrusion width = 10.50mm
; top infill extrusion width = 10.50mm

;Start_gcode
G28 ; home all axes

G21 ; set units to millimeters
G90 ; use absolute coordinates
M82 ; use absolute distances for extrusion
G92 E0
T0
G92 E0
;Before
G1 Z10.000 F900.000
;After
G1 E-1.00000 F2400.00000
G92 E0
G1 Z25.000 F900.000
G1 X23.562 Y18.808 F900.000
G1 Z10.000 F900.000
G1 E1.00000 F2400.00000
G1 X33.562 Y18.808 E11.00000 F120.000
G1 X33.562 Y28.808 E21.00000
G1 X23.562 Y28.808 E31.00000
G1 X23.562 Y20.308 E39.50000
G1 X32.222 Y23.808 F900.000
;Before
G1 Z10.000 F900.000
;After
G92 E0
G1 Z25.000 F900.000
;ToolChange
T1
G92 E0
G1 E-1.00000 F2400.00000
G92 E0
G1 X57.775 Y20.792 F900.000
G1 Z10.000 F900.000
G1 E1.00000 F2400.00000
G1 X67.775 Y20.792 E11.00000 F120.000
G1 X67.775 Y30.792 E21.00000
G1 X57.775 Y30.792 E31.00000
G1 X57.775 Y22.292 E39.50000
G1 X66.436 Y25.792 F900.000
;Before
G1 Z20.000 F900.000
;After
G92 E0
G1 Z35.000 F900.000
;ToolChange
T0
G92 E0
G1 E-1.00000 F2400.00000
G92 E0
G1 X23.562 Y18.808 F900.000
G1 Z20.000 F900.000
G1 E1.00000 F2400.00000
G1 X33.562 Y18.808 E11.00000 F120.000
G1 X33.562 Y28.808 E21.00000
G1 X23.562 Y28.808 E31.00000
G1 X23.562 Y20.308 E39.50000
G1 X32.222 Y23.808 F900.000
;Before
G1 Z20.000 F900.000
;After
G92 E0
G1 Z35.000 F900.000
;ToolChange
T1
G92 E0
G1 E-1.00000 F2400.00000
G92 E0
G1 X57.775 Y20.792 F900.000
G1 Z20.000 F900.000
G1 E1.00000 F2400.00000
G1 X67.775 Y20.792 E11.00000 F120.000
G1 X67.775 Y30.792 E21.00000
G1 X57.775 Y30.792 E31.00000
G1 X57.775 Y22.292 E39.50000
G1 X66.436 Y25.792 F900.000
G1 E38.50000 F2400.00000
G92 E0
G1 Z35.000 F900.000
M84 ; steppers off
;End_gcode
; filament used = 77.0mm (6.0cm3)
; filament used = 77.0mm (6.0cm3)

; avoid_crossing_perimeters = 0
; bed_shape = 0x0,200x0,200x200,0x200
; bed_temperature = 0
; before_layer_gcode = ;Before
; bridge_acceleration = 0
; bridge_fan_speed = 0
; brim_width = 0
; complete_objects = 0
; cooling = 0
; default_acceleration = 0
; disable_fan_first_layers = 3
; duplicate_distance = 6
; end_gcode = M84 ; steppers off\n;End_gcode
; extruder_clearance_height = 20
; extruder_clearance_radius = 20
; extruder_offset = 0x0,0x0
; extrusion_axis = E
; extrusion_multiplier = 1,1
; fan_always_on = 0
; fan_below_layer_time = 60
; filament_colour = #FFFFFF;#FFFFFF
; filament_diameter = 10,10
; first_layer_acceleration = 0
; first_layer_bed_temperature = 0
; first_layer_extrusion_width = 100%
; first_layer_speed = 2
; first_layer_temperature = 0,0
; gcode_arcs = 0
; gcode_comments = 0
; gcode_flavor = reprap
; infill_acceleration = 0
; infill_first = 0
; layer_gcode = ;After
; max_fan_speed = 100
; max_print_speed = 2
; max_volumetric_speed = 0
; min_fan_speed = 35
; min_print_speed = 10
; min_skirt_length = 0
; notes = 
; nozzle_diameter = 10,10
; only_retract_when_crossing_perimeters = 0
; ooze_prevention = 0
; output_filename_format = [input_filename_base].gcode
; perimeter_acceleration = 0
; post_process = 
; pressure_advance = 0
; resolution = 0
; retract_before_travel = 2,2
; retract_layer_change = 0,0
; retract_length = 1,1
; retract_length_toolchange = 0,0
; retract_lift = 15,15
; retract_restart_extra = 0,0
; retract_restart_extra_toolchange = 0,0
; retract_speed = 40,40
; skirt_distance = 6
; skirt_height = 1
; skirts = 0
; slowdown_below_layer_time = 5
; spiral_vase = 0
; standby_temperature_delta = -5
; start_gcode = ;Start_gcode\nG28 ; home all axes\n
; temperature = 0,0
; threads = 2
; toolchange_gcode = ;ToolChange
; travel_speed = 15
; use_firmware_retraction = 0
; use_relative_e_distances = 0
; use_volumetric_e = 0
; vibration_limit = 0
; wipe = 0,0
; z_offset = 0
; dont_support_bridges = 1
; extrusion_width = 0
; first_layer_height = 10
; infill_only_where_needed = 0
; interface_shells = 0
; layer_height = 10
; raft_layers = 0
; seam_position = aligned
; support_material = 0
; support_material_angle = 0
; support_material_contact_distance = 0.2
; support_material_enforce_layers = 0
; support_material_extruder = 1
; support_material_extrusion_width = 0
; support_material_interface_extruder = 1
; support_material_interface_layers = 3
; support_material_interface_spacing = 0
; support_material_interface_speed = 100%
; support_material_pattern = pillars
; support_material_spacing = 2.5
; support_material_speed = 60
; support_material_threshold = 0
; xy_size_compensation = 0
; bottom_solid_layers = 3
; bridge_flow_ratio = 1
; bridge_speed = 2
; external_fill_pattern = rectilinear
; external_perimeter_extrusion_width = 0
; external_perimeter_speed = 2
; external_perimeters_first = 0
; extra_perimeters = 1
; fill_angle = 45
; fill_density = 100%
; fill_pattern = rectilinear
; gap_fill_speed = 2
; infill_every_layers = 1
; infill_extruder = 1
; infill_extrusion_width = 0
; infill_overlap = 15%
; infill_speed = 2
; overhangs = 1
; perimeter_extruder = 1
; perimeter_extrusion_width = 0
; perimeter_speed = 2
; perimeters = 3
; small_perimeter_speed = 2
; solid_infill_below_area = 70
; solid_infill_every_layers = 0
; solid_infill_extruder = 1
; solid_infill_extrusion_width = 0
; solid_infill_speed = 2
; thin_walls = 1
; top_infill_extrusion_width = 0
; top_solid_infill_speed = 2
; top_solid_layers = 3
