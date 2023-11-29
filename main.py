import os
from detection.objdet import obj_det
from coord_mapping.coord import CoordPixel, Coord3D, CoordRobot #Probably find a way to clean this up
from coord_mapping.cam_coord_transform import CamCoordTransformer
from coord_mapping.robot_coord_transform import RobotCoordTransformer
from motor.motor_utils import robot_coord_to_servo
from controls.naive_controller import NaiveController
from controls.planned_controller import PlannedController

def run(
	target_obj = 75,
	conf_threshold = 0.5, 
	target_depth = 200,
	planning = "naive",
):
	
	###1. Object Detection: Loops end when detected first vase/bottle
	detected_obj = obj_det(target_obj = target_obj, conf_threshold = conf_threshold)

	###2. Coordinate conversion: Convert object's coordinate to robot's world coordinate
	u1, v1, u2, v2 = detected_obj[2]
	u = int((u1 + u2) / 2)
	v = int((v1 + v2) / 2)
	pixel_coord = CoordPixel(u, v)
	print(pixel_coord)

	cam_coord_transformer = CamCoordTransformer()
	world_coord = cam_coord_transformer.pixel_to_world_coord(pixel_coord, target_depth)
	print(world_coord)


	###3. Config inference: From object's coordinate, infer robot's joints' angles
	robot_coord_transformer = RobotCoordTransformer()
	robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
	print(robot_coord)
	if not robot_coord_transformer.is_above_ground():
		return "Object unattainable by the robot's configuration"

	###4. Target Motor Angle: From target robot angles in kinematics, infer target angles to be input in motors
	servo_angles = robot_coord_to_servo(robot_coord)
	print(servo_angles)
	
	
	###5. Execute
	if planning == 'naive':
		controller = NaiveController()
	else:
		# sequence = Planner.do_something()
		# controller = PlannedController(sequence)
		raise NotImplemented
	
	controller.execute()
	
	print('Donezo')
	
if __name__ == "__main__":
	run()
