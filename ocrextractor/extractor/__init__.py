__app_name__ = 'ocrextractor'
__version__ = '0.1.0'

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    CONFIG_WRITE_ERROR,
) = range(4)

ERRORS = {
    DIR_ERROR: 'Configuration directory error',
    FILE_ERROR: 'Configuration file error',
}
