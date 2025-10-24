import pandas as pd
import numpy as np

df = pd.read_csv("data/data.csv")

angles_left = []
angles_right = []

for frame in range(len(df)):
    # joint 좌표 초기화 (3x2 배열로 수정)
    joint_left = np.zeros((3, 2))
    joint_right = np.zeros((3, 2))

    # 왼쪽 관절
    joint_left[0] = [df.loc[frame, "calf_knee_l_RelLoc_X"],
                     df.loc[frame, "calf_knee_l_RelLoc_Y"]]
    joint_left[1] = [df.loc[frame, "thigh_out_l_RelLoc_X"],
                     df.loc[frame, "thigh_out_l_RelLoc_Y"]]
    joint_left[2] = [df.loc[frame, "clavicle_out_l_RelLoc_X"],
                     df.loc[frame, "clavicle_out_l_RelLoc_Y"]]

    # 오른쪽 관절
    joint_right[0] = [df.loc[frame, "calf_knee_r_RelLoc_X"],
                      df.loc[frame, "calf_knee_r_RelLoc_Y"]]
    joint_right[1] = [df.loc[frame, "thigh_out_r_RelLoc_X"],
                      df.loc[frame, "thigh_out_r_RelLoc_Y"]]
    joint_right[2] = [df.loc[frame, "clavicle_out_r_RelLoc_X"],
                      df.loc[frame, "clavicle_out_r_RelLoc_Y"]]

    # 벡터 계산
    v1_left = joint_left[1] - joint_left[0]  # 무릎에서 허벅지 방향
    v2_left = joint_left[2] - joint_left[1]  # 허벅지에서 쇄골 방향
    
    v1_right = joint_right[1] - joint_right[0]
    v2_right = joint_right[2] - joint_right[1]

    # 벡터 정규화
    v1_left_norm = v1_left / np.linalg.norm(v1_left)
    v2_left_norm = v2_left / np.linalg.norm(v2_left)
    v1_right_norm = v1_right / np.linalg.norm(v1_right)
    v2_right_norm = v2_right / np.linalg.norm(v2_right)

    # 각도 계산
    cos_left = np.clip(np.dot(v1_left_norm, v2_left_norm), -1.0, 1.0)
    angle_left = np.degrees(np.arccos(cos_left))

    cos_right = np.clip(np.dot(v1_right_norm, v2_right_norm), -1.0, 1.0)
    angle_right = np.degrees(np.arccos(cos_right))

    angles_left.append(angle_left)
    angles_right.append(angle_right)

df["angle_left_deg"] = angles_left
df["angle_right_deg"] = angles_right

df.to_csv("output1.csv", index=False)