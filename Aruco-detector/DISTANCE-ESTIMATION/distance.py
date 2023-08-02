import cv2 as cv
from cv2 import aruco
import numpy as np

# calib_data_path = "../calib_data/MultiMatrix.npz"

# calib_data = np.load(calib_data_path)
# print(calib_data.files)

cam_mat = [[1.48853270e+03, 0.00000000e+00, 1.21625588e+03],
           [0.00000000e+00, 1.48353128e+03, 8.24353749e+02],
           [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
dist_coef = [[-0.31830316, -0.02869803, -0.00377274, -0.00179806,  0.24244702]]
r_vectors = [[[0.72579576], [0.63516087], [1.45512597]], 
             [[ 0.1222652 ], [-0.12612164], [ 1.60500963]], 
             [[ 0.13229092], [ 0.0402791 ], [-0.74223666]], 
             [[ 0.00345742], [-0.31664501], [ 2.28520813],[[-0.03964316],
       [-0.30023126],
       [ 3.00285623]]), array([[ 0.09877454],
       [ 0.19283952],
       [-1.55686052]]), array([[ 0.16357625],
       [-0.14630735],
       [ 1.56067128]]), array([[ 0.14503652],
       [-0.12359627],
       [ 1.59092631]]), array([[-0.24357754],
       [ 0.77853605],
       [ 2.21153088]]), array([[ 0.21968561],
       [-0.05406748],
       [ 0.66596032]]), array([[ 0.21186873],
       [-1.46160358],
       [ 1.83743862]]), array([[-0.51655123],
       [ 0.53576391],
       [ 1.47165452]]), array([[ 0.16915787],
       [ 0.17297407],
       [-2.55625406]]), array([[ 0.82708943],
       [-0.84683905],
       [ 1.40619935]]), array([[ 0.14110295],
       [-0.03578192],
       [-0.03652879]]), array([[-0.41458908],
       [-0.73956144],
       [ 1.37901743]])]
t_vectors = [array([[ 0.17269816],
       [-9.31996787],
       [21.43726637]]), array([[-0.57726593],
       [-9.50147126],
       [20.61686429]]), array([[-6.72005171],
       [-6.43191223],
       [24.006528  ]]), array([[ 3.29285688],
       [-3.78584111],
       [27.23899121]]), array([[ 1.41666619],
       [-2.13665786],
       [27.0733688 ]]), array([[-5.13568327],
       [-2.86540545],
       [24.5708234 ]]), array([[ 1.93108572],
       [-8.52898168],
       [25.970839  ]]), array([[ 1.16589788],
       [-7.88027499],
       [21.97185888]]), array([[ 1.93431693],
       [-8.01290413],
       [23.15955849]]), array([[ -3.00400807],
       [-10.14653616],
       [ 23.03647174]]), array([[ 2.05289301],
       [-7.98588625],
       [24.1541102 ]]), array([[ 1.68138312],
       [-8.08359666],
       [21.85005266]]), array([[-1.83847351],
       [-1.28313847],
       [26.91664401]]), array([[ 0.88626404],
       [-6.46370551],
       [19.35761749]]), array([[ -4.6490949 ],
       [-10.02030069],
       [ 24.17710557]]), array([[-0.8848694 ],
       [-9.10435983],
       [26.21779113]])]

MARKER_SIZE = 8  # centimeters

marker_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)

param_markers = aruco.DetectorParameters_create()

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv.resize(frame, (1024,760))
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
            marker_corners, MARKER_SIZE, cam_mat, dist_coef
        )
        total_markers = range(0, marker_IDs.size)
        for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()

            # Since there was mistake in calculating the distance approach point-outed in the Video Tutorial's comment
            # so I have rectified that mistake, I have test that out it increase the accuracy overall.
            # Calculating the distance
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )
            # Draw the pose of the marker
            point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
            cv.putText(
                frame,
                f"id: {ids[0]} Dist: {round(distance, 2)}",
                top_right,
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            cv.putText(
                frame,
                f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                bottom_right,
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
            # print(ids, "  ", corners)
    cv.imshow("frame", frame)
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()