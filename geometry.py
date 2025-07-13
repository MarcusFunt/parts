import numpy as np
from geomdl import BSpline
from geomdl import utilities

class SplineProfile:
    """Represents an axisymmetric nozzle profile defined by spline control points."""

    def __init__(self, control_points):
        self.control_points = control_points
        self.curve = BSpline.Curve()
        self.curve.degree = 3
        self.curve.ctrlpts = control_points
        self.curve.knotvector = utilities.generate_knot_vector(self.curve.degree, len(control_points))

    def sample(self, num=100):
        """Samples the spline curve."""
        return np.array(self.curve.evalpts)

    def update_points(self, control_points):
        self.control_points = control_points
        self.curve.ctrlpts = control_points
        self.curve.knotvector = utilities.generate_knot_vector(self.curve.degree, len(control_points))

    def to_dxf(self, path):
        """Export the profile to a DXF polyline."""
        import ezdxf
        doc = ezdxf.new()
        msp = doc.modelspace()
        pts = self.sample()
        msp.add_polyline2d([(p[0], p[1]) for p in pts])
        doc.saveas(path)
