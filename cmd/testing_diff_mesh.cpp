/*
    Copyright 2008 Brain Research Institute, Melbourne, Australia

    Written by Robert E. Smith, 2015.

    This file is part of MRtrix.

    MRtrix is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MRtrix is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MRtrix.  If not, see <http://www.gnu.org/licenses/>.

*/

#include "command.h"
#include "progressbar.h"

#ifdef MRTRIX_UPDATED_API
#include "types.h"
#endif

#include "mesh/mesh.h"

using namespace MR;
using namespace App;

void usage ()
{
  DESCRIPTION
  + "compare two mesh files for differences, within specified tolerance. "
    "Note that vertex normals are currently not tested.";

  ARGUMENTS
  + Argument ("in1", "a mesh file.").type_file_in ()
  + Argument ("in2", "another mesh file.").type_file_in ()
  + Argument ("tolerance", "the maximum distance to consider acceptable").type_float (0.0, 0.0);
}



void run ()
{
#ifdef MRTRIX_UPDATED_API
  const default_type dist_sq = Math::pow2 (default_type(argument[2]));
#else
  const float dist_sq = Math::pow2 (float(argument[2]));
#endif

  Mesh::Mesh in1 (argument[0]), in2 (argument[1]);
  
  if (in1.num_vertices() != in2.num_vertices())
    throw Exception ("Mismatched vertex count - test FAILED");
  if (in1.num_triangles() != in2.num_triangles())
    throw Exception ("Mismatched triangle count - test FAILED");
  if (in1.num_quads() != in2.num_quads())
    throw Exception ("Mismatched quad count - test FAILED");
    
  // For every triangle and quad in one file, there must be a matching triangle/quad in the other
  // Can't rely on a preserved order; need to look through the entire list for a triangle/quad for
  //   which every vertex has a corresponding vertex
  
  for (size_t i = 0; i != in1.num_triangles(); ++i) {
    // Explicitly load the vertex data
#ifdef MRTRIX_UPDATED_API  
    std::array<Eigen::Vector3, 3> v1;
#else 
    std::array<Point<float>, 3> v1;
#endif
    for (size_t axis = 0; axis != 3; ++axis)
      v1[axis] = in1.vert(in1.tri(i)[axis]);
    bool match_found = false;
    for (size_t j = 0; j != in2.num_triangles() && !match_found; ++j) {
#ifdef MRTRIX_UPDATED_API 
      std::array<Eigen::Vector3, 3> v2;
#else 
      std::array<Point<float>, 3> v2;
#endif
      for (size_t axis = 0; axis != 3; ++axis)
        v2[axis] = in1.vert (in1.tri(i)[axis]);
      for (size_t a = 0; a != 3; ++a) {
        size_t b = 0;
        for (; b != 3; ++b) {
#ifdef MRTRIX_UPDATED_API
          if ((v1[a]-v2[b]).squaredNorm() < dist_sq)
#else
          if (dist2 (v1[a], v2[b]) < dist_sq)
#endif          
            break;
            
        }
        if (b == 3)
          throw Exception ("Unmatched vertex - test FAILED");
      }
    }
    if (!match_found)
      throw Exception ("Unmatched triangle - test FAILED");
  }
  
  for (size_t i = 0; i != in1.num_quads(); ++i) {
#ifdef MRTRIX_UPDATED_API  
    std::array<Eigen::Vector3, 4> v1;
#else 
    std::array<Point<float>, 4> v1;
#endif
    for (size_t axis = 0; axis != 4; ++axis)
      v1[axis] = in1.vert (in1.quad(i)[axis]);
    bool match_found = false;
    for (size_t j = 0; j != in2.num_quads() && !match_found; ++j) {
#ifdef MRTRIX_UPDATED_API 
      std::array<Eigen::Vector3, 4> v2;
#else 
      std::array<Point<float>, 4> v2;
#endif
      for (size_t axis = 0; axis != 4; ++axis)
        v2[axis] = in1.vert (in1.quad(i)[axis]);
      for (size_t a = 0; a != 4; ++a) {
        size_t b = 0;
        for (; b != 4; ++b) {
#ifdef MRTRIX_UPDATED_API
          if ((v1[a]-v2[b]).squaredNorm() < dist_sq)
#else
          if (dist2 (v1[a], v2[b]) < dist_sq)
#endif          
            break;
            
        }
        if (b == 4)
          throw Exception ("Unmatched vertex - test FAILED");
      }
    }
    if (!match_found)
      throw Exception ("Unmatched quad - test FAILED");
  }

  CONSOLE ("data checked OK");
}

