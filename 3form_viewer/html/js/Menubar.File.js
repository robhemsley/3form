Menubar.File = function ( editor ) {

	var container = new UI.Panel();
	container.setClass( 'menu' );

	var title = new UI.Panel();
	title.setTextContent( 'File' );
	title.setMargin( '0px' );
	title.setPadding( '8px' );
	container.add( title );

	//

	var options = new UI.Panel();
	options.setClass( 'options' );
	container.add( options );

	// new

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'New' );
	option.onClick( function () {

		if ( confirm( 'Are you sure?' ) ) {

			editor.config.clear();
			editor.storage.clear( function () {

				location.href = location.pathname;

			} );

		}

	} );
	options.add( option );

	options.add( new UI.HorizontalRule() );


	// import

	var input = document.createElement( 'input' );
	input.type = 'file';
	input.addEventListener( 'change', function ( event ) {

		editor.loader.loadFile( input.files[ 0 ] );

	} );

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Import' );
	option.onClick( function () {

		input.click();

	} );
	options.add( option );

	options.add( new UI.HorizontalRule() );


	// export geometry

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export Geometry' );
	option.onClick( function () {

		var object = editor.selected;

		if ( object === null ) {

			alert( 'No object selected.' );
			return;

		}

		var geometry = object.geometry;

		if ( geometry === undefined ) {

			alert( 'The selected object doesn\'t have geometry.' );
			return;

		}

		if ( geometry instanceof THREE.BufferGeometry ) {

			exportGeometry( THREE.BufferGeometryExporter );

		} else if ( geometry instanceof THREE.Geometry2 ) {

			exportGeometry( THREE.Geometry2Exporter );

		} else if ( geometry instanceof THREE.Geometry ) {

			exportGeometry( THREE.GeometryExporter );

		}

	} );
	options.add( option );

	// export object

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export Object' );
	option.onClick( function () {

		if ( editor.selected === null ) {

			alert( 'No object selected' );
			return;

		}

		exportObject( THREE.ObjectExporter );

	} );
	options.add( option );

	// export scene

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export Scene' );
	option.onClick( function () {

		exportScene( THREE.ObjectExporter );

	} );
	options.add( option );

	// export OBJ

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export OBJ' );
	option.onClick( function () {

		exportGeometry( THREE.OBJExporter );

	} );
	options.add( option );
	
	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export STL' );
	option.onClick( function () {
		console.log(editor.selected);
		var blob = new Blob([exportSTL(editor.selected, {useObjectPosition:false})], {type: "application/stl"});
        saveAs(blob, editor.selected.name);
	} );
	options.add( option );
	
	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Export GCode' );
	option.onClick( function () {
        var tmp = new gcode(editor.selected);
		tmp.slice(function(gcodeData){
            var blob = new Blob([gcodeData], {type: "text/gcode"});
            console.log(editor.selected.name);
            saveAs(blob, (editor.selected.name+".gcode"));
		});
		
	} );
	options.add( option );

	var exportGeometry = function ( exporterClass ) {

		var object = editor.selected;
		var exporter = new exporterClass();

		var output;

		if ( exporter instanceof THREE.BufferGeometryExporter ||
			 exporter instanceof THREE.Geometry2Exporter ||
		     exporter instanceof THREE.GeometryExporter ) {

			output = JSON.stringify( exporter.parse( object.geometry ), null, '\t' );
			output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		} else {

			output = exporter.parse( object.geometry );

		}

		/*var blob = new Blob( [ output ], { type: 'text/plain' } );
		var objectURL = URL.createObjectURL( blob );

		window.open( objectURL, '_blank' );
		window.focus();*/
		
		var blob = new Blob([ output ], { type: 'text/plain' } );
        saveAs(blob, editor.selected.name);
	};

	var exportObject = function ( exporterClass ) {

		var object = editor.selected;
		var exporter = new exporterClass();

		var output = JSON.stringify( exporter.parse( object ), null, '\t' );
		output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		/*var blob = new Blob( [ output ], { type: 'text/plain' } );
		var objectURL = URL.createObjectURL( blob );

		window.open( objectURL, '_blank' );
		window.focus();*/
		
		var blob = new Blob([ output ], { type: 'text/plain' } );
        saveAs(blob, editor.selected.name);

	};

	var exportScene = function ( exporterClass ) {

		var exporter = new exporterClass();

		var output = JSON.stringify( exporter.parse( editor.scene ), null, '\t' );
		output = output.replace( /[\n\t]+([\d\.e\-\[\]]+)/g, '$1' );

		var blob = new Blob( [ output ], { type: 'text/plain' } );
		var objectURL = URL.createObjectURL( blob );

		window.open( objectURL, '_blank' );
		window.focus();

	};
	
	options.add( new UI.HorizontalRule() );

	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( 'Slice' );
	option.onClick( function () {
	    var tmp = new gcode(editor.selected);
		tmp.slice(function(gcodeData){
            var blob = new Blob([gcodeData], {type: "text/gcode"});
            console.log(editor.selected.name);

            object = createObjectFromGCode(gcodeData);
            editor.addObject(object);
		});
	} );
	options.add( option );
	
	var option = new UI.Panel();
	option.setClass( 'option' );
	option.setTextContent( '3D Print' );
	option.onClick( function () {

	    var tmp = new gcode(editor.selected);
		tmp.slice(function(gcodeData){
            var blob = new Blob([gcodeData], {type: "text/gcode"});

            object = createObjectFromGCode(gcodeData);
            editor.addObject(object);
            
            fd1 = new FormData();
                
            fd1.append('file', blob, editor.selected.name+".gcode");
            fd1.append('print', true);

                $.ajax({
                    url: 'http://octopi.media.mit.edu/api/load?apikey=246AC6F0229D4313954B796E7F1C165A',
                    type: "POST",
                    crossDomain: true,
                    data: fd1,
                    processData: false,
                    contentType: false,
                    success: function(responseer){
                        alert("Sent");
                    },
                    error: function(jqXHR, textStatus, errorMessage) {
                       console.log(errorMessage); // Optional
                       console.log(textStatus);
                       console.log(jqXHR);
                    }
                });
            
                        
		});		
		
	} );
	options.add( option );

	return container;

}
