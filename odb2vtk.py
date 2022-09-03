#import necessary modules to handle Abaqus output database, files and
string
from odbAccess import *
from textRepr import *
from string import *
from time import *
input_frame = [0, 0]
input_step = [0]
#auto run convert odb to vtk
def runConvert(filename, stepNum):
global input_frame
starttime = time()
for i in range(stepNum):
if(i == 0):
input_frame = [0,1]
input_frame = range(int(input_frame[0]),int(input_frame[1])+1)
elif(i % 2 == 1):
input_frame = [0,0]
input_frame = range(int(input_frame[0]),int(input_frame[1])+1)
elif(i != 0 and i % 2 == 0):
input_frame = [1,1]
input_frame = range(int(input_frame[0]),int(input_frame[1])+1)
input_step[0] = i
ConvertOdb2Vtk(filename)
print "All step's time elapsed: ", time() - starttime, "s"
def ConvertOdb2Vtk(filename):
starttime = time()
# Check if filename points to existing file
if not os.path.isfile(filename):
print 'Parameter file "%s" not found'%(filename)
sys.exit(2)
#read odb2vtk file to get parameter setting
odb2vtk = open(filename,'rt')
read = odb2vtk.read()
input = read.split("'")
#get odb file's path
odb_path = input[1]
#get odb file name
odbname = input[3]
#get the output files' path
vtk_path = input[5]
#get the mesh type
mesh_type = int(input[7])
mesh_conner = 0
if (mesh_type == 12):
mesh_conner = 8
mesh_name = "Hexahedron"
if (mesh_type == 10):
mesh_conner = 4
mesh_name = "Tetra"
if (mesh_conner == 0):
print "Mesh type error or unidentified"
os._exit(0)
#get the quantity of pieces to partition
piecenum = int(input[9])
#get the frame
#input_frame = input[11].split("-")
#input_frame = range(int(input_frame[0]),int(input_frame[1])+1)
#get the step
#input_step = input[13].split(",")
#get the instance
input_instance = input[15].split(",")
#end reding and close odb2vtk file
odb2vtk.close()
#display the reading result of odb2vtk file
print "odb2vtk reading finished, time elapsed: ", time()-starttime
print "Basic Information:"
print "Model:",odbname,"; Mesh type:",mesh_name,"; Number of
blocks:",piecenum
print "Convert frames: ",input_frame[0]," to ",input_frame[-1]
print "Step & Instance : ",str(input_step),", ",str(input_instance)
#open an ODB ( Abaqus output database )
odb = openOdb(os.path.join(odb_path,odbname)+'.odb',readOnly=True)
print "ODB opened"
#access geometry and topology information ( odb->rootAssembly-
>instances->(nodes, elements) )
rootassembly = odb.rootAssembly
instance = rootassembly.instances
#access attribute information
step = odb.steps
#get instance & step information : Quantity and all names
allinstancestr = str(instance)
autoins = allinstancestr.split("'")
inslen = len(autoins)/4
instance_N = range(0,inslen)
allstepstr = str(step)
autostep = allstepstr.split("'")
steplen = len(autostep)/4
step_N = range(0,steplen)
for i in input_step:
if(steplen < int(i)):
print "input step exceeds the range of steps"
os._exit(0)
for i in input_instance:
if(inslen < int(i)):
print "input instance exceeds the range of instances"
os._exit(0)
#ensure death_ele
death_num = (int(input_step[0]) + 1)/2
death_ele = []
if(death_num > 0 and death_num < 86):
for i in range(death_num):
death_ele.append(24904 - i)
death_ele.append(25244 - i)
elif(death_num > 85):
for i in range(0, 85):
death_ele.append(24904 - i)
death_ele.append(25244 - i)
for i in range(85, death_num):
death_ele.append(25075 + i - 85)
death_ele.append(25415 + i - 85)
#step cycle
for step_i in input_step:
n = int(step_i)*4+1
stepname = autostep[n]
print "Step: ",stepname
#instance cycle
for ins_i in input_instance:
n = int(ins_i)*4+1
instancename = autoins[n]
print "Instance: ",instancename
#access nodes & elements
node = instance[instancename].nodes
element = instance[instancename].elements
n_nodes = len(node)
n_elements = len(element)
#access attribute(fieldOutputs) information
frame = step[stepname].frames
#compute the number of element of each block
p_elements = n_elements/piecenum + 1
lp_elements = n_elements - (p_elements*(piecenum-1)) #last
block
#match nodes' label and its order in sequence (for empty nodes
in tetra mesh)
MLN = node[n_nodes-1].label
TOTAL=[]
#read node in sequence, and get the largest label of node(nonempty)
#MLN is the max label of nodeset
for i in node:
TOTAL.append(i.label)
if(i.label > MLN):
MLN = i.label
#match (the key)
L=[]
n = 0
for i in range(MLN):
L.append(0)
for i in TOTAL:
L[i-1] = n
n += 1
#frame cycle
for i_frame in input_frame:
#Detect whether the input frame is out of range
try:
TRY = odb.steps[stepname].frames[int(i_frame)]
except:
print "input frame exceeds the range of frames"
os._exit(0)
break
#Access a frame
N_Frame = odb.steps[stepname].frames[int(i_frame)]
print "Frame:",i_frame
#create array for store result data temporarily
# U-S two vars
# Vector-U
L0=[]
# Tensors-S
L1=[]
for i in range(MLN):
L0.append([0,0,0])
L1.append([0,0])
print "Reading U"
time1 = time()
#Access Spatial displacement
displacement = N_Frame.fieldOutputs['U']
fieldValues = displacement.values
for valueX in fieldValues :
i = valueX.nodeLabel
L0[i-1][0] = valueX.data[0]
L0[i-1][1] = valueX.data[1]
L0[i-1][2] = valueX.data[2]
print "Time elapsed: ", time() - time1, "s"
print "Reading Stress"
time1 = time()
#access Stress components
Stress = N_Frame.fieldOutputs['S']
node_Stress = Stress.getSubset(position=ELEMENT_NODAL)
fieldValues = node_Stress.values
for valueX in fieldValues :
L1[valueX.nodeLabel-1][0] += 1
L1[valueX.nodeLabel-1][1] += valueX.mises
# can first ave
print "Time elapsed: ", time() - time1, "s"
'''============================================================'''
print "Partitionning model and writing vtk files ......"
#piece cycle, to partion the model and create each piece
for vtk files
for pn in range(piecenum):
time1 = time()
print "frame:",i_frame,"; block:",pn
#Reorganization
#Control&Storage
#estimate whether the node has already existed
stg_p = []
#store the reorganized node for element
stg_e = []
#store the reorganized node for node
stg_n = []
for i in range(MLN):
stg_p.append(-1)
nodecount = 0
#reorganize the node and element (reconstruct the mesh)
if(pn == piecenum-1):
M = range(pn*p_elements,n_elements)
else:
M = range(pn*p_elements,(pn+1)*p_elements)
for i in M:
for j in range(mesh_conner):
k = element[i].connectivity[j] - 1
if(stg_p[k] < 0):
stg_p[k] = nodecount
stg_n.append(L[k])
stg_e.append(nodecount)
nodecount += 1
else:
stg_e.append(stg_p[k])
#compute point quantity
n_reop = len(stg_n)
reop_N = range(0,len(stg_n))
#create and open a VTK(.vtu) files
if(piecenum > 1):
outfile = open
(os.path.join(vtk_path,odbname)+'_'+stepname+'_'+instancename+'f%03d'%int(i
_frame)+' '+'p'+str(pn)+'.vtu','w')
if(piecenum == 1):
outfile = open
(os.path.join(vtk_path,odbname)+'_'+stepname+'_'+instancename+'f%03d'%int(i
_frame)+'.vtu','w')
#<VTKFile>, including the type of mesh, version, and
byte_order
outfile.write('<VTKFile type="UnstructuredGrid"
version="0.1" byte_order="LittleEndian">'+'\n')
#<UnstructuredGrid>
outfile.write('<UnstructuredGrid>'+'\n')
#<Piece>, including the number of points and cells
if(pn == piecenum-1):
outfile.write('<Piece
NumberOfPoints="'+str(n_reop)+'"'+'
'+'NumberOfCells="'+str(lp_elements)+'">'+'\n')
else:
outfile.write('<Piece
NumberOfPoints="'+str(n_reop)+'"'+'
'+'NumberOfCells="'+str(p_elements)+'">'+'\n')
print "Writing Nodes ......"
#<Points> Write nodes into vtk files
displacement = N_Frame.fieldOutputs['U']
fieldValues = displacement.values
outfile.write('<Points>'+'\n')
outfile.write('<DataArray type="Float64"
NumberOfComponents="3" format="ascii">'+'\n')
for i in reop_N:
nt = stg_n[i]
k = node[stg_n[i]].label-1
# L1[k][0] == 0 represent death element's node
if(L1[k][0] == 0):
print k
else:
X,Y,Z = node[nt].coordinates[0]+L0[k]
[0],node[nt].coordinates[1]+L0[k][1],node[nt].coordinates[2]+L0[k][2]
outfile.write(' '+'%11.8e'%X+' '+'%11.8e'%Y+'
'+'%11.8e'%Z+'\n')
outfile.write('</DataArray>'+'\n')
outfile.write('</Points>'+'\n')
#</Points>
print "Writing Results data ......"
#<PointData> Write results data into vtk files
outfile.write("<"+"PointData"+"
"+"Vevtors="+'"'+"Spatial_displacement"+'"'\
+" "+"Scalars="+'"'+"Stress_Mises"+'"'+">"+'\n')
#Spatial displacement, <DataArray>
outfile.write("<"+"DataArray"+"
"+"type="+'"'+"Float32"+'"'+" "+"Name="+'"'+"Spatial_displacement"+'"'+"
"+"NumberOfComponents="+'"'+"3"+'"'+" "+"format="+'"'+"ascii"+'"'+">"+'\n')
for i in reop_N:
k = node[stg_n[i]].label-1
if(L1[k][0] != 0):
X,Y,Z = L0[k][0],L0[k][1],L0[k][2]
outfile.write('%11.8e'%X+' '+'%11.8e'%Y+'
'+'%11.8e'%Z+'\n')
outfile.write("</DataArray>"+'\n')
#</DataArray>
#Stress Mises, <DataArray>
outfile.write("<"+"DataArray"+"
"+"type="+'"'+"Float32"+'"'+" "+"Name="+'"'+"Stress_Mises"+'"'+"
"+"format="+'"'+"ascii"+'"'+">"+'\n')
for i in reop_N:
k = node[stg_n[i]].label-1
if(L1[k][0] != 0):
X = L1[k][1]/L1[k][0]
outfile.write('%11.8e'%X+'\n')
outfile.write('</DataArray>'+'\n')
#</DataArray>
outfile.write("</PointData>"+'\n')
#</PointData>
print "Writing Cells ......"
#<Cells> Write cells into vtk files
outfile.write('<Cells>'+'\n')
#Connectivity
outfile.write('<DataArray type="Int32"
Name="connectivity" format="ascii">'+'\n')
if (mesh_type == 12):
count = 0;
for i in range(len(stg_e)/8):
# i represent element index, when i equals
death element's index, write "0 0 0 0 0 0 0 0"
if(i in death_ele):
count = count + 1
outfile.write("0 0 0 0 0 0 0 0" +'\n')
else:
outfile.write(str(stg_e[i*8])+'
'+str(stg_e[i*8+1])+' '+str(stg_e[i*8+2])+' '+str(stg_e[i*8+3])+'
'+str(stg_e[i*8+4])+' '+str(stg_e[i*8+5])+' '+str(stg_e[i*8+6])+'
'+str(stg_e[i*8+7])+'\n')
print "deleted" + str(count) + "elements"
if (mesh_type == 10):
for i in range(len(stg_e)/4):
outfile.write(str(stg_e[i*4])+'
'+str(stg_e[i*4+1])+' '+str(stg_e[i*4+2])+' '+str(stg_e[i*4+3])+'\n')
outfile.write('</DataArray>'+'\n')
#Offsets
outfile.write('<DataArray type="Int32" Name="offsets"
format="ascii">'+'\n')
for i in range(len(stg_e)/mesh_conner):
outfile.write(str(i*mesh_conner+mesh_conner)+'\n')
outfile.write('</DataArray>'+'\n')
#Type
outfile.write('<DataArray type="UInt8" Name="types"
format="ascii">'+'\n')
for i in range(len(stg_e)/mesh_conner):
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
print "Time elapsed: ", time() - time1, "s"
'''====================================================================='''
print "Creating .pvtu file for frame ", i_frame," ......"
#create .pvtu files for parallel visualization
if ( piecenum > 1 ):
outfile = open
(os.path.join(vtk_path,odbname)+'_'+stepname+'_'+'f%03d'%int(i_frame)+'.pvt
u','w')
#write the basic information for .pvtu files
outfile.write('<?xml version="1.0"?>'+'\n')
outfile.write('<VTKFile type="PUnstructuredGrid"
version="0.1" byte_order="LittleEndian">'+'\n')
outfile.write("<PUnstructuredGrid
GhostLevel="+'"'+str(piecenum)+'"'+">"+'\n')
#pointdata
outfile.write("<"+"PPointData"+"
"+"Vevtors="+'"'+"Spatial_displacement"+'"'\
+" "+"Scalars="+'"'+"Stress_Mises"+'"'+">"+'\n')
outfile.write("<"+"PDataArray"+"
"+"type="+'"'+"Float32"+'"'+" "+"Name="+'"'+"Spatial_displacement"+'"'+"
"+"NumberOfComponents="+'"'+"3"+'"'+" "+"/>"+'\n')
outfile.write("<"+"PDataArray"+"
"+"type="+'"'+"Float32"+'"'+" "+"Name="+'"'+"Stress_Mises"+'"'+"
"+"/>"+'\n')
outfile.write("</PPointData>"+'\n')
#points
outfile.write("<PPoints>"+'\n')
outfile.write("<PDataArray type="+'"'+"Float64"+'"'+"
"+"NumberOfComponents="+'"'+"3"+'"'+"/>"+'\n')
outfile.write("</PPoints>"+'\n')
#write the path of each piece for reading it through
the .pvtu file
for pn in range(piecenum):
outfile.write("<Piece
Source="+'"'+odbname+'_'+stepname+'_'+instancename+'f%03d'%int(i_frame)+'
'+'p'+str(pn)+'.vtu'+'"'+"/>"+'\n')
outfile.write("</PUnstructuredGrid>"+'\n')
outfile.write("</VTKFile>")
outfile.close()
odb.close()
print "Total time elapsed: ", time() - starttime, "s"