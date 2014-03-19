
function exportSTL(mesh, options ) {

    if (mesh instanceof Array) {
    }else{
        alert("not array")
    }
    console.log(mesh);
    
    geometry = mesh.geometry;

	// calculate the faces and normals if they are not yet present
	geometry.computeFaceNormals();

	var addX = addY = addZ = 0;

	if ( options ) {
		if ( options.useObjectPosition ) {
			addX = mesh.position.x;
			addY = mesh.position.y;
			addZ = mesh.position.z;
		}
	}
	
	var facetToStl = function( verts, normal ) {
		var faceStl = ''
		faceStl += 'facet normal ' + normal.x + ' ' + normal.y + ' ' +  normal.z + '\n'
		faceStl += 'outer loop\n'

		for ( var j = 0; j < 3; j++ ) {
			var vert = verts[j]
			faceStl += 'vertex ' + (vert.x+addX) + ' ' + (vert.y+addY) + ' ' + (vert.z+addZ) + '\n'
		}

		faceStl += 'endloop\n'
		faceStl += 'endfacet\n'
	
		return faceStl
	}

	// start bulding the STL string
	var stl = ''
	stl += 'solid\n'
	
	for ( var i = 0; i < geometry.faces.length; i++ ) {
		var face = geometry.faces[i]

		// if we have just a griangle, that's easy. just write them to the file
		if ( face.d === undefined ) {
			var verts = [
				geometry.vertices[ face.a ],
				geometry.vertices[ face.b ],
				geometry.vertices[ face.c ]
			]

			stl += facetToStl( verts, face.normal )

		} else {
			// if it's a quad, we need to triangulate it first
			// split the quad into two triangles: abd and bcd
			var verts = []
			verts[0] = [
				geometry.vertices[ face.a ],
				geometry.vertices[ face.b ],
				geometry.vertices[ face.d ]
			]
			verts[1] = [
				geometry.vertices[ face.b ],
				geometry.vertices[ face.c ],
				geometry.vertices[ face.d ]
			]
			
			for ( var k = 0; k<2; k++ ) {
				stl += facetToStl( verts[k], face.normal )
			}
		}
	}

	stl += 'endsolid'

	return stl
}
