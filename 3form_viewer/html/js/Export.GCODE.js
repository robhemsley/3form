gcode = function ( mesh ) {
    this.mesh = CS.SyncMesh(mesh);
        
    this.slice = function(callback){
        blob = new Blob([exportSTL(this.mesh, {useObjectPosition:true})], {type: "application/stl"});
        fd = new FormData();
        fd.append('stl', blob);
        fd.append('print', false);
        
		this.mesh.geometry.computeBoundingBox();
        
        minX = this.mesh.geometry.boundingBox.min.x;
        minY = this.mesh.geometry.boundingBox.min.y;
        minZ = this.mesh.geometry.boundingBox.min.z;
        maxX = this.mesh.geometry.boundingBox.max.x;
        maxY = this.mesh.geometry.boundingBox.max.y;
        maxZ = this.mesh.geometry.boundingBox.max.z;

        if (minX < 0){
            centerX = this.mesh.position.x;
        }else{
            centerX = this.mesh.position.x+(maxX/2);
            centerX = this.mesh.position.x+((Math.abs(maxX)-Math.abs(minX))/2);

        }
        
        if(minY < 0){
            centerY = this.mesh.position.y;
        }else{
            console.log("H");
            console.log('x', centerX);
            console.log('minY', minY);
            console.log('maxY', maxY);

            centerY = this.mesh.position.y+((Math.abs(maxY)-Math.abs(minY))/2);
        }
        
        if(minZ < 0){
            centerZ = this.mesh.position.z+minZ;
        }else{
            centerZ = this.mesh.position.z;
            //centerZ = this.mesh.position.z+((Math.abs(maxZ)-Math.abs(minZ))/2);
        }
        
        //centerZ = 0;

        console.log("Center");
        console.log('x', centerX);
        console.log('y', centerY);
        console.log('z', centerZ);
        console.log('minz', minZ);
        console.log('maxz', maxZ);

        fd.append('x', centerX);
        fd.append('y', centerY);
        fd.append('z', centerZ);
        
        var scope = this;
        
        $.ajax({
            url: '/v1/slice/',
            type: "POST",
            data: fd,
            processData: false,
            contentType: false,
            success: function(response){
                //callback(response, scope.mesh)
                GetProgress(response, callback, scope.mesh);
            },
            error: function(jqXHR, textStatus, errorMessage) {
               console.log(errorMessage); // Optional
            }
        });
        
        
    }
}


function GetProgress(id, callback, mesh) {
    $.ajax({
        url: "http://localhost:8088/v1/progress/?id="+id,
        success: function (msg) {
            console.log(msg)
            
            $("#progressTest").progressbar( "option", {
                value: Math.floor( msg )
             });
            //$("#pbrQuery").progressbar("value", data.value);
            
            if (msg == 100) {                
                $.ajax({
                    url: "http://localhost:8088/v1/gcode/?id="+id,
                    success: function (response) {
                        callback(response, mesh);
                          $("#progressTest").progressbar( "option", {
                            value: Math.floor( 0 )
                            });
                    }
                });
            } else {
                setTimeout(function(){GetProgress(id, callback, mesh)}, 500);
            }
        }
    });
}


