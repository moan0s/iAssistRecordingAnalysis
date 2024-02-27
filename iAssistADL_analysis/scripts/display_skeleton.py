from iAssistADL_analysis import loaders
from iAssistADL_analysis.skeleton import Joint
import matplotlib.pyplot as plt
def get_joint_datum(zed_data, idx:int):
    datum = {}
    for j in Joint:
        datum[j.name] = zed_data["Skeletons"]["Body_21"][j.name]["SkeletonJoint3d"][idx]
    return datum

def draw_skeleton(datum):
    ax = plt.figure().add_subplot(projection='3d')
    x = [joint_pos[0] for joint_pos in datum.values()]
    y = [joint_pos[1] for joint_pos in datum.values()]
    z = [joint_pos[2] for joint_pos in datum.values()]
    ax.scatter(x, y, z, label='points in (x, z)')
    ax.set_title('Simple plot')
    plt.show()

if __name__ == '__main__':
    subject = "BRAD-0701"
    session = "1"
    recording = "1"
    base_data_path = "/home/moanos/software/Compsense/recordings"
    recording_base_path = f"{base_data_path}/{subject}/{session}/{recording}"
    zed_data = loaders.get_zed_skeleton3d_data(recording_base_path)

    print(zed_data["Skeletons"]["Body_21"]["RIGHT_SHOULDER"]["SkeletonJoint3d"])

    print(get_joint_datum(zed_data, 20))
    draw_skeleton(get_joint_datum(zed_data, 50))