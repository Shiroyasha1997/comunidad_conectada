document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,dayGridDay'
        },
        selectable: true,
        events: '{% url "cargar_eventos" %}',
        select: function(info) {
            $('#crearReservaModal').modal('show');
            document.getElementById('fecha_inicio').value = info.startStr;
            document.getElementById('fecha_fin').value = info.endStr;
        },
        eventClick: function(info) {
            if (confirm("¿Estás seguro que deseas eliminar esta reserva?")) {
                $.ajax({
                    url: '{% url "eliminar_reserva" 0 %}'.replace('0', info.event.id),
                    type: 'DELETE',
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    success: function() {
                        info.event.remove();
                        alert('Reserva eliminada exitosamente.');
                    }
                });
            }
        }
    });
    calendar.render();
});
