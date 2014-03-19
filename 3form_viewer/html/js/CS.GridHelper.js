CS = function(){
}

CS.GridHelper = function(size, step) {
	var geometry = new THREE.Geometry();
	var material = new THREE.LineBasicMaterial( { vertexColors: THREE.VertexColors } );

	this.color1 = new THREE.Color( 0x444444 );
	this.color2 = new THREE.Color( 0x888888 );

	for ( var i = 0; i <= size; i += step ) {

		geometry.vertices.push(
			new THREE.Vector3(0, i, 0), new THREE.Vector3(size, i, 0),
			new THREE.Vector3(i, 0, 0), new THREE.Vector3(i, size, 0)
		);

		var color = i === 0 ? this.color1 : this.color2;

		geometry.colors.push( color, color, color, color );
	}
	
	geometry.vertices.push(
	    new THREE.Vector3(0, size, 0), new THREE.Vector3(size, size, 0),
		new THREE.Vector3(size, 0, 0), new THREE.Vector3(size, size, 0)
	);

	var color = this.color1;
	geometry.colors.push( color, color, color, color );

	THREE.Line.call( this, geometry, material, THREE.LinePieces );

};

CS.GridHelper.prototype = Object.create( THREE.Line.prototype );

CS.GridHelper.prototype.setColors = function( colorCenterLine, colorGrid ) {

	this.color1.set( colorCenterLine );
	this.color2.set( colorGrid );

	this.geometry.colorsNeedUpdate = true;

}
