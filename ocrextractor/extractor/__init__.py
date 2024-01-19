__app_name__ = 'extractor'
__version__ = '0.1.0'

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
) = range(3)

ERRORS = {
    DIR_ERROR: 'Configuration directory error',
    FILE_ERROR: 'Configuration file error',
}
