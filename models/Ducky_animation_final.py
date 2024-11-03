# Duck animation
# Here, all is real, and all is illusion. What is, what was, and what will be start here,
# with the words: In the beginning, there was... HOWARD THE DUCK!
import numpy as np
import trimesh
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Load the GLB file dynamically. Sounds Russian.
file_path = os.path.join("models", "Duck.glb")
scene = trimesh.load(file_path)

# Check if the scene is loaded properly. If not, cuss loudly and try again.
if scene.is_empty:
    raise ValueError("The 3D scene is empty. Please check the file.")

# Get the first geometry in the scene (assuming there is at least one)
mesh = scene.geometry[list(scene.geometry.keys())[0]]  # Get the first mesh before it gets you.
vertices = mesh.vertices
faces = mesh.faces

# Set the initial angles and motion parameters. Gots to follow da rule fool.
INITIAL_ANGLES_DEGREES = (0, 0, 0)  # Object starts facing forward. Attention!
SIDE_TO_SIDE_MAX_ANGLE = 60  # Degrees to rotate left and right. Political Science?
NODDING_MAX_ANGLE = 20  # Degrees for nodding motion: PhD or something.
FRAMES_PER_DIRECTION = 30  # Animation smoothness that would shame some low budget toons from the 80's
TOTAL_FRAMES = FRAMES_PER_DIRECTION * 4  # Total frames to do the shoulder lean

# Size adjustment percentages for each axis. They're a bit insecure about that.
scale_x = 0.25  # Scale down to 25% of original width
scale_y = 0.25  # Scale down to 25% of original height
scale_z = 0.25  # Scale down to 25% of original depth

# Function to create rotation matrices. Spin little ducky
def rotation_matrix_degrees(angles):
    alpha, beta, gamma = np.radians(angles)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(alpha), -np.sin(alpha)],
                   [0, np.sin(alpha), np.cos(alpha)]])
    
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)],
                   [0, 1, 0],
                   [-np.sin(beta), 0, np.cos(beta)]])
    
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],
                   [np.sin(gamma), np.cos(gamma), 0],
                   [0, 0, 1]])
    
    return Rz @ Ry @ Rx

# Set up the plot for world domination
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
initial_rotation_matrix = rotation_matrix_degrees(INITIAL_ANGLES_DEGREES)

# Scale the vertices and storm the castle.
scaled_vertices = vertices * np.array([scale_x, scale_y, scale_z])

# Apply the initial rotation to the vertices. Spin them like Latrell Sprewell's wheels circa 2000
rotated_vertices = np.dot(scaled_vertices, initial_rotation_matrix.T)

# Function to center the object on the Z-axis, even if it doesn't look centered. 
def center_object(vertices):
    # Calculate the mean of the Z coordinates. Very mean.
    z_mean = np.mean(vertices[:, 2])
    vertices[:, 2] -= z_mean

# Center the object. That should be the middle, but even that's confusing.
center_object(rotated_vertices)

# Function to render the object. I've been awake so long I can barely function.
def render_object(vertices, faces):
    ax.cla()  # Clear previous axes. They were rusty and dull.
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio. It's only fair.
    
    # Prepare the list of vertices for each face. I named these hands "Vertices"
    poly3d = [vertices[face] for face in faces]  

    # Create a solid yellow color for the mesh. How do you have solid mesh??
    colors = np.full((len(faces), 3), fill_value=[1, 1, 0])  # Yellow (RGB: 1, 1, 0)

    # Use Poly3DCollection to add the surface with face colors, or the whole thing. That works too.
    collection = Poly3DCollection(poly3d, facecolors=colors, edgecolors='k', linewidths=0.5, alpha=0.7)
    ax.add_collection3d(collection)

    # Set limits for the axes. Don't swing it without being aware of your surroundings
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    # Set labels for axes. They say "AXE"
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

# Initial render (was actually about 400 renders ago. At least this time it works... somehow.)
render_object(rotated_vertices, faces)

# Flag for typing detection. No need to pledge allegience
is_typing = False

def on_key_press(event):
    global is_typing
    is_typing = True

def on_key_release(event):
    global is_typing
    is_typing = False

# Connect keyboard events to the motion of the duck
fig.canvas.mpl_connect('key_press_event', on_key_press)
fig.canvas.mpl_connect('key_release_event', on_key_release)

# putting the "fun" in animation update FUNction
def update_motion(frame):
    global is_typing
    
    if is_typing:
        # Side to side like a '64
        angle = NODDING_MAX_ANGLE * np.sin(np.pi * frame / FRAMES_PER_DIRECTION)
        rotation_x = np.array([[1, 0, 0],
                                [0, np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                [0, np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
        rotated_vertices = np.dot(scaled_vertices, initial_rotation_matrix.T)
        rotated_vertices = np.dot(rotated_vertices, rotation_x.T)
    else:
        # Twistin like Chubby Checker
        frame_position = frame % TOTAL_FRAMES
        if frame_position < FRAMES_PER_DIRECTION:
            angle = -SIDE_TO_SIDE_MAX_ANGLE * (frame_position / FRAMES_PER_DIRECTION)
        elif frame_position < 2 * FRAMES_PER_DIRECTION:
            angle = -SIDE_TO_SIDE_MAX_ANGLE * (1 - (frame_position - FRAMES_PER_DIRECTION) / FRAMES_PER_DIRECTION)
        elif frame_position < 3 * FRAMES_PER_DIRECTION:
            angle = SIDE_TO_SIDE_MAX_ANGLE * ((frame_position - 2 * FRAMES_PER_DIRECTION) / FRAMES_PER_DIRECTION)
        else:
            angle = SIDE_TO_SIDE_MAX_ANGLE * (1 - (frame_position - 3 * FRAMES_PER_DIRECTION) / FRAMES_PER_DIRECTION)

        rotation_z = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle)), 0],
                                [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0],
                                [0, 0, 1]])
        
        rotated_vertices = np.dot(scaled_vertices, initial_rotation_matrix.T)
        rotated_vertices = np.dot(rotated_vertices, rotation_z.T)

    # Clear previous surfaces and update with new vertices. The old ones were so last hackathon.
    render_object(rotated_vertices, faces)

# Start animation. Now. Hurry up.
ani = FuncAnimation(fig, update_motion, frames=range(TOTAL_FRAMES), interval=50)
plt.show()
# Thats it. That's my duck. Hope you like it. Hope he didn't bite you.

