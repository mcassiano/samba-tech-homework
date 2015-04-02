var interval;

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
        }
    }
});

$(document).ready(function () {
    $('#status').progress();
    $('#status').css('display', 'none');
    $('#status').css('width', '300px');
    $('#status').css('margin', '0px auto');
});

function on_zencoder_job_done(output_url) {
    $.post("/save_video_details",
        {video_url: output_url}).done(function(data) {
            $('.label').html('<a href="' + data + '">Assista ao vídeo</a>');
    });
}

function poll_zencoder_job(job_id, output_url) {

    $.post("/encoder/get_status_on_job",
        {zencoder_job_id: job_id}).done(function(data) {

        data = $.parseJSON(data);

        $('.label').html(data.state);

        $('#status').progress({
            percent: data.progress
        });

        if (data.outputs[0].state == "finished") {

            $('#status').progress({
                percent: 100
            });

            clearTimeout(interval);

            on_zencoder_job_done(output_url);
        }
            
    });

}

function on_video_upload_done(url) {

    $.post("/encoder/add_job",
        {s3_input_file: url}).done(function(data) {

        data = $.parseJSON(data);
                
        var job_id = data.id;
        var output_url = data.outputs[0].url;

        $('#status').progress({
            percent: 0
        });

        interval = setInterval(function (data) {
            poll_zencoder_job(job_id, output_url);
        }, 1000);

    });

}

function s3_upload(){

    $('#status').css('display', 'block');

    var s3upload = new S3Upload({

        file_dom_selector: '#file',
        s3_sign_put_url: '/uploader/get_signed_s3_url',

        onProgress: function(percent, message) {

            $('#status').progress({
                percent: percent
            });

            $('.label').html(message);
        },

        onFinishS3Put: function(url) {
            $('.label').html('Upload completo. <br>Iniciando conversão...');
            on_video_upload_done(url);

        },
        onError: function(status) {
            $('#label').html('Erro ao enviar arquivo. ' + status);
        }
    });
}