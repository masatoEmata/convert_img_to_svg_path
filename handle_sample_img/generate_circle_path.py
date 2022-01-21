import math
import svgwrite

dwg = svgwrite.Drawing( "sample_circle.svg" )

def plotter(length):
	points = []
	for i in range( 720 ):
		x = length * math.cos( math.radians( 360.0/720 * i ) )
		y = length * math.sin( math.radians( 360.0/720 * i ) )
		points.append( [x,y] )
	return points

points = plotter(10)
print(f'Sample points data: {points}')
dwg.add(dwg.polygon(points=points))

points = plotter(20)
print(f'Sample points data: {points}')
dwg.add( dwg.polygon( points=points , stroke='blue', stroke_width=3.0, fill='none') )

dwg.save()