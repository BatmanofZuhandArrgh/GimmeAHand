import numpy as np
import cv2 as cv
import glob
import pickle
import os


def save_mat(array,outfile = 'cam_calibrate/intrinsic_mat.pkl'):
    with open(outfile, 'wb') as pickle_file:
        pickle.dump(array, pickle_file)


def load_mat(outfile):
    with open(outfile, 'rb') as pickle_file:
        loaded_data = pickle.load(pickle_file)
    return loaded_data


def calibrate():
    CHECKERBOARD = (8,6)
    CELL_SIZE = 24.4
    INIT_X = -122.0 / 2
    INIT_Y = 61.5
    # INIT_Z = 250.0
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1],3), np.float32)
    # objp[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],0:CHECKERBOARD[1]].T.reshape(-1,2)
    # Edit: adjust coordinate based on mm (origin is below camera)
    for j in range(CHECKERBOARD[0]):
        for i in range(CHECKERBOARD[1]):
            m = CHECKERBOARD[1] - i - 1
            n = CHECKERBOARD[0] - j - 1
            idx = m * CHECKERBOARD[0] + n
            objp[0, idx, 0] = i * CELL_SIZE + INIT_X
            objp[0, idx, 1] = j * CELL_SIZE + INIT_Y
    # objp[0, :, 0] = objp[0, :, 0] * CELL_SIZE + INIT_X
    # objp[0, :, 1] = -1 * (objp[0, :, 1] * CELL_SIZE + INIT_Y)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.


    images = glob.glob('cam_calibrate/calib_img/*.jpg')

    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
            cv.imshow('img', img)
            cv.imwrite(os.path.dirname(fname) + '/' + os.path.basename(fname).split('.')[0]+ 'calib.png', img)
            cv.waitKey(500)
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    out_intrinsic = 'cam_calibrate/intrinsic_mat.pkl'
    out_extrinsic = 'cam_calibrate/extrinsic_mat.pkl'


    save_mat(mtx)
    intrinsic_mat = load_mat(out_intrinsic)
    print(intrinsic_mat)

    # print(rvecs)
    # print(tvecs)

    # save_mat()

    # Choose an index for the calibration image you are interested in
    calibration_image_index = 0

    # Get the rotation vector and translation vector for the chosen image
    rvec = rvecs[calibration_image_index]
    tvec = tvecs[calibration_image_index]

    # Convert the rotation vector to a rotation matrix
    R, _ = cv.Rodrigues(rvec)

    # Construct the extrinsic matrix [R|t]
    extrinsic_matrix = np.hstack((R, tvec))

    print("Extrinsic Matrix:")
    print(extrinsic_matrix)
    save_mat(extrinsic_matrix, outfile=out_extrinsic)


if __name__ == "__main__":
    calibrate()
