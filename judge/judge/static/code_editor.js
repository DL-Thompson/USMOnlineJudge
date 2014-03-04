var textarea = document.getElementById('code_editor');

  var editor = new CodeMirrorUI(textarea,
   {
  	    path : '',
	    buttons : ['load','save','undo','redo','jump','reindent','reindentSelection','search','about'],
        saveCallback : function(){ alert("Some saving goes here.  Probably AJAX or something fancy."); }
   },
   {
    mode: "text/x-c++src",
    lineNumbers : true,
    autofocus : true,
    matchBrackets: true
  });

