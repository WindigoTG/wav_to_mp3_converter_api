from io import BytesIO
from typing import BinaryIO, Optional

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError, CouldntEncodeError


def convert_wav_to_mp3(data: bytes) -> Optional[bytes]:
    """
    Конвертирование wav файла в mp3 формат.

    Args:
        data (BinaryIO):
    """

    try:
        audio = AudioSegment(data=data)
        output = BytesIO()
        audio.export(output, 'mp3')
        return output.read()
    except (CouldntDecodeError, CouldntEncodeError):
        return None
