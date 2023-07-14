from gl import Renderer, V2

width = 1920
height = 1080

rend = Renderer(width, height)

rend.glClearColor(0,0,0)
rend.glClear()

rend.glColor(1,1,1)
rend.glPoint(250,250)

rend.glLine(V2(0,0), V2(100,250))

rend.glTriangle(V2(10,70), V2(50,160), V2(70,80))

rend.glFinish("output.bmp")