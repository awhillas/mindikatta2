/*
  see: https://www.html5rocks.com/en/tutorials/file/dndfiles/

expects:
<form id="UPLOAD_FORM" action="http//.../">
  <input class="btn btn-warning" type="file" id="files" name="file" />
  <div id="PROGRESS_BAR"><div class="percent">0%</div></div>
  <button id= "CANCEL_BTN" onclick="abortRead();">Cancel</button>
</form>

*/

// Check for the various File API support.
if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
  alert('The File APIs are not fully supported in this browser.');
}


var reader;
var progress = document.querySelector('.percent');
$('#CANCEL_BTN').hide();
$('#PROGRESS_BAR').hide();

function abortRead() {
  reader.abort();
}

function errorHandler(evt) {
  switch(evt.target.error.code) {
    case evt.target.error.NOT_FOUND_ERR:
      alert('File Not Found!');
      break;
    case evt.target.error.NOT_READABLE_ERR:
      alert('File is not readable');
      break;
    case evt.target.error.ABORT_ERR:
      break; // noop
    default:
      alert('An error occurred reading this file.');
  };
}

function updateProgress(evt) {
  // evt is an ProgressEvent.
  if (evt.lengthComputable) {
    var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
    // Increase the progress bar length.
    if (percentLoaded < 100) {
      progress.style.width = percentLoaded + '%';
      progress.textContent = percentLoaded + '%';
    }
  }
}

function handleFileSelect(evt) {
  // Reset progress indicator on new file selection.
  progress.style.width = '0%';
  progress.textContent = '0%';

  reader = new FileReader();
  reader.onerror = errorHandler;
  reader.onprogress = updateProgress;
  reader.onabort = function(e) {
    alert('File read cancelled');
  };
  reader.onloadstart = function(e) {
    $('#CANCEL_BTN').show();
    $('#PROGRESS_BAR').show();
    document.getElementById('PROGRESS_BAR').className = 'loading';
  };
  reader.onload = function(e) {
    
    // Update GUI

    $('#CANCEL_BTN').hide();

    // Ensure that the progress bar displays 100% at the end.
    progress.style.width = '100%';
    progress.textContent = '100%';
    setTimeout("document.getElementById('PROGRESS_BAR').className='';", 2000);
    
    // Send XML to the server
    
    // Obtain the read file data
    let xml = e.target.result;
    
    // Parse the XML?
    // let xmldoc = $.parseXML( xml );
    // console.log(xmldoc);

    // POST it to the server
    $.ajax({
        type: "POST",
        url: $('#UPLOAD_FORM').attr('action'),
        dataType: "json",  // what we expect back
        contentType: "application/xml",
        data: xml,
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        success: function (res) {
            console.log("Data has been saved!");
        },
        error: function (res) {
            alert("There was a problem, server said: " + res.statusText);
        }
    });
  }

  // Read in the XML file as a text sting.
  reader.readAsText(evt.target.files[0]);
}

document.getElementById('files').addEventListener('change', handleFileSelect, false);
