ansible-playbook main.yaml -e ansible_become_pass={{ PASS }}

I presume Blender is installed, and I presume it has the path as my current installation:

'/mnt/c/Program Files/Blender Foundation/Blender 3.2/blender.exe'

This process uses things from packages, to allow ansible easy access I presume are installed in a folder paralell to the main directory called "packages":

appdirs
pyvista
scooby
vtk

The process presumes you have another paralell folder called 'seedingArea' which must contain the files used to within the process.

Inside this folder there should be:

- An 'fbx' folder containing the fbx files. (For the sake of Klein-like shapes I presume that this is an animation which perfectly loops)
- A "Hyperplane" Folder which contains the vector of the hyperplane of which we will take parallel slices of the 4-d shape created for the new animation. (These should be four floats seperated by a space in a .txt file)


The process will create another folder called processFiles as it creates things.



My current inventory uses ansible_python_interpreter=/usr/bin/python3 but this may not be the python3 installation location in other computers.


Change the vars in the main.yaml






















Noting the installation process I have written down.


git clone https://github.com/pyvista/tetgen


Not 100% on the below commands:
 sudo apt-get install build-essential
 sudo apt-get install python3-numpy python3-scipy python3-matplotlib ipython3 python3-notebook python3-pandas python3-sympy python3-nose

pip install --target=../packages/vtk vtk
