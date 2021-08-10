import sys
import vtk

def create_stl_render():
    colors = vtk.vtkNamedColors()
    bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
    colors.SetColor("BkgColor", *bkg)
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(renWin)
    reader = vtk.vtkSTLReader()
    filename = sys.argv.pop(-1)
    reader.SetFileName(filename)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(reader.GetOutputPort())
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    axes = vtk.vtkAxesActor()
    marker = vtk.vtkOrientationMarkerWidget()
    marker.SetInteractor(iren )
    marker.SetOrientationMarker( axes )
    marker.SetViewport(0.75,0,1,0.25)
    marker.SetEnabled(1)
    ren.AddActor(coneActor)
    ren.SetBackground(colors.GetColor3d("BkgColor"))
    renWin.SetSize(500, 500)
    iren.Initialize()
    ren.ResetCamera()
    ren.GetActiveCamera().Zoom(1.5)
    renWin.Render()
    iren.Start()
    return renWin, iren

def close_stl_render(iren):
    render_window = iren.GetRenderWindow()
    render_window.Finalize()
    iren.TerminateApp()

renWin, iren = create_stl_render()
close_stl_render(iren)
del renWin, iren