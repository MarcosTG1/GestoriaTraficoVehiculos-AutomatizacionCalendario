# Este archivo permite que Python trate el directorio 'src' como un paquete.
__version__ = "0.1.0"

# Define qué se exporta cuando se hace: from src import *

from .services.ManejoDeEventos import (
    AnadirEventosCalendarioJustificantes,
    AnadirEventosCalendarioIncidencias,
    AnadirEventosCalendarioTrafico
)

from .services.ManejoGoogleCalendar import (
    get_calendar_service,
    add_event,
    delete_event
)

# Definir qué se exporta con from src import *
__all__ = [
    'AnadirEventosCalendarioJustificantes',
    'AnadirEventosCalendarioIncidencias',
    'AnadirEventosCalendarioTrafico',
    'get_calendar_service',
    'add_event',
    'delete_event',
]