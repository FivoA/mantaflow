#include "vectorbase.h"
#include "kernel.h"
#include "conjugategrad.h"
#include "multigrid.h"

#define PI 3.14159265358979323846

using namespace std;

namespace Manta {


// Populate velocity field with values according to taylor green vortex formula
// NOTE: I AM USING the domain [0, pi]
// 0 to pi is ONE HALF PERIOD AS NORMAL TG VORTEX USES A WHOLE PERIOD OF [0, 2pi]
KERNEL(bnd=1) void populateTGVortex(MACGrid& vel, Real domainSize) {
    const Real U0 = 0.04;
    const Real k_ = 2.0 * PI / domainSize; // 2 half periods right now
    
    const int resX = vel.getSizeX();
    const Real dx = domainSize / Real(resX - 2); // -2 because we have 1 boundary cell that is not liquid on each side of the domain

    // Locations where we measure U and V components respectively
    // Need to go half on other components as we measure in the middle of the face (face itself is staggered from center!)
    const Real xU = (i-1) * dx;
    const Real yU = (j - 0.5) * dx;
    const Real zU = (k - 0.5) * dx;

    const Real xV = (i - 0.5) * dx;
    const Real yV = (j-1) * dx;
    const Real zV = (k - 0.5) * dx;

    // According to TG definition formula:
    const Real u = U0 * sin(k_ * xU) * cos(k_ * yU) * cos(k_ * zU);
    const Real v = -U0 * cos(k_ * xV) * sin(k_ * yV) * cos(k_ * zV);
    const Real w = 0.0;
    vel(i, j, k) = Vec3(u,v,w);
}


PYTHON() void initTGVortex(
	MACGrid& vel, Real domainSize)
{
    populateTGVortex(vel, domainSize);
}
}