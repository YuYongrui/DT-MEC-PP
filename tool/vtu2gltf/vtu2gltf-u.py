# trace generated using paraview version 5.9.0
#### import the simple module from the paraview
from paraview.simple import *
from time import *
time1 = time()
for i in range(341):
    # create a new 'XML Unstructured Grid Reader'
    myVtu = XMLUnstructuredGridReader(registrationName='Job-1_' + 'f%03d' % i
                                                       + '.vtu', FileName=[
        'F:\\Abaqus_Study\\baobi\\7050-T7451\\0705\\odb2vtk\\rfvtks\\conForce\\Job-1_' + 'f%03d' % i + '.vtu'])
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # show data in view
    myVtuDisplay = Show(myVtu, renderView1,
                        'UnstructuredGridRepresentation')
    # trace defaults for the display properties.
    myVtuDisplay.Representation = 'Surface'
    # get color transfer function/color map for 'Stress_Mises'
    stress_MisesLUT = GetColorTransferFunction('Stress_Mises')
    # get opacity transfer function/opacity map for 'Stress_Mises'
    stress_MisesPWF = GetOpacityTransferFunction('Stress_Mises')
    # set scalar coloring
    ColorBy(myVtuDisplay, ('POINTS', 'Spatial_displacement', 'Magnitude'))
    # Hide the scalar bar for this color map if no visible data is colored
    by
    it.
    HideScalarBarIfNotNeeded(stress_MisesLUT, renderView1)
    # rescale color and/or opacity maps used to include current data range
    myVtuDisplay.RescaleTransferFunctionToDataRange(True, False)
    # show color bar/color legend
    myVtuDisplay.SetScalarBarVisibility(renderView1, True)
    # get color transfer function/color map for 'Spatial_displacement'
    Spatial_displacementLUT =
    GetColorTransferFunction('Spatial_displacement')
    # get opacity transfer function/opacity map for 'Spatial_displacement'
    Spatial_displacementPWF =
    GetOpacityTransferFunction('Spatial_displacement')
    Spatial_displacementLUT.ApplyPreset('Rainbow Uniform', True)
    # export view
    ExportView('F:/Abaqus_Study/baobi/7050-T7451/0705/gltf/disp/' + 'Job-1_'
               + 'f%03d' % i + '_U.gltf', InlineData=1,
               SaveNormal=1,
               SaveBatchId=1)
    # destroy myVtu
    Delete(myVtu)
    del myVtu
print("Total time: " + str(time() - time1) + "s")