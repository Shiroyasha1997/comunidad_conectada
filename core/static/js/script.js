$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  if ($('#tabla-principal').length > 0) {

    var table = new DataTable('#tabla-principal', {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
    });

  }

});