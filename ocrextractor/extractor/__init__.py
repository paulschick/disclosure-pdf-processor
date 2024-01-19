__app_name__ = 'ocrextractor'
__version__ = '0.1.0'

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    CONFIG_WRITE_ERROR,
    IMAGE_COPY_ERROR,
    EXTRACTION_ERROR,
) = range(6)

ERRORS = {
    DIR_ERROR: 'Configuration directory error',
    FILE_ERROR: 'Configuration file error',
    CONFIG_WRITE_ERROR: 'Configuration write error',
    IMAGE_COPY_ERROR: 'Image copy error',
    EXTRACTION_ERROR: 'Extraction error',
}
