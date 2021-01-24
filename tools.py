def error_message(ex: Exception) -> str:
    """
    Gibt den String eines error Objekts zurück
    """

    if hasattr(ex, 'message'):
        return ex.message
    else:
        return ex