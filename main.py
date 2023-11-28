import os
from sample_test.objdet_test import obj_det
from cam_calibrate.coord import CoordPixel, Coord3D, CoordRobot
from cam_calibrate.cam_coord_transform import CamCoordTransformer
from cam_calibrate.robot_coord_transform import RobotCoordTransformer


def run(
	target_obj = 75,
	conf_threshold = 0.5, 
	target_depth = 200,
):
	cam_coord_transformer = CamCoordTransformer()
	robot_coord_transformer = RobotCoordTransformer()
	detected_obj = obj_det(target_obj = target_obj, conf_threshold = conf_threshold)
	u1, v1, u2, v2 = detected_obj[2]
	u = int((u1 + u2) / 2)
	v = int((v1 + v2) / 2)
	pixel_coord = CoordPixel(u, v)
	print(pixel_coord)
	world_coord = cam_coord_transformer.pixel_to_world_coord(pixel_coord, target_depth)
	print(world_coord)
	robot_coord = robot_coord_transformer.world_to_robot_coord(world_coord)
	print(robot_coord)

	
if __name__ == "__main__":
	run()
