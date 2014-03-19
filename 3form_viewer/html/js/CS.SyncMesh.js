

CS.SyncMesh = function(mesh){
    meshClone = mesh.clone();
    geometry = meshClone.geometry.clone();

    CS.scaleGeometry(geometry, new THREE.Vector3(meshClone.scale["x"],meshClone.scale["y"],meshClone.scale["z"]));
    CS.rotateGeometry(geometry, meshClone.rotation);

    meshClone.geometry = geometry;
    return meshClone;
}

CS.scaleGeometry = function(geometry, scale){
        // change all geometry.vertices
        for(var i = 0; i < geometry.vertices.length; i++) {
                var vertex      = geometry.vertices[i];
                vertex.multiply(scale); 
        }
        
        // mark the vertices as dirty
        geometry.__dirtyVertices = true;

        // return this, to get chained API      
        return this;
}

CS.rotateGeometry = function(geometry, rotation){
        // change all geometry.vertices
        for(var i = 0; i < geometry.vertices.length; i++) {
                var vertex      = geometry.vertices[i];
                vertex.applyEuler(rotation); 
        }
        
        // mark the vertices as dirty
        geometry.__dirtyVertices = true;

        // return this, to get chained API      
        return this;
}