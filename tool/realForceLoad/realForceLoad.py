import meshio
import os
from string import *
from time import *
import random
#mesh = meshio.read("F:/Abaqus_Study/baobi/7050-
T7451/0705/odb2vtk/vtks/Job-1_Step-340_WP-1f000.vtu")
vtk_path = "F:/Abaqus_Study/baobi/7050-T7451/0705/odb2vtk/rf-vtks/"
odbname = "Job-1"
#stepname = "Step-340"
#instancename = "WP-1"
#i_frame = "1"
mesh_conner = 8
mesh_type = 12
#paras:forceX, forceY, forceZ, stepNums
def runLoad(forceX, forceY, forceZ, stepNums):
time1 = time()
#get each step's mesh by meshio
for i in range(stepNums):
if ((i + 1) % 2 == 0):
mesh = meshio.read("F:/Abaqus_Study/baobi/7050-
T7451/0705/odb2vtk/vtks/Job-1_Step-" + str(i + 1) + "_WP-1f000.vtu")
else :
mesh = meshio.read("F:/Abaqus_Study/baobi/7050-
T7451/0705/odb2vtk/vtks/Job-1_Step-" + str(i + 1) + "_WP-1f001.vtu")
i_frame = str(i + 1)
#mesh,i_frame paras pass to function realForceLoad
realForceLoad(forceX, forceY, forceZ, mesh, i_frame)
print("runLoad time elapsed: ", time() - time1, "s")
def realForceLoad(forceX, forceY, forceZ, mesh, i_frame):
#get all infos of each step's mesh by meshio
points = mesh.points
cells = mesh.cells[0][1]
disps = mesh.point_data['Spatial_displacement']
stress = mesh.point_data['Stress_Mises']
nodeNum = int(points.size / 3)
cellNum = int(cells.size / 8)
#force: add random value
forceX = forceX + random.randint(1,10)
forceY = forceY + random.randint(1,10)
forceZ = forceZ + random.randint(1,10)
time1 = time()
#outfile = open
(os.path.join(vtk_path,odbname)+'_'+stepname+'_'+instancename+'f%03d'%int(i
_frame)+'.vtu','w')
#create a new vtu file
outfile = open
(os.path.join(vtk_path,odbname)+'_'+'f%03d'%int(i_frame)+'.vtu','w')
#<VTKFile>, including the type of mesh, version, and byte_order
outfile.write('<VTKFile type="UnstructuredGrid" version="0.1"
byte_order="LittleEndian">'+'\n')
#<UnstructuredGrid>
outfile.write('<UnstructuredGrid>'+'\n')
#<Piece>, including the number of points and cells
outfile.write('<Piece NumberOfPoints="'+str(nodeNum)+'"'+'
'+'NumberOfCells="'+str(cellNum)+'">'+'\n')
print("Writing Nodes ......")
#<Points> Write nodes into vtk files
outfile.write('<Points>'+'\n')
outfile.write('<DataArray type="Float64" NumberOfComponents="3"
format="ascii">'+'\n')
for i in range(nodeNum):
X, Y, Z = points[i][0] + disps[i][0] * (forceX - 1), points[i][1] +
disps[i][1] * (forceY - 1), points[i][2] + disps[i][2] * (forceZ - 1)
outfile.write(' '+'%11.8e'%X+' '+'%11.8e'%Y+' '+'%11.8e'%Z+'\n')
outfile.write('</DataArray>'+'\n')
outfile.write('</Points>'+'\n')
#</Points>
print("Writing Results data ......")
#<PointData> Write results data into vtk files
outfile.write("<"+"PointData"+"
"+"Vevtors="+'"'+"Spatial_displacement"+'"'\
+" "+"Scalars="+'"'+"Stress_Mises"+'"'+">"+'\n')
#Spatial displacement, <DataArray>
outfile.write("<"+"DataArray"+" "+"type="+'"'+"Float32"+'"'+"
"+"Name="+'"'+"Spatial_displacement"+'"'+"
"+"NumberOfComponents="+'"'+"3"+'"'+" "+"format="+'"'+"ascii"+'"'+">"+'\n')
for i in range(nodeNum):
X, Y, Z = disps[i][0] * forceX, disps[i][1] * forceY, disps[i][2] *
forceZ
outfile.write(' '+'%11.8e'%X+' '+'%11.8e'%Y+' '+'%11.8e'%Z+'\n')
outfile.write("</DataArray>"+'\n')
#</DataArray>
#Stress Mises, <DataArray>
outfile.write("<"+"DataArray"+" "+"type="+'"'+"Float32"+'"'+"
"+"Name="+'"'+"Stress_Mises"+'"'+" "+"format="+'"'+"ascii"+'"'+">"+'\n')
for i in range(nodeNum):
#empirical equation, maybe it has some questions
X = stress[i] * ((forceX ** 2 + forceY ** 2 + forceZ ** 2) / 3) **
0.5
outfile.write('%11.8e'%X+'\n')
outfile.write('</DataArray>'+'\n')
#</DataArray>
outfile.write("</PointData>"+'\n')
#</PointData>
print("Writing Cells ......")
#<Cells> Write cells into vtk files
outfile.write('<Cells>'+'\n')
#Connectivity
outfile.write('<DataArray type="Int32" Name="connectivity"
format="ascii">'+'\n')
for i in range(cellNum):
outfile.write(str(cells[i][0])+' '+str(cells[i][1])+'
'+str(cells[i][2])+' '+str(cells[i][3])+' '+str(cells[i][4])+'
'+str(cells[i][5])+' '+str(cells[i][6])+' '+str(cells[i][7])+'\n')
outfile.write('</DataArray>'+'\n')
#Offsets and Type are necessary
#Offsets
outfile.write('<DataArray type="Int32" Name="offsets"
format="ascii">'+'\n')
for i in range(cellNum):
outfile.write(str(i*mesh_conner+mesh_conner)+'\n')
outfile.write('</DataArray>'+'\n')
#Type
outfile.write('<DataArray type="UInt8" Name="types"
format="ascii">'+'\n')
for i in range(cellNum):
outfile.write(str(mesh_type)+'\n')
outfile.write('</DataArray>'+'\n')
outfile.write('</Cells>'+'\n')
#</Cells>
#</Piece>
outfile.write('</Piece>'+'\n')
#</UnstructuredGrid>
outfile.write('</UnstructuredGrid>'+'\n')
#</VTKFile>
outfile.write('</VTKFile>'+'\n')
outfile.close()
print("Time elapsed: ", time() - time1, "s")