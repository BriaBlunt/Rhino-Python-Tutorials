## VECTORS

import rhinoscriptsyntax as rs

vec1 = rs.GetObject("pick pt 01", 0)
vec2 = rs.GetObject("pick pt 02", 0)



#vec3 = rs.VectorAdd(vec1,vec2)

#rs.AddPoint(vec3)

    ##the third point (vec3) results in adding distance of pt 2
    ##from Origin to pt1's distance, as seen from Topview
    ##is like the two pts median... kinda

#vec3 = rs.VectorSubtract(vec1,vec2)
#rs.AddPoint(vec3)
    ##this produces to opposite effect as rs.VectorAdd
    ##it's the left behind (substracted) line btwn the two vectors
    ##and directed in the opposite direction
    ##the results wouls change if you changed the order of the "vec"s in the rhino action

#vec3 = rs.VectorCreate(vec1,vec2)
#rs.AddPoint(vec3)
    ##same result as subtraction

#vec1 = rs.VectorScale(vec1, 0.5)
    ##scaled the vector in half

#vec = rs.VectorUnitize(vec1)
    ## made the vector one unit in length
    ##useful for specifying direction and such


vec3 = rs.VectorSubtract(vec2,vec1)
    ##directinality
vec3 = rs.VectorUnitize(vec3)
    ##unitize
vec3 = rs.VectorScale(vec3,2)
    ##make it really small
vec3 = rs.VectorAdd(vec3,vec1)



rs.AddPoint(vec3)
