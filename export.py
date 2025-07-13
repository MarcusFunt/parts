from geometry import SplineProfile


def export_profile(control_points, path):
    profile = SplineProfile(control_points)
    profile.to_dxf(path)
