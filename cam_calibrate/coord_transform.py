import numpy as np
import pickle
# from calibrate import load_mat


def load_intrinsic_mat(mat_file):
    with open(mat_file, "rb") as f:
        mat = pickle.load(f)
    img_width, img_height = 2592, 1944
    mat[0, 2] = (img_width - 1) / 2.0
    mat[1, 2] = (img_height - 1) / 2.0
    return mat


def get_rotation_mat(deg):
	s = np.sin(np.deg2rad(deg))
	c = np.cos(np.deg2rad(deg))
	mat = np.array([
		[1.0, 0.0, 0.0],
		[0.0,  -c,  -s],
		[0.0,   s,  -c],
	])
	return mat


def calculate_world_coord(u, v, intrinsic_mat, target_z = 250.0):
	# u: horizontal image pixel (from left to right)
	# v: vertical image pixel (from top to bottom)
	angle = 20 # camera angle in degree
	img_coord = np.array([u, v, 1.0])
	int_mat = np.array(intrinsic_mat)
	cam_coord = np.matmul(np.linalg.inv(int_mat), img_coord)
	cam_coord = cam_coord / cam_coord[2] * target_z
	rot_mat = get_rotation_mat(angle)
	world_coord = np.matmul(np.linalg.inv(rot_mat), cam_coord)
	world_coord = world_coord / world_coord[2] * target_z * -1.0
	return world_coord


if __name__ == "__main__":
	out_intrinsic = 'cam_calibrate/intrinsic_mat.pkl'
	intrinsic_mat = load_intrinsic_mat(out_intrinsic)
	# u, v = 1296, 972
	u = int(input("Input u: "))
	v = int(input("Input v: "))
	target_z = 250.0 # 250 mm

	print(calculate_world_coord(u, v, intrinsic_mat, target_z))
