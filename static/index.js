$(document).ready(function() {
    $('.select2').select2();

    $('#togglePassword').click(function() {
        const passwordField = $('#txtpassword');
        const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
        passwordField.attr('type', type);
        $(this).toggleClass('fa-eye fa-eye-slash');
    });

    $('#type').change(function () {
        const selectedType = $(this).val();
        const subtypeDropdown = $('#subtype');

        // Disable subtype dropdown initially
        subtypeDropdown.empty().attr('disabled', true).html('<option value="0">Select</option>');
        $('.clsdownload').hide();

        // Make an AJAX call to fetch subtypes for the selected type
        $.ajax({
            url: `/get_subtypes/${selectedType}`, // Endpoint to fetch subtypes
            type: 'GET',
            success: function (response) {
                // Clear and enable the subtype dropdown
                // subtypeDropdown.empty().attr('disabled', true);
                debugger;
                if(response != null && response.length > 0){
                    subtypeDropdown.empty().attr('disabled', false);
                    subtypeDropdown.append('<option value="">Select</option>');

                    // Populate the subtype dropdown with response data
                    response.forEach(function (item) {
                        const option = new Option(item.SheetName, item.SheetName, false, false);
                        subtypeDropdown.append(option);
                        // subtypeDropdown.append(`<option value="${item.SheetName}">${item.SheetName}</option>`);
                    });
                }
            },
            error: function (xhr, status, error) {
                // Handle errors
                subtypeDropdown.empty().append('<option value="">Error loading subtypes</option>');
                console.error('Error fetching subtypes:', error);
            }
        });
    });

    $('.clsdownload').hide();
    $('#subtype').change(function () {
        const selectedSubtype = $(this).val();
        const downloadLink = $('.clsdownload a');
        // $('#downloadButton').attr('disabled', !selectedSubtype);
        if (selectedSubtype) {
            // Update the href for the download link
            downloadLink.attr('href', `/downloadTemplates/${selectedSubtype}.xlsx`);
            // Show the download icon
            $('.clsdownload').show();
        } else {
            // Hide the download icon if no subtype is selected
            $('.clsdownload').hide();
        }
    });
    
    $('#uploadForm').on('submit', function(e) {
        $('#result').html("")
        e.preventDefault();  
        $('#progress-section').show();  // Show progress section on form submission
        $('#progress-bar').css('width', '0%');
        $('#progress-text').text('0');
        $('#sheet-name').text('');
        const submitButton = $('#btnSubmit');
        submitButton.prop('disabled', true).text('Uploading...'); 
        debugger;
        var formData = new FormData(this);

        $.ajax({
            url: '/upload',  // The Flask endpoint
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // If the server returns a file link, display it
                if (response.error_files) {
                    debugger;
                    $('#result').html('<a href=/download/' + response.error_files + '><i class="fa fa-download" aria-hidden="true"> </i> Download Status File </a> ').show();
                } else {
                    $('#result').html('<p>' + response.message + '</p>').show();
                }
                $('#progress-section').hide();
                submitButton.prop('disabled', false).text('Submit');
            },
            error: function(xhr, status, error) {
                $('#progress-section').hide();
                $('#result').html('<p>Error: ' + xhr.responseText + '</p>').show();
                submitButton.prop('disabled', false).text('Submit');
            }
        });
    });
    // var socket = io();

    // socket.on('progress_update', function(data) {
    //     $('#sheet-name').text(data.sheet_name);
    //     $('#progress-bar').css('width', data.progress + '%');
    //     $('#progress-text').text(data.progress);
    // });
});
