"""
We use this validator to filter ip that can access mobile zhihu website.
"""
from haipproxy.config.settings import (
    TEMP_MFW_QUEUE, VALIDATED_MFW_QUEUE, TTL_MFW_QUEUE, SPEED_MFW_QUEUE
)
from ..redis_spiders import ValidatorRedisSpider
from .base import BaseValidator


class MFWValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of zhihu proxy resources"""
    name = 'mfw'
    urls = [
        'http://www.mafengwo.cn/'
    ]
    task_queue = TEMP_MFW_QUEUE
    score_queue = VALIDATED_MFW_QUEUE
    ttl_queue = TTL_MFW_QUEUE
    speed_queue = SPEED_MFW_QUEUE
    success_key = '马蜂窝'
